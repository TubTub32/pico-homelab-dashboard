class LcdApi:
    LCD_CLR = 0x01
    LCD_HOME = 0x02
    LCD_ENTRY_MODE = 0x04
    LCD_DISPLAY_CTRL = 0x08
    LCD_SHIFT = 0x10
    LCD_FUNCTION = 0x20
    LCD_CGRAM = 0x40
    LCD_DDRAM = 0x80

    LCD_ENTRY_RIGHT = 0x00
    LCD_ENTRY_LEFT = 0x02
    LCD_ENTRY_SHIFT_INC = 0x01
    LCD_ENTRY_SHIFT_DEC = 0x00

    LCD_DISPLAY_ON = 0x04
    LCD_DISPLAY_OFF = 0x00
    LCD_CURSOR_ON = 0x02
    LCD_CURSOR_OFF = 0x00
    LCD_BLINK_ON = 0x01
    LCD_BLINK_OFF = 0x00

    LCD_8BIT_MODE = 0x10
    LCD_4BIT_MODE = 0x00
    LCD_2_LINE = 0x08
    LCD_1_LINE = 0x00
    LCD_5x10_DOTS = 0x04
    LCD_5x8_DOTS = 0x00

    def __init__(self, num_lines, num_columns):
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.cursor_x = 0
        self.cursor_y = 0

    def clear(self):
        self.hal_write_command(self.LCD_CLR)
        self.hal_write_command(self.LCD_HOME)

    def move_to(self, cursor_x, cursor_y):
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y
        addr = cursor_x & 0x3F
        if cursor_y & 1:
            addr += 0x40
        self.hal_write_command(self.LCD_DDRAM | addr)

    def putstr(self, string):
        for char in string:
            if char == '\n':
                self.cursor_y += 1
                if self.cursor_y >= self.num_lines:
                    self.cursor_y = 0
                self.move_to(0, self.cursor_y)
            else:
                self.hal_write_data(ord(char))
                self.cursor_x += 1
                if self.cursor_x >= self.num_columns:
                    self.cursor_x = 0
                    self.cursor_y += 1
                    if self.cursor_y >= self.num_lines:
                        self.cursor_y = 0
                    self.move_to(self.cursor_x, self.cursor_y)

    def hal_write_command(self, cmd):
        raise NotImplementedError

    def hal_write_data(self, data):
        raise NotImplementedError

