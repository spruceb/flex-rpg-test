from core.controller import event_dispatcher
import time
import pygame
from pygame import locals
import cProfile
main = event_dispatcher.Dispatcher()
cProfile.run("while True: main.update()")

    #main.display.cursor_update()
    #pygame.display.update()