#!/usr/bin/env python3

import pygame, os, sys, math

os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

def get_path(relative_path):
    if getattr(sys, 'frozen', False):
        # ./binario
        base_path = os.path.dirname(sys.executable)
    else:
        # python .py
        base_path = os.path.dirname(os.path.abspath(__file__))
        
    return os.path.join(base_path, relative_path)

class Stick:
    def __init__(self, pos, image):
        self.pos = pos
        self.image = image
        self.offset = 32
        self.ratio_x = 0
        self.ratio_y = 0

    def render(self, surf):

        length = math.hypot(self.ratio_x, self.ratio_y)

        ratio_x = self.ratio_x / length if length > 1 else self.ratio_x
        ratio_y = self.ratio_y / length if length > 1 else self.ratio_y

        pos = [self.pos[0] + self.offset * ratio_x, self.pos[1] + self.offset * ratio_y]
        surf.blit(self.image, pos)

class App:
    def __init__(self):

        pygame.init()
        pygame.display.set_mode(flags=pygame.HIDDEN)
        self.app_name = "Joystick Viewer"
        pygame.display.set_caption(self.app_name)
        icon = self.load_image("data/images/icon.png")
        pygame.display.set_icon(icon)

        self.joystick_image = self.load_image("data/images/joystick.png")
        self.joystick_w, self.joystick_h = self.joystick_image.get_size()
        self.display = pygame.display.set_mode((self.joystick_w, self.joystick_h))
        
        self.clock = pygame.time.Clock()
        self.running = True

        self.light_on = self.load_image("data/images/on.png")

        buttons = ["cross", "circle", "triangle", "square",
                   "down", "right", "up", "left",
                   "l1", "l2", "l3", "r1", "r2", "r3",
                   "select", "start"]
        
        self.buttons = {}
        for button in buttons:
            image = self.load_image("data/images/" + button + ".png")
            self.buttons[button] = [False, image]

        LEFT_STICK = (213, 333)
        RIGHT_STICK = (472, 333)
        stick_image = self.load_image("data/images/stick.png")

        self.left_stick = Stick(LEFT_STICK, stick_image.copy())
        self.right_stick = Stick(RIGHT_STICK, stick_image.copy())

        self.joystick = None     
        self.joystick_name = ""
        
        self.notify = False
        self.first_time_connection = True 

    def load_image(self, path):
        return pygame.image.load(get_path(path)).convert_alpha()

    def get_type(self):

        # ps2
        if self.joystick_name == "SHANWAN Android Gamepad":
            self.button_event = {
                0:  "cross",
                1:  "circle",
                2:  "",
                3:  "square",
                4:  "triangle",
                5:  "",
                6:  "l1",
                7:  "r1",
                8:  "l2",
                9:  "r2",
                10:  "select",
                11:  "start",
                12:  "",
                13:  "l3",
                14:  "r3",
            }

            self.axis_event = {
                "left_x":       0, 
                "left_y":       1, 
                "right_x":      2, 
                "right_y":      3, 
            }

        # ps4
        elif self.joystick_name == "Sony Interactive Entertainment Wireless Controller":
            self.button_event = {
                0:  "cross",
                1:  "circle",
                2:  "triangle",
                3:  "square",
                4:  "l1",
                5:  "r1",
                6:  "l2",
                7:  "r2",
                8:  "select",
                9:  "start",
                10:  "",
                11:  "l3",
                12:  "r3",
                13:  "",
                14:  "",
            }

            self.axis_event = {
                "left_x":       0, 
                "left_y":       1, 
                "right_x":      3, 
                "right_y":      4, 
            }

    def run(self):
        
        while self.running:

            for event in pygame.event.get():

                if event.type == pygame.JOYDEVICEADDED:
                    self.joystick = pygame.joystick.Joystick(event.device_index)
                    self.joystick_name = self.joystick.get_name()
                    self.get_type()
                    
                    if self.notify:
                        if not self.first_time_connection:
                            # send notification
                            pass
                        else: 
                            self.first_time_connection = False
                
                if event.type == pygame.JOYDEVICEREMOVED:
                    
                    if self.notify:
                        # send notification
                        pass
                           
                    self.joystick = None
                    self.joystick_name = ""
                    

                if event.type == pygame.JOYHATMOTION:
                    
                    self.buttons["left"][0] = event.value[0] == -1
                    self.buttons["right"][0] = event.value[0] == 1
                    self.buttons["down"][0] = event.value[1] == -1
                    self.buttons["up"][0] = event.value[1] == 1
                    
                if event.type == pygame.JOYBUTTONDOWN:
                    if self.button_event[event.button] in self.buttons.keys():
                        self.buttons[self.button_event[event.button]][0] = True

                if event.type == pygame.JOYBUTTONUP:
                    if self.button_event[event.button] in self.buttons.keys():
                        self.buttons[self.button_event[event.button]][0] = False

                if event.type == pygame.JOYAXISMOTION:

                    # left stick
                    if event.axis == self.axis_event["left_x"]:
                        self.left_stick.ratio_x = int(event.value * 100)/100

                    if event.axis == self.axis_event["left_y"]:
                        self.left_stick.ratio_y = int(event.value * 100)/100

                    # right stick
                    if event.axis == self.axis_event["right_x"]:
                        self.right_stick.ratio_x = int(event.value * 100)/100
                    
                    if event.axis == self.axis_event["right_y"]:
                        self.right_stick.ratio_y = int(event.value * 100)/100


                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update()
            self.render()

    def update(self):
        self.clock.tick(30)
        pygame.display.flip()
    
    def render(self):
        self.display.fill((0,0,0,0))

        self.display.blit(self.joystick_image, (0,0))

        if self.joystick != None:
            self.display.blit(self.light_on, (0,0))

            for pressed, button_image in self.buttons.values():
                if pressed:
                    self.display.blit(button_image, (0,0))

        self.left_stick.render(self.display)
        self.right_stick.render(self.display)

if __name__ == "__main__":
    App().run()