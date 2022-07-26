#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# This file is part of Tatyana.
#
# Copyright (C) 2022  Dialogue Movement contributors.  See AUTHORS.
#
# Tatyana is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tatyana is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from dotenv import load_dotenv
from glob import glob
import base64
import smtplib
import gspread
import time
import os

load_dotenv()


def encode_base64(s: str) -> str:
    encoded_text = base64.b64encode(s.encode("utf-8")).decode("ascii")
    return f"=?utf-8?b?{encoded_text}?="

    
def format_named_address(name: str, addr: str):
    return f"{encode_base64(name)} <{addr}>"


def addresses(addrstring):
    return [x.strip() for x in addrstring.split(',')]


def sendMessage(msg_subject, msg_body):

    # Connect to Google Sheets

    gc = gspread.service_account()

    sheet = gc.open_by_key(os.getenv('SHEET_ID'
                           )).worksheet(os.getenv('SHEET_NAME'))

    last_index = sheet.get('E2:E')[-1][0].split('/')[0]

    # SMTP variables

    SMTP_HOST = os.getenv('SMTP_HOST')
    SMTP_PORT = os.getenv('SMTP_PORT')
    SMTP_USER = os.getenv('SMTP_USER')
    SMTP_PASSWORD = os.getenv('SMTP_PASS')

    # Sender headers

    EMAIL_FROM_NAME = os.getenv('FROM_NAME')
    EMAIL_FROM_ADDR = os.getenv('FROM_ADDR')
    EMAIL_SUBJECT = \
        "Исх. № {} {} от Каяшкиной Т. А.".format(str(int(last_index)
            + int(1)) + '/' + time.strftime(str('%y')),
            time.strftime('%d.%m.%Y'))

    # Recipient headers

    DESTINATION_NAME = os.getenv('DEST_NAME')
    DESTINATION_ADDR = os.getenv('DEST_ADDR')

    # Special headers

    CARBONCOPY_NAME = os.getenv('COPY_NAME')
    CARBONCOPY_ADDR = os.getenv('COPY_ADDR')
    RETURN_RECEIPT_NAME = os.getenv('RCPT_NAME')
    RETURN_RECEIPT_ADDR = os.getenv('RCPT_ADDR')
    ORGANIZATION_NAME = os.getenv('ORG_NAME')

    smtp = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    smtp.starttls()
    smtp.login(SMTP_USER, SMTP_PASSWORD)

    # Message object

    msg = MIMEMultipart()
    msg['Content-Type'] = 'text/plain; charset=utf-8'
    msg['Subject'] = encode_base64(EMAIL_SUBJECT)

    msg['From'] = format_named_address(EMAIL_FROM_NAME, EMAIL_FROM_ADDR)
    msg['To'] = format_named_address(DESTINATION_NAME, DESTINATION_ADDR)
    msg['Cc'] = format_named_address(CARBONCOPY_NAME, CARBONCOPY_ADDR)
    msg['Organization'] = encode_base64(ORGANIZATION_NAME)
    msg['Disposition-Notification-To'] = \
        format_named_address(RETURN_RECEIPT_NAME, RETURN_RECEIPT_ADDR)

    part1 = MIMEText(msg_body, 'plain', 'UTF-8')
    msg.attach(part1)

    files = glob('attachments/*.jpg')

    for path in files:
        part2 = MIMEBase('application', 'octet-stream')
        with open(path, 'rb') as file:
            part2.set_payload(file.read())
        encoders.encode_base64(part2)
        part2.add_header('Content-Disposition',
                         'attachment; filename={}'.format(Path(path).name))
        msg.attach(part2)

    smtp.sendmail(SMTP_USER, addresses(DESTINATION_ADDR)
                  + addresses(CARBONCOPY_ADDR), msg.as_bytes())
    smtp.quit()

    # Update data in Google Sheets

    sheet.append_row([
        msg_subject,
        "Администрация Коломны",
        time.strftime('%d.%m.%Y'),
        "—",
        str(int(last_index) + int(1)) + '/' + time.strftime(str('%y')),
        "—",
        "Регистрация",
        "—",
        "—",
        "—",
        "—",
        '',
        ])
