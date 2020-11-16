#!venv\\Scripts\\python.exe
import re
import sys
import threading

import pygame
import win32api
import win32con
import win32gui
import os
import send
import status_read
import time
from win32gui import GetWindowText, GetForegroundWindow
import math

pygame.init()

import message

last_place = (-1, -1)
list_of_messages = []
last_win_name = ""

timer_for_disappear = time.time()
mouse_cursor = pygame.image.load("mouse.png")
mouse_cursor = pygame.transform.scale(mouse_cursor, (18, 30))

visual_mode = True
last_tuppler = []
tupler = (0, 0)

on_ = 0

code = ""

trigger_save = True
def add_to(add, index):  # Use Time - Rooms's Joined - Total Mouse Distance
    global trigger_save
    trigger_save = False
    filer = open("C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\MouseData\\save.txt", "r")
    lister = filer.readlines()
    filer.close()
    lister[index] = str(int(lister[index]) + add) + "\n"

    filer = open("C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\MouseData\\save.txt", "w")
    for x in lister:
        filer.write(x)
    filer.close()
    trigger_save = True


def main_picker(screen, fuchsia):
    clock = pygame.time.Clock()
    try:
        os.mkdir("C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\MouseData")
    except FileExistsError:
        print("File Already Exists")

    font = pygame.font.Font('Silver.ttf', 32)
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
    input_box = pygame.Rect(win32api.GetSystemMetrics(0)/2 - 160, win32api.GetSystemMetrics(1)/2 - 25, 320, 50)
    border_box = pygame.Rect(input_box.x, input_box.y, 320, 50)

    color = (60, 60, 60)
    text = ''
    done = False

    if not os.path.exists("C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\MouseData\\save.txt"):
        save_file = open("C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\MouseData\\save.txt", "w")
        save_file.write("0\n0\n0")  # Use Time - Rooms's Joined - Total Mouse Distance
        save_file.close()

    save_file = open("C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\MouseData\\save.txt", "r")
    liner = save_file.readlines()  # Use Time - Rooms's Joined - Total Mouse Distance
    save_file.close()

    try:
        hour = 0
        minute = 0
        second = int(liner[0])
        while second >= 60:
            minute += 1
            second -= 60
        while minute >= 60:
            hour += 1
            minute -= 60
        second_ = str(second)
        minute_ = str(minute)
        hour_ = str(hour)
        if second <= 9:
            second_ = "0" + str(second)
        if minute <= 9:
            minute_ = "0" + str(minute)
        if hour <= 9:
            hour_ = "0" + str(hour)
        liner[0] = hour_ + ":" + minute_ + ":" + second_
    except IndexError:
        liner.append("0")
        liner.append("0")
        liner.append("0")
        save_file = open("C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\MouseData\\save.txt", "w")
        save_file.write("0\n0\n0")  # Use Time - Rooms's Joined - Total Mouse Distance
        save_file.close()

    clicked = False
    while not done:
        screen.fill(fuchsia)
        tex__ = screen.blit(render_with_outline("Server: " + send.all_servers[send.on_server], font), (win32api.GetSystemMetrics(0) - 200, win32api.GetSystemMetrics(1) - 70))

        for event in pygame.event.get():
            if pygame.mouse.get_pressed(3)[0] and not clicked:
                clicked = True
                if tex__.collidepoint(win32gui.GetCursorPos()):
                    if not send.on_server + 1 > len(send.all_servers) - 1:
                        send.on_server += 1
                    else:
                        send.on_server = 0
            elif not pygame.mouse.get_pressed(3)[0] and clicked:
                clicked = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif len(text) < 5:
                    text += event.unicode
            elif event.type == pygame.QUIT:
                sys.exit()

        pygame.draw.rect(screen, color, input_box, 0)
        pygame.draw.rect(screen, (120, 120, 120), border_box, 2)

        if len(text) > 0:
            txt_surface = font.render(text, True, (255, 255, 255))
        else:
            txt_surface = font.render("Room Code...", True, (120, 120, 120))
        screen.blit(txt_surface, (input_box.x+12, input_box.y+12))

        display_help = ["V: Turn On/Off Visual Mode", "P: Change Log Position", "While using the program, first click the window icon in your task bar", "then use the buttons to properly trigger the commands.", "Leave blank to join the public room"]
        on_hint = 0
        for x in display_help:
            screen.blit(render_with_outline(x, font), (win32api.GetSystemMetrics(0)/2 - 160, win32api.GetSystemMetrics(1)/2 + 40 + (40 * on_hint)))
            on_hint += 1

        screen.blit(render_with_outline("Statistics (Local): ", font), (0, 0))

        screen.blit(render_with_outline(" Use Time: " + liner[0], font), (0, 24))
        screen.blit(render_with_outline(" Room's Joined: " + liner[1].replace("\n", ""), font), (0, 48))
        screen.blit(render_with_outline(" Distance Traveled: " + str(round(int(liner[2])/38/100000, 5)) + "km", font), (0, 72))

        screen.blit(render_with_outline("Information:", font), (win32api.GetSystemMetrics(0) - 250, 0))

        cast = "To clarify, you have no control over other \npeople's desktops. This is just a visual \nprogram. I made this program as a joke in \na couple of days. I am a high school \nstudent so I can't exactly afford a good \nserver and am using a home-made one hence \nthe not-so-optimal performance depending \non your location. If you would like to \nsupport me the best way to do it would be \nto check out my YouTube channel: DHMelon. \nWhich has videos about projects I make \nlike this one!"
        cast_ult = cast.split("\n")
        line_y_pos = 1
        for x in cast_ult:
            screen.blit(render_with_outline(x, font), (win32api.GetSystemMetrics(0) - 400, 24 * line_y_pos))
            line_y_pos += 1
        pygame.display.flip()

        clock.tick(20)  # Limit Main UI FPS because no animations are here, limiting this will decrease the CPU usage by a land slide, 20 FPS doesn't even change the feel of text typing + clicking


_circle_cache = {}  # I fucking hate everything about this
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points


def render_with_outline(text, font, gfcolor=(255, 255, 255), ocolor=(0, 0, 0), opx=2):
    try:
        textsurface = font.render(text, True, gfcolor).convert_alpha()
    except UnicodeError:
        textsurface = font.render("Invalid String", True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    try:
        osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))
    except UnicodeError:
        osurf.blit(font.render("Invalid String", True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf


def get_focused_window():
    returner = str(GetWindowText(GetForegroundWindow()))
    returner = returner.replace("~", "")
    if len(returner) > 50:
        returner = returner[:50] + "..."
    return returner


def set_window_boring_stuff():
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)\

    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)


def move_the_thing(mouse_pos):
    if len(list_of_messages) > 0:
        pygame.draw.rect(screen, (24, 24, 24), (mouse_pos[0] - message.pos_ult, mouse_pos[1], 200, 300))


ping_refresher = time.time()
ping_final = -1
target_color = (0, 255, 0)
def connection_things():
    global code
    res = str(status_read.get_pc_name())
    res = res.replace("~", "")
    code = code.replace("~", "")
    global ping_refresher
    global ping_final
    global target_color
    ping_calculator = time.time()
    send.send_to_machine(str(mouse_pos) + "~" + res + "~" + get_focused_window() + "~" + code + "~")  # Comm with server
    final = send.receive_from()
    if time.time() - ping_refresher >= 1:
        ping_refresher = time.time()
        ping_final = round((time.time() - ping_calculator) * 1000)
        if ping_final > 300:
            target_color = (255, 0, 0)
        elif ping_final > 150:
            target_color = (255, 255, 0)
        else:
            target_color = (0, 255, 0)

    font = pygame.font.Font('Silver.ttf', 32)
    screen.blit(render_with_outline("Ping: " + str(ping_final), font, gfcolor=target_color), (0, 0))

    lister = final.split("~")

    while len(last_tuppler) < len(lister):
        last_tuppler.append((0, 0))

    if final.count(str(mouse_pos)) >= 2:
        rf = ""
        try:
            for x in lister:
                if str(mouse_pos) in x and lister[lister.index(x) + 1] != str(status_read.get_pc_name()):
                    rf = lister[lister.index(x) + 1]  # Note: It works now I guess, I am not sure I feel drunk
                    list_of_messages.append(message.message("Contact", "With " + rf))
                    global timer_for_disappear
                    timer_for_disappear = time.time()
        except IndexError:
            pass

    if visual_mode:
        try:
            global on_
            on_ = 0
            for x in lister:
                if lister[lister.index(x) + 1] != str(status_read.get_pc_name()) and lister[lister.index(x) + 3] == code:
                    lister_main = list(re.findall('\d+', x))
                    lister_final_int = []
                    for zz in lister_main:
                        lister_final_int.append(int(zz))
                    if len(lister_main) >= 2 and (lister.index(x) % 4 == 0 or lister.index(x) == 0):
                        global tupler
                        tupler = tuple(lister_final_int)
                        font = pygame.font.Font('Silver.ttf', 32)
                        screen.blit(mouse_cursor, tupler)
                        screen.blit(render_with_outline(lister[lister.index(x) + 2], font), (tupler[0] + 20, tupler[1]))

                on_ += 1
        except IndexError:
            pass


if __name__ == '__main__':
    # mouse_icon = pygame.image.load("mouse_icon.ico")
    pygame.display.set_icon(mouse_cursor)

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
    display_res = [win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)]

    screen = pygame.display.set_mode((display_res[0], display_res[1]), pygame.NOFRAME)
    pygame.display.set_caption("Multiplayer Desktop")
    fuchsia = (255, 0, 128)
    set_window_boring_stuff()

    code = main_picker(screen, fuchsia)
    add_to(1, 1)

    mouse_cursor.convert()

    connection_enabled = True

    try:
        send.server_init()
    except ConnectionRefusedError:
        connection_enabled = False
        list_of_messages.append(message.message("Connection E#", "Connection to server failed."))
    timer_plus = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if message.pos_ult == 220:
                        message.pos_ult = -20
                    elif message.pos_ult == -20:
                        message.pos_ult = 220
                elif event.key == pygame.K_v:
                    if visual_mode:
                        visual_mode = False
                    else:
                        visual_mode = True

        try:
            mouse_pos = win32gui.GetCursorPos()
            if last_place != (-1, -1):
                x_change = abs(mouse_pos[0] - last_place[0])
                y_change = abs(mouse_pos[1] - last_place[1])
                total_change = round(math.sqrt(x_change ** 2 + y_change ** 2))
                if trigger_save:
                    threading.Thread(target=add_to, args=(total_change, 2)).start()
            last_place = mouse_pos
        except BaseException:
            mouse_pos = (0, 0)

        screen.fill(fuchsia)  # Transparent window

        move_the_thing(mouse_pos)
        if connection_enabled:
            connection_things()

        if len(list_of_messages) > 6:
            list_of_messages.pop(0)
        elif time.time() - timer_for_disappear > 8:
            timer_for_disappear = time.time()
            list_of_messages.clear()

        on = len(list_of_messages) - 1
        while on >= 0:
            list_of_messages[on].display_message(screen, mouse_pos, list_of_messages)
            on -= 1

        pygame.display.update()  # Display Update

        if time.time() - timer_plus >= 1:
            timer_plus = time.time()
            threading.Thread(target=add_to, args=(1, 0)).start()



