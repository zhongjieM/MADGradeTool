'''
Created on Jan 30, 2015

@author: kevin
'''

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib


GMAIL_USER = ''
GMAIL_PASS = ''

DEFAULT_TO_ADDR1 = ''
DEFAULT_TO_ADDR2 = ''

def send_out_grade(attach_file_path, subject='Assignment Grade', to_addr=DEFAULT_TO_ADDR1):

    if os.path.exists(attach_file_path) == False:
        print 'Error: The attachment file does not exists: '.join(attach_file_path)
        return

    if os.path.isfile(attach_file_path) == False:
        print 'Error: The attachment file path does not link to a file: '.join(attach_file_path)
        return

    attach_file_name = os.path.basename(attach_file_path)
    attach_file = open(attach_file_path, 'r')

    print '--------------------------------------------------------------------'
    print 'Sending Email to: ' + to_addr
    print 'Subject: ' + subject
    print 'Attached file name is: ' + attach_file_name
    print '--------------------------------------------------------------------'

    from_addr = 'zhongjie.mao@gmail.com'
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject

    content = MIMEText('Hi,\n' \
                       '\n' \
                       'Please find your ' + subject + ' in the attached file.\n\n' \
                       'The due date for this assignment is on Feb. 22.\n' \
                       'We updated your apps on Feb. 24.\n' \
                       'We graded your apps from Feb. 25 to Feb. 27 without accepting any updates.\n\n' \
                       'If the grade does not belong to you, please contact graders ASAP.\n' \
                       'If your grades is 0 or quite low, check if you have applied late pass. We will do regrade next week as stated in a previous post on piazza.\n' \
                       'We will process all of your Emails regarding grades on Tuesday afternoon. \n\n' \
                       'Regards,\n' \
                       'Zhongjie & Ameya\n', 'plain')

    msg.attach(content);

    part = MIMEBase('application', "octet-stream")
    part.set_payload(attach_file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename=' + attach_file_name)
    msg.attach(part)
    send_email(from_addr, to_addr, msg.as_string())


def send_email(from_addr, to_addr, msg):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PASS);
    server.sendmail(from_addr, to_addr, msg)
    server.quit()
