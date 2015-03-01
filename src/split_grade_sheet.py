#!/usr/bin/env python

'''
Created on Jan 30, 2015

@author: kevin
'''

import os
import shutil
import sys
from tempfile import TemporaryFile

from send_grades import send_out_grade
import xlrd
import xlwt
from test.test_zipimport import TESTMOD

## If TEST_MODE is enabled, all the grade will be sent to the default address
## The default addresses are specified in send_grades.py file.
TEST_MODE = False
## If GRADER_MODE is enabled, the tool will only work for those students that
## belong to the specified grader. Specify the grader name to GRADER below.
GRADER_MODE = False
GRADER = ''

SEND_OUT_DIR = '/send_out/'

HEAD_ROW_COUNT = 2
NAME_COL = 1
EMAIL_COL = 2
GRADER_COL = 3

def split(file_path, send_out_dir, sheet_index=-1):
    gradesheets = xlrd.open_workbook(file_path);
    sheet = gradesheets.sheet_by_index(sheet_index)

    nrows = sheet.nrows;
    if nrows < HEAD_ROW_COUNT:
        error('Row number is smaller than {0}'.format(HEAD_ROW_COUNT))

    # Get head rows from the sheet
    head_rows = []
    for row in range(0, HEAD_ROW_COUNT):
        head_row = sheet.row_values(row, 0)
        head_rows.append(head_row)

    # Check if Grader column exists in the sheet
    hasGraderColumn = False
    for head_row in head_rows:
        if head_row[GRADER_COL].lower() == 'grader':
            hasGraderColumn = True
            break

    if hasGraderColumn == False:
        for head_row in head_rows:
            print head_row[GRADER_COL]
        error('There is no grader column. Please add grader column and put grader inside. Then try again.')

    for row in range(HEAD_ROW_COUNT, nrows):
        student_data = sheet.row_values(row, 0)
        if GRADER_MODE:
            grader_name = student_data[GRADER_COL]
            if grader_name.lower() == GRADER.lower():
                create_student_doc(send_out_dir, head_rows, student_data)
        else:
            create_student_doc(send_out_dir, head_rows, student_data)


def clear_send_out_dir(send_out_dir):
    if os.path.exists(send_out_dir) == True:
        shutil.rmtree(send_out_dir)
    os.makedirs(send_out_dir)

def create_student_doc(send_out_dir, head_rows, data):
    email = data[EMAIL_COL];
    file_path = send_out_dir + email + '.xls'
    newWorkBook = xlwt.Workbook()
    sheet = newWorkBook.add_sheet('Grade')

    row = 0
    for head_row in head_rows:
        for col in range(0, len(head_row)):
            sheet.write(row, col, head_row[col])
        row = row + 1

    for col in range(0, len(data)):
        sheet.write(row, col, data[col])

    newWorkBook.save(file_path)
    newWorkBook.save(TemporaryFile())

def error(msg):
    print msg
    sys.exit()

def main():
    # handle args
    args = sys.argv
    if len(args) <> 4:
        error('Please specify the path or the name of the file'\
              ', the number of assignment'\
              ' and the subject of email! \n'\
              ' e.g. grade assignment.xlst 1 Assignment\ 1\ grade')

    # handle file paths
    file_path = args[1]
    if os.path.exists(file_path) == False:
        error('The file does not exist!')
    file_path = os.path.abspath(file_path)
    send_out_dir = os.path.dirname(file_path) + SEND_OUT_DIR
    clear_send_out_dir(send_out_dir)

    # get assignment number
    assignment = -1
    try:
        assignment = int(args[2])
        if assignment < 1:
            assignment = -1
            error('Invalid assignment number!')
    except ValueError:
        error('Invalid assignment number!')

    # get subject
    subject = args[3]

    # start work
    split(file_path, send_out_dir, assignment)

    # send grades out
    files = os.listdir(send_out_dir)
    for fn in files:
        file_name = os.path.basename(fn)
        to_addr = file_name.split('.xls')[0]
        if TEST_MODE:
            send_out_grade(send_out_dir + file_name, subject)
        else:
            send_out_grade(send_out_dir + file_name, subject, to_addr)


if __name__ == '__main__':
    main()
