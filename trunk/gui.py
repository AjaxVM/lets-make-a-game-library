import pygame
from pygame.locals import *

class EventHandler(object):
    def __init__(self):

        self.key_down = {
            'up': False,
            'down': False,
            'left': False,
            'right': False,
            'enter': False,
            'esc': False
            }

        self.events = []

        self.mouse_x = 0

        self.bindings = {
            'up': [],
            'down': [],
            'left': [],
            'right': [],
            'enter': [],
            'esc': [],
            'quit': [],
            }

    def add_binding(self, event, function):
        self.bindings[event].append(function)

    def call_binding(self, event):
        for func in self.bindings[event]:
            func()

    def update(self):
        self.events = []
        for event in pygame.event.get():
            if event.type == QUIT:
                self.events.append('quit')
                self.call_binding('quit')

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.key_down['left'] = True
                    self.events.append('left')
                    self.call_binding('left')
                if event.key == K_RIGHT:
                    self.key_down['right'] = True
                    self.events.append('right')
                    self.call_binding('right')
                if event.key == K_UP:
                    self.key_down['up'] = True
                    self.events.append('up')
                    self.call_binding('up')
                if event.key == K_DOWN:
                    self.key_down['down'] = True
                    self.events.append('down')
                    self.call_binding('down')
                if event.key == K_RETURN:
                    self.key_down['enter'] = True
                    self.events.append('enter')
                    self.call_binding('enter')
                if event.key == K_ESCAPE:
                    self.key_down['esc'] = True
                    self.events.append('esc')
                    self.call_binding('esc')

            if event.type == KEYUP:
                if event.key == K_LEFT:
                    self.key_down['left'] = False
                if event.key == K_RIGHT:
                    self.key_down['right'] = False
                if event.key == K_UP:
                    self.key_down['up'] = False
                if event.key == K_DOWN:
                    self.key_down['down'] = False
                if event.key == K_RETURN:
                    self.key_down['enter'] = False
                if event.key == K_ESCAPE:
                    self.key_down['esc'] = False

        self.mouse_x = pygame.mouse.get_pos()[0]


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
        
