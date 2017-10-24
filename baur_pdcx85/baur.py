from __future__ import (absolute_import, division, print_function, unicode_literals)
from slave.driver import Driver, Command
from slave.protocol import Protocol
from slave.types import Integer, String, Register, Enum, Mapping, Float, Percent, Register, BitSequence
from slave.transport import Serial, SimulatedTransport
import logging
import time

from future.builtins import *
from slave.driver import _to_instance
import itertools

#logger = logging.getLogger(__name__)
#logger.addHandler(logging.NullHandler())
#logging.basicConfig(filename='log.txt', filemode='w', level=logging.DEBUG)

logger = logging.getLogger('Baur Motor')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = logging.FileHandler('Motor Driver.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

class BaurProtocol(Protocol):
    def __init__(self, echo = None, msg_term='\r', resp_data_sep='=', resp_term='\r', encoding='ascii'):
        self.echo = echo
        self.resp_data_sep=resp_data_sep
        self.msg_term = msg_term
        self.resp_term = resp_term
        self.encoding = encoding
        self.name = 'No Name set'
        
    def setName(self, name):
        self.name = name
    
    def create_message(self, header, *data):
        msg = []
        if not self.echo:
            msg.append('')
        msg.append(header)
        msg.extend(data)
        msg.append(self.msg_term)
        return ''.join(msg).encode(self.encoding)    

    def parse_response(self, response, header):
        #response = response.decode(self.encoding)
        if not self.echo:
            pass
        else:
            if not response.startswith(header[0]):
                raise ValueError('Response header mismatch')
            response = response[len(header):] # response starts with header + '='
        return [response]
    
    def query(self, transport, header, *data):
        message = self.create_message(header, *data)
        logger.debug(self.name + ': query: %s', repr(message))
        with transport:
            transport.write(message)
            response = transport.read_until(self.resp_term.encode(self.encoding))
        logger.debug(self.name + ': response: %s', repr(response))
        return self.parse_response(response,header)

    def write(self, transport, header, *data):
        message = self.create_message(header, *data)
        logger.debug(self.name + ': write: %s', repr(message))
        with transport:
            transport.write(message)

class BaurMotor(Driver):
    
    # Handling Base Classes
    def __init__(self, transport, protocol=None):
        if protocol == None:
	   protocol = BaurProtocol()
             
        super(BaurMotor,self).__init__(transport,protocol)        
                
        self.protocol = protocol
        # Commands:
        
        self.position = Command( # Command: def __init__(self, query=None, write=None, type_=None, protocol=None):
            'mabs?', #query
            'mabs',
            String
        )
        
        self.status = Command(( # Command: def __init__(self, query=None, write=None, type_=None, protocol=None):
            'STAT', #query
           BitSequence([
                (1, String),              # Service  
                (8, String), # Learn data set
                (1, String) # Power failure battery
                ])
            ))
            
    def initialize(self, step=4000, accel=1, velstart=1, velend=1):
        time.sleep(0.5)
        self.steps(step)
        time.sleep(0.5)
        self.acc(accel)
        time.sleep(0.5)
        self.vstart(velstart)
        time.sleep(0.5)
        self.vend(velend)
        self.clear()
    
    def isConnected(self):
        self.position
        return True;        
        
    def getTransport(self):
        return self.protocol        
    
    # Functions: 
    def steps(self,value):
        cmd = 'steps', String
        return self._write(cmd,value)
    
    def xfer(self,value):
        cmd = 'xfer', String
        return self._write(cmd,value)
    
    def acc(self,value):
        cmd = 'acc', String
        return self._write(cmd,('{:0>3}').format(value))

    def mvel(self,value):
        cmd = 'mvel', String
        return self._write(cmd,('{:0>5}').format(value))    

    def vstart(self,value):
        cmd = 'vstart', String
        return self._write(cmd,('{:0>5}').format(value))

    def vend(self,value):
        cmd = 'vend', String
        return self._write(cmd,('{:0>5}').format(value))

    def pset(self, value):
        cmd = 'pset', String
        return self._write(cmd,value)    
    
    def move_rel(self,value):
        cmd = 'mrel', String
        return self._write(cmd,('{:0>8}').format(value))
    
    def cannon_reference(self,value=2):
        cmd = 'mref', String
        return self._write(cmd,value)

    def gnum(self,value):
        cmd = 'gnum', String
        return self._write(cmd,value)
    
    def gden(self,value):
        cmd = 'gden', String
        return self._write(cmd,value)
    
    def stop(self):
        cmd = 'stop', String
        return self._write(cmd,'')
    
    def con(self):
        cmd = 'MCON', String
        return self._write(cmd,'')

    def clear(self): # delete all errors
        cmd = 'clre', String
        return self._write(cmd,'') # First digit: Gauge 1; Second digit: Gauge 2; '0': No change, '1': Turn off, '2': Turn on

    def ired(self,value): # delete all errors
        cmd = 'ired', String
        return self._write(cmd,value) # First digit: Gauge 1; Second digit: Gauge 2; '0': No change, '1': Turn off, '2': Turn on

    def move_abs (self,value):
        cmd = 'mabs', String
        return self._write(cmd,value)
    
    def cannon_move_down(self,value=90): # move degrees down
        position_change = int((903/90) * value) # 900 : steps for 90 degrees
        actual_position=int(self.position[5:])
        time.sleep(1)
        return self.move_abs(actual_position-position_change)

    def cannon_move_up(self,value=90): # move degrees up
        position_change = int((903/90) * value) # 900 : steps for 90 degrees
        actual_position=int(self.position[5:])
        time.sleep(1)
        return self.move_abs(actual_position+position_change)
    
Cannon=BaurMotor(Serial('/dev/ttyMXUSB15', 9600, 8,'N',1,1))
Cannon.getTransport().setName('Cannon')
Cannon.initialize(4000, 1, 1, 2) # steps, acc, vstart, vend
                 
D_stage=BaurMotor(Serial('/dev/ttyMXUSB9', 9600, 8,'N',1,1))
D_stage.getTransport().setName('D_stage')
D_stage.initialize(4000, 1, 1, 1)

X_stage=BaurMotor(Serial('/dev/ttyMXUSB11', 9600, 8,'N',1,1))
X_stage.getTransport().setName('X_stage')
X_stage.initialize(4000, 1, 1, 1)

Z_stage=BaurMotor(Serial('/dev/ttyMXUSB13', 9600, 8,'N',1,1))
Z_stage.getTransport().setName('Z_stage')
Z_stage.initialize(4000, 1, 1, 1)
