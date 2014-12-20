import pygame
import gui

class SceneManager(object):
    def __init__(self, screen):
        self.screen = screen

        self.scenes = {}

        self.active_scene = None

        self.running = True

    def add_scene(self, scene):
        self.scenes[scene.name] = scene

    def activate_scene(self, scene, data=None):
        self.active_scene = self.scenes[scene]
        self.active_scene.activate(data)

    def update(self):
        if self.running and self.active_scene:
            self.active_scene.doupdate()

    def render(self):
        if self.running and self.active_scene:
            self.active_scene.dorender()

class Scene(object):
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.name = 'default'

        self.event_handler = gui.EventHandler()
        self.event_handler.add_binding('quit', self.quit)

        self.setup()

        self.scene_manager.add_scene(self)

    def quit(self):
        self.scene_manager.running = False

    def setup(self):
        return

    def activate(self, data):
        return

    def dorender(self):
        self.render()

    def doupdate(self):
        self.event_handler.update()
        self.update()

    def render(self):
        return

    def update(self):
        return
