#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# This file is part of Tatyana.
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
