from protocol import BaurProtocol
from driver import BaurDriver
from e21_util.transport import Serial
from e21_util.ports import Ports
from e21_util.log import get_sputter_logger

class BaurFactory:


    def create_gun(self, device=None, logger=None):

        if logger is None:
            logger = get_sputter_logger('Motor Gun', 'motor_gun.log')

        if device is None:
            device = Ports().get_port(Ports.DEVICE_MOTOR_C)

        gun = BaurDriver(Serial(device, 9600, 8, 'N', 1, 1), BaurProtocol(logger))
        gun.initialize(4000, 1, 1, 6)  # steps, acc, vstart, vend
        return gun

    def create_z_stage(self):

        if logger is None:
            logger = get_sputter_logger('Motor Z', 'motor_z.log')

        if device is None:
            device = Ports().get_port(Ports.DEVICE_MOTOR_Z)

        z_motor = BaurDriver(Serial(device, 9600, 8, 'N', 1, 1), BaurProtocol(logger))
        z_motor.initialize(4000, 10, 30, 30)
        return z_motor

    def create_x_stage(self):

        if logger is None:
            logger = get_sputter_logger('Motor X', 'motor_x.log')

        if device is None:
            device = Ports().get_port(Ports.DEVICE_MOTOR_X)

        x_motor = BaurDriver(Serial(device, 9600, 8, 'N', 1, 1), BaurProtocol(logger))
        x_motor.initialize(4000, 1, 1, 1)
        return z_motor