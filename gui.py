import pygame
from pygame.locals import *


key_mappings = {
    K_UP: 'up',
    K_DOWN: 'down',
    K_LEFT: 'left',
    K_RIGHT: 'right',
    K_RETURN: 'enter',
    K_ESCAPE: 'esc',
    K_SPACE: 'space',
    K_TAB: 'tab',
    K_SCROLLOCK: 'scroll_lock',
    K_SYSREQ: 'print_screen',
    K_BREAK: 'break',
    K_DELETE: 'delete',
    K_BACKSPACE: 'back_space',
    K_CAPSLOCK: 'caps_lock',
    K_CLEAR: 'clear',
    K_NUMLOCK: 'num_lock',
    
    K_F1: 'F1',
    K_F2: 'F2',
    K_F3: 'F3',
    K_F4: 'F4',
    K_F5: 'F5',
    K_F6: 'F6',
    K_F7: 'F7',
    K_F8: 'F8',
    K_F9: 'F9',
    K_F10: 'F10',
    K_F11: 'F11',
    K_F12: 'F12',
    K_F13: 'F13',
    K_F14: 'F14',
    K_F15: 'F15',

    K_HELP: 'help',
    K_HOME: 'home',
    K_END: 'end',
    K_INSERT: 'insert',
    K_PRINT: 'print',
    K_PAGEUP: 'page_up',
    K_PAGEDOWN: 'page_down',
    K_FIRST: 'first',
    K_LAST: 'last',

    K_KP0: 'key_pad_0',
    K_KP1: 'key_pad_1',
    K_KP2: 'key_pad_2',
    K_KP3: 'key_pad_3',
    K_KP4: 'key_pad_4',
    K_KP5: 'key_pad_5',
    K_KP6: 'key_pad_6',
    K_KP7: 'key_pad_7',
    K_KP8: 'key_pad_8',
    K_KP9: 'key_pad_9',

    K_KP_DIVIDE: 'key_pad_divide',
    K_KP_ENTER: 'key_pad_enter',
    K_KP_EQUALS: 'key_pad_equals',
    K_KP_MINUS: 'key_pad_minus',
    K_KP_MULTIPLY: 'key_pad_multiply',
    K_KP_PERIOD: 'key_pad_period',
    K_KP_PLUS: 'key_pad_plus',

    K_LALT: 'left_alt',
    K_RALT: 'right_alt',
    K_LCTRL: 'left_control',
    K_RCTRL: 'right_control',
    K_LSUPER: 'left_super',
    K_RSUPER: 'right_super',
    K_LSHIFT: 'left_shift',
    K_RSHIFT: 'right_shift',
    K_LMETA: 'left_meta',
    K_RMETA: 'right_meta',
    }

pseudo_key_mappings = {
    'left_alt': 'p_alt',
    'right_alt': 'p_alt',
    'left_control': 'p_control',
    'right_control': 'p_control',
    'left_super': 'p_super',
    'right_super': 'p_super',
    'left_shift': 'p_shift',
    'right_shift': 'p_shift',
    'left_meta': 'p_meta',
    'right_meta': 'p_meta',
    'enter': 'p_enter',
    'key_pad_enter': 'p_enter',
    }

char_kp_mappings = {
    K_KP0: '0',
    K_KP1: '1',
    K_KP2: '2',
    K_KP3: '3',
    K_KP4: '4',
    K_KP5: '5',
    K_KP6: '6',
    K_KP7: '7',
    K_KP8: '8',
    K_KP9: '9',

    K_KP_DIVIDE: '/',
    K_KP_EQUALS: '=',
    K_KP_MINUS: '-',
    K_KP_MULTIPLY: '*',
    K_KP_PERIOD: '.',
    K_KP_PLUS: '+',
    }

char_shift_mappings = {
    '`': '~',
    '1': '!',
    '2': '@',
    '3': '#',
    '4': '$',
    '5': '%',
    '6': '^',
    '7': '&',
    '8': '*',
    '9': '(',
    '0': ')',
    '-': '_',
    '=': '+',

    '[': '{',
    ']': '}',
    '\\': '|',
    ';': ':',
    "'": '"',
    ',': '<',
    '.': '>',
    '/': '?',
    }

    

class EventHandler(object):
    def __init__(self):

        self.key_down = {}

        self.chars = ''

        self.caps_on = False #TODO: find initial state of caps lock

        self.events = []

        self.mouse_x = 0
        self.mouse_y = 0

        self.bindings = {}

    def add_binding(self, event, function):
        if not event in self.bindings:
            self.bindings[event] = []

        self.bindings[event].append(function)

    def call_binding(self, event):
        if event in self.bindings:
            for func in self.bindings[event]:
                func()

    def get_key(self, key):
        if key in self.key_down:
            return self.key_down[key]
        return False

    def get_chars(self):
        return self.chars

    def convert_char(self, char):
        if len(char) != 1:
            return ''
        caps = self.caps_on
        shift = 'p_shift' in self.key_down and self.key_down['p_shift']

        if char in char_shift_mappings:
            if shift:
                return char_shift_mappings[char]
            else:
                return char

        if caps and shift:
            shift = False
        elif caps:
            shift = True

        if shift:
            return char.upper()
        return char

    def update(self):
        self.events = []
        self.chars = ""

        for event in pygame.event.get():
            if event.type == QUIT:
                self.events.append('quit')
                self.call_binding('quit')

            if event.type == KEYDOWN:
                if event.key == K_CAPSLOCK:
                    self.caps = not self.caps
                if event.key in key_mappings:
                    key = key_mappings[event.key]
                try:
                    key = chr(event.key)
                except:
                    print 'unknown key:', event.key

                if key in pseudo_key_mappings:
                    p_key = pseudo_key_mappings[key]
                else:
                    p_key = None

                self.key_down[key] = True
                self.events.append(key)
                if p_key:
                    self.key_down[p_key] = True
                    self.events.append(p_key)
                self.call_binding(key)
                self.call_binding(p_key)

            if event.type == KEYUP:
                if event.key in key_mappings:
                    key = key_mappings[event.key]
                elif event.unicode:
                    key = event.unicode
                else:
                    print 'unknown key'

                if key in pseudo_key_mappings:
                    p_key = pseudo_key_mappings[key]
                else:
                    p_key = None

                self.key_down[key] = False
                if p_key:
                    self.key_down[p_key] = False

        for i in self.key_down:
            self.chars += self.convert_char(i)

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()


class UIGroup(object):
    def __init__(self, event_handler):
        self.event_handler = event_handler

        self.elements = []

        self.focus = None

    def add_element(self, element):
        self.elements.append(element)
        if not self.focus:
            self.focus = element
            element.focus = True

    def get_element_by_name(self, name):
        for i in elements:
            if i.name == name:
                return element
        return None

    def set_focus(self, element, focus):
        if focus and self.focus==element:
            pass #nothing changed
        elif focus:
            for i in self.elements:
                if not i==element:
                    i.focus = False
            self.focus = element
        elif self.focus==element:
            self.focus = None

    def go_next(self):
        self.focus.focus = False
        if self.focus:
            index = self.elements.index(self.focus) + 1
        else:
            index = 0

        if index >= len(self.elements):
            index = 0

        self.focus = self.elements[index]
        self.focus.focus = True
        if not self.focus.focusable:
            return self.go_next()
        return self.focus

    def go_prev(self):
        self.focus.focus = False
        if self.focus:
            index = self.elements.index(self.focus) - 1
        else:
            index = 0

        if index < 0:
            index = len(self.elements)-1

        self.focus = self.elements[index]
        self.focus.focus = True
        if not self.focus.focusable:
            return self.go_prev()
        return self.focus

    def update(self):
        if self.focus:
            self.focus.handle_events(self.event_handler)

    def render(self, screen):
        for i in self.elements:
            if not i==self.focus:
                i.render(screen)

        if self.focus:
            self.focus.render(screen)

class UIElement(object):
    def __init__(self, group=None, name='default', visible=True, focus=False, focusable=True, callback=None, **kwargs):
        self.group = group
        self.name = name
        self.focus = focus
        self.focusable = focusable
        self.visible = visible
        self.callback = callback

        self.setup(**kwargs)
        if self.group:
            self.group.add_element(self)

    def setup(self):
        pass

    def set_focus(self, focus):
        self.focus = focus
        if self.group:
            self.group.set_focus(self, focus)

    def call(self):
        if self.callback:
            self.callback()

    def handle_events(self, event_handler):
        if self.focus:
            if self.group:
                if 'down' in event_handler.events:
                    self.group.go_next()
                if 'up' in event_handler.events:
                    self.group.go_prev()
            if 'enter' in event_handler.events:
                self.call()

    def render(self, screen):
        pass

    def get_next(self):
        if not self.group:
            return None
        index = self.group.elements.index(self) + 1
        if index >= len(self.group.elements):
            index = 0

        return self.group.elements[index]

    def get_prev(self):
        if not self.group:
            return None
        index = self.group.elements.index(self) - 1
        if index < 0:
            index = len(self.group.elements)-1

        return self.group.elements[index]

class TextSelect(UIElement):
    def setup(self, text='Some Text', position=(0,0), antialias=False,
              focus_color=(0,0,0), focus_background=(255,255,255), focus_font=None,
              focus_size=16, focus_outline=(125,125,125), focus_outline_width=1,

              unfocus_color=(0,0,0), unfocus_background=(255,255,255), unfocus_font=None,
              unfocus_size=16, unfocus_outline=None, unfocus_outline_width=0):

        self.text = text
        self.position = position
        self.antialias = antialias

        self.focus_color = focus_color
        self.focus_background = focus_background
        self.focus_font = focus_font
        self.focus_size = focus_size
        self.focus_outline = focus_outline
        self.focus_outline_width = focus_outline_width

        self.unfocus_color = unfocus_color
        self.unfocus_background = unfocus_background
        self.unfocus_font = unfocus_font
        self.unfocus_size = unfocus_size
        self.unfocus_outline = unfocus_outline
        self.unfocus_outline_width = unfocus_outline_width

        self.__focus_font = pygame.font.Font(self.focus_font, self.focus_size)
        self.__focus_font_details = (self.focus_font, self.focus_size)
        self.__unfocus_font = pygame.font.Font(self.unfocus_font, self.unfocus_size)
        self.__unfocus_font_details = (self.unfocus_font, self.unfocus_size)

    def render(self, screen):
        if self.focus:
            if not (self.focus_font,self.focus_size) == self.__focus_font_details:
                self.__focus_font = pygame.font.Font(self.focus_font, self.focus_size)
                self.__focus_font_details = (self.focus_font, self.focus_size)

            if self.focus_background:
                render = self.__focus_font.render(self.text, self.antialias,
                                              self.focus_color, self.focus_background)
            else:
                render = self.__focus_font.render(self.text,self.antialias,self.focus_color)
            screen.blit(render, self.position)

            if self.focus_outline and self.focus_outline_width:
                rect = render.get_rect()
                rect.inflate_ip(self.focus_outline_width*2, self.focus_outline_width*2)
                rect.topleft = (self.position[0]-self.focus_outline_width,
                                self.position[1]-self.focus_outline_width)
                pygame.draw.rect(screen, self.focus_outline, rect, self.focus_outline_width)

        else:
            if not (self.unfocus_font,self.unfocus_size) == self.__unfocus_font_details:
                self.__unfocus_font = pygame.font.Font(self.unfocus_font, self.unfocus_size)
                self.__unfocus_font_details = (self.unfocus_font, self.unfocus_size)

            if self.unfocus_background:
                render = self.__unfocus_font.render(self.text, self.antialias,
                                              self.unfocus_color, self.unfocus_background)
            else:
                render = self.__unfocus_font.render(self.text,self.antialias,self.unfocus_color)
            screen.blit(render, self.position)

            if self.unfocus_outline and self.unfocus_outline_width:
                rect = render.get_rect()
                rect.inflate_ip(self.unfocus_outline_width*2, self.unfocus_outline_width*2)
                rect.topleft = (self.position[0]-self.unfocus_outline_width,
                                self.position[1]-self.unfocus_outline_width)
                pygame.draw.rect(screen, self.unfocus_outline, rect, self.unfocus_outline_width)
        
