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

from slave.driver import Driver, Command
from slave.types import String, BitSequence
from protocol import BaurProtocol
import time

class BaurDriver(Driver):
    # Handling Base Classes
    def __init__(self, transport, protocol, timer=None):
        super(BaurDriver, self).__init__(transport, protocol)

        assert isinstance(protocol, BaurProtocol)

        if timer is None:
            timer = time
        self._timer = timer

        self.protocol = protocol
        # Commands:

        self.position = Command(  # Command: def __init__(self, query=None, write=None, type_=None, protocol=None):
            'mabs?',  # query
            'mabs',
            String
        )

        self.status = Command((  # Command: def __init__(self, query=None, write=None, type_=None, protocol=None):
            'STAT',  # query
            BitSequence([
                (1, String),  # Service
                (8, String)  # Learn data set
               #,(1, String)  # Power failure battery
            ])
        ))

    def initialize(self, step=4000, acceleration=1, v_start=1, v_end=1):
        self.timer.sleep(0.1)
        self.steps(step)
        self.timer.sleep(0.1)
        self.acc(acceleration)
        self.timer.sleep(0.1)
        self.vstart(v_start)
        self.timer.sleep(0.1)
        self.vend(v_end)
        self.clear()

    def is_connected(self):
        try:
            self.position
            return True
        except:
            return False

    def get_transport(self):
        return self.protocol

    def get_position(self):
        pos = str(self.position)
        length = len(pos)
        return int(pos[5:length])

    def steps(self, value):
        cmd = 'steps', String
        return self._write(cmd, value)

    def xfer(self, value):
        cmd = 'xfer', String
        return self._write(cmd, value)

    def acc(self, value):
        cmd = 'acc', String
        return self._write(cmd, ('{:0>3}').format(value))

    def mvel(self, value):
        cmd = 'mvel', String
        return self._write(cmd, ('{:0>5}').format(value))

    def vstart(self, value):
        cmd = 'vstart', String
        return self._write(cmd, ('{:0>5}').format(value))

    def vend(self, value):
        cmd = 'vend', String
        return self._write(cmd, ('{:0>5}').format(value))

    def pset(self, value):
        cmd = 'pset', String
        return self._write(cmd, value)

    def move_rel(self, value):
        cmd = 'mrel', String
        return self._write(cmd, ('{:0>8}').format(value))

    def reference(self, value=2):
        cmd = 'mref', String
        return self._write(cmd, value)

    def gnum(self, value):
        cmd = 'gnum', String
        return self._write(cmd, value)

    def gden(self, value):
        cmd = 'gden', String
        return self._write(cmd, value)

    def stop(self):
        cmd = 'stop', String
        return self._write(cmd, '')

    def con(self):
        cmd = 'MCON', String
        return self._write(cmd, '')

    def clear(self):
        cmd = 'clre', String
        return self._write(cmd, '')

    def ired(self, value):
        cmd = 'ired', String
        return self._write(cmd, value)

    def move_abs(self, value):
        cmd = 'mabs', String
        return self._write(cmd, value)
