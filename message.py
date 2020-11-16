import pygame
import datetime

pos_ult = 220
font = pygame.font.Font('Silver.ttf', 32)
font_desc = pygame.font.Font('Silver.ttf', 18)


class message:
    def __init__(self, title, msg):
        self.title = title
        self.message = msg
        hour = str(datetime.datetime.now().hour)
        minute = str(datetime.datetime.now().minute)
        second = str(datetime.datetime.now().second)

        if len(hour) == 1:
            hour = "0" + hour
        if len(minute) == 1:
            minute = "0" + minute
        if len(second) == 1:
            second = "0" + second

        self.time_thing = hour + ":" + minute + ":" + second

    def display_message(self, display, mouse_pos, list_of_messages):
        title = font.render(self.title, False, (255, 255, 255))
        message_for_all = font_desc.render(self.message, False, (210, 210, 210))
        time = font_desc.render(self.time_thing, False, (210, 210, 210))
        display.blit(title, (mouse_pos[0] - pos_ult + 10, mouse_pos[1] + (len(list_of_messages) - list_of_messages.index(self) - 1) * 50))
        display.blit(message_for_all, (mouse_pos[0] - pos_ult + 5, mouse_pos[1] + 25 + (len(list_of_messages) - list_of_messages.index(self) - 1) * 50))
        display.blit(time, (mouse_pos[0] - pos_ult + 150, mouse_pos[1] + (len(list_of_messages) - list_of_messages.index(self) - 1) * 50))

