from slave.driver import Driver, Command
from slave.types import String, BitSequence
from protocol import BaurProtocol
import time

class BaurDriver(Driver):
    # Handling Base Classes
    def __init__(self, transport, timer=None, protocol=None):
        if protocol is None:
            protocol = BaurProtocol()

        if timer is None:
            timer = time

        self.timer = timer

        super(BaurDriver, self).__init__(transport, protocol)

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

    def initialize(self, step=4000, accel=1, velstart=1, velend=1):
        self.timer.sleep(0.5)
        self.steps(step)
        self.timer.sleep(0.5)
        self.acc(accel)
        self.timer.sleep(0.5)
        self.vstart(velstart)
        self.timer.sleep(0.5)
        self.vend(velend)
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