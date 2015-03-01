################################# README ######################################
AUTHOR:
  ZHONGJIE MAO
  zhongjie.mao@husky.neu.edu


BEFORE USE

1.	This tool has only been tested on the following environment:
    1) Mac OSX, Python 2.7.5
2.	Before you use the tool, make sure the following python modules have been
    installed:
    1) xlrd
    2) xlwt
    ** These two modules are open source and used for read & write excel files.
3.	If you use Gmail account to send the grades, make sure your Gmail account allow
    less secure apps:
    Google Account -> Sign In Section -> Access for less secure apps -> Turn on
4.	Set your Gmail account:
    In send_grade.py file, set your Gmail account's username and password into:
    GMAIL_USER
    GMAIL_PASS


TEST MODE AND GRADER MODE

  The tool support two more helper and debug modes: TEST mode and GRADER mode.

1.	TEST MODE:
    If TEST mode is enabled, all the grades will be sent to the default address
    specified in send_grades.py file.

    How to enable:
    1)	In split_grade_sheet.py, change TEST_MODE to True.
    2)	In send_grades.py, set default address to DEFAULT_TO_ADDRESS1

2.	GRADER MODE:
    If GRADER mode is enabled, only students belong to the specified grader will be
    processed.

    How to enable:
    1)	In split_grade_sheet.py, change GRADER_MODE to True.
    2)	In split_grade_sheet.py, assign grader's name to GRADER.


FORMAT CONSTRAINTS ON EXCEL FILE

1.	Make sure the excel sheet has the following format:
    1) The first two rows are heads. Students' records start from the third row.
    2) The first four columns should be:
      (1) Student Id
      (2) Student Name
      (3) Student Email
      (4) Grader Name


USE THE TOOL

1.	Command of the tool:
    1)	Make "split_grade_sheet.py" executable.
    2)	Add an alias for the tool:
        In your ~/.bash_profile, add:
        alias grade='/path/to/split_grade_sheet.py'
    3) Command format:

        grade [/path/to/excel/file] [n] [subject]

      Explanation:

        [/path/to/excel/file]: this should be the path to the excel file. It can
                               be absolute or relative path.
        [n]: this argument should be the sheet index (start from 0) that you would
             like of which you would like to process.
        [subject]: this will be the subject of email which you will send to students.

      Example: grade /path/to/excel/file 5 Assignment\ 1\ grade


HOW IT WORKS

  To be continue...