#!/usr/bin/python
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
from glob import glob
import time
import os

load_dotenv()

# Local variables

msg_body = ''


def generateMessage(msg_type, msg_addresses):
    if msg_type == "Разбросанный мусор":

        # Subject

        msg_subject = "Об уборке мусора"

        # Addresses

        if len(msg_addresses.replace('\\n', '\n').splitlines()) == 1:
            msg_addresses_string = "•" + ' ' + msg_addresses
            msg_addresses_type1_string = "по следующему адресу"
            msg_addresses_type2_string = "по приведенному адресу"
        else:
            msg_addresses_string = msg_addresses.replace('\\n', '\n'
                    ).splitlines()
            msg_addresses_string = \
                '\n'.join(list(map(lambda orig_string: "•" + ' ' \
                          + orig_string, msg_addresses_string)))
            msg_addresses_type1_string = "по следующим адресам"
            msg_addresses_type2_string = "по приведенным адресам"

        # Attachments

        if len(glob('attachments/*.jpg')) == 1:
            msg_attachments_type1_string = "приложенной"
            msg_attachments_type2_string = "фотографией"
        elif len(glob('attachments/*.jpg')) > 1:
            msg_attachments_type1_string = "приложенными"
            msg_attachments_type2_string = "фотографиями"

        # Generating message

        with open('templates/trash.txt', 'r') as template:
            msg_body = template.read()
            msg_body = msg_body.format(msg_addresses_type1_string,
                    msg_addresses_string, msg_addresses_type2_string,
                    msg_attachments_type1_string,
                    msg_attachments_type2_string)

    return (msg_subject, msg_body)
