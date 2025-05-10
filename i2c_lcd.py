from lcd_api import LcdApi
from machine import I2C
import utime

class I2cLcd(LcdApi):
    I2C_ADDR = 0x27  # You may need to change this to 0x3F depending on your module
    LCD_WIDTH = 16
    LCD_HEIGHT = 2

    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.backlight = 0x08
        self.init_lcd()
        super().__init__(num_lines, num_columns)

    def init_lcd(self):
        utime.sleep_ms(50)
        self.write_init_nibble(0x30)
        utime.sleep_ms(5)
        self.write_init_nibble(0x30)
        utime.sleep_us(100)
        self.write_init_nibble(0x30)
        self.write_init_nibble(0x20)
        self.hal_write_command(0x28)
        self.hal_write_command(0x08)
        self.hal_write_command(0x01)
        utime.sleep_ms(2)
        self.hal_write_command(0x06)
        self.hal_write_command(0x0C)

    def write_init_nibble(self, nibble):
        self.i2c.writeto(self.i2c_addr, bytearray([(nibble | self.backlight) & 0xF0 | 0x04]))
        self.i2c.writeto(self.i2c_addr, bytearray([(nibble | self.backlight) & 0xF0]))

    def hal_write_command(self, cmd):
        self.send(cmd, 0)

    def hal_write_data(self, data):
        self.send(data, 1)

    def send(self, value, mode):
        high = value & 0xF0
        low = (value << 4) & 0xF0
        self.write_byte(high | mode << 0)
        self.write_byte(low | mode << 0)

    def write_byte(self, val):
        self.i2c.writeto(self.i2c_addr, bytearray([val | self.backlight | 0x04]))
        self.i2c.writeto(self.i2c_addr, bytearray([val | self.backlight]))

