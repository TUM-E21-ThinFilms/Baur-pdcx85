# Copyright (C) 2016, see AUTHORS.md
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from slave.protocol import Protocol
import logging

class BaurProtocol(Protocol):
    def __init__(self, logger, echo=None, msg_term='\r', resp_data_sep='=', resp_term='\r', encoding='ascii', ):
        self.echo = echo
        self.resp_data_sep = resp_data_sep
        self.msg_term = msg_term
        self.resp_term = resp_term
        self.encoding = encoding

        self.logger = logger

    def set_logger(self, logger):
        self.logger = logger
        return self

    def create_message(self, header, *data):
        msg = []
        if not self.echo:
            msg.append('')
        msg.append(header)
        msg.extend(data)
        msg.append(self.msg_term)
        return ''.join(msg).encode(self.encoding)

    def parse_response(self, response, header):
        # response = response.decode(self.encoding)
        if not self.echo:
            pass
        else:
            if not response.startswith(header[0]):
                raise ValueError('Response header mismatch')

            response = response[len(header):]  # response starts with header + '='
        return [response]

    def query(self, transport, header, *data):
        message = self.create_message(header, *data)
        self.logger.debug('Sending query: %s', repr(message))
        with transport:
            transport.write(message)
            response = transport.read_until(self.resp_term.encode(self.encoding))
        self.logger.debug('Received response: %s', repr(response))
        return self.parse_response(response, header)

    def write(self, transport, header, *data):
        message = self.create_message(header, *data)
        self.logger.debug('Writing: %s', repr(message))
        with transport:
            transport.write(message)