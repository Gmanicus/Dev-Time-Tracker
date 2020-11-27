# Dev Time Tracker
# By: Grant Scritsmier @ Geek Overdrive Studio

import subprocess
import re
import os
import sys
import string
import time
import math
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import matplotlib.pyplot as plotter
import win32gui
from parse import *
import calendar
import atexit
import mouse
import keyboard
import json
import operator
import traceback

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

time_table = {}
task_table = []

today_time = 0
update_time = 0
last_task_check = 0
tick_time = 2

base_size = {
    "x": 1600,
    "y": 900
}

bar_width = 50
spacer_width = 10
margin_width = 100
top_margin = 50
bot_margin = 500
hour_height = 20
total_hours = 10
hour_segments = 2

# All colors available + Other/General color
max_partitions_per_bar = 14


# Quality of Life Changes

segment_overextension = 5
text_offset = 35

class rgb:
    background = (25,35,40,255)

    # Assigning colors:
    #
    # Different code files get colors "one" through "five", depending on order edited for this month
    #
    # Overflow code files worked on and all other work gets color "general"

    bar = [
        (50,80,225,255),
        (178,91,44,255),
        (127,19,46,255),
        (181,167,21,255),
        (97,184,82,255),
        (16,143,152,255),
        (122,47,183,255),
        (196,60,182,255),
        (89,42,1,255),
        (124,0,104,255),
        (71,79,124,255),
        (0,124,35,255),
        (128,183,0,255),
    ]

    general_hours = (175,175,175,255)

    dark_div = (70,70,70,255)
    light_div = (100,100,100,255)
    bright_div = (125,125,125,255)

    bar_text = (45,45,45,255)


# Variable statements to satisfy Python

min_hour_draw = 1

multiplier = 1

mouse_pos = (0,0)

activity = 0
inactivity_max = 120



# DEBUG MODE....................
initialize = True
show_status = True



def test():
    # graph = open("this_graph.txt", "r")
    # data = graph.read()

    global time_now
    time_now = {
        "year": datetime.now().year,
        "month": datetime.now().month,
        "day": datetime.now().day
    }

    global month_length
    month_length = calendar.monthrange(time_now["year"], time_now["month"])

    global bar_width
    global hour_height

    bar_width = ( (base_size["x"] - (margin_width * 2) ) - (spacer_width * (month_length[1] + 1)) ) / month_length[1]
    hour_height = (base_size["y"] - (bot_margin + top_margin)) / total_hours

    # return_data = search("2019_11_[03] = {}\n", data)
    # test_data = data[return_data.spans[0][0]:return_data.spans[0][1]]
    # #return_data["test"] = "test123"
    # print(return_data.fixed[0])
    # print(test_data)

    #draw_graph()

    time.sleep(1)

    get_focus()

    # while True:

    #     draw_graph()

    #     time.sleep(10)





def init():
    global time_now
    time_now = {
        "year": datetime.now().year,
        "month": datetime.now().month,
        "day": datetime.now().day
    }

    global month_length
    month_length = calendar.monthrange(time_now["year"], time_now["month"])

    global base_size
    base_size["x"] *= multiplier
    base_size["y"] *= multiplier

    global bar_width
    global hour_height

    bar_width = ( (base_size["x"] - (margin_width * 2) ) - (spacer_width * (month_length[1] + 1)) ) / month_length[1]
    hour_height = (base_size["y"] - (bot_margin + top_margin)) / total_hours

    day = datetime.now().day

    global year_m_day
    year_m_day = str(time_now["year"]) + "_" + str(time_now["month"]) + "_" + str(day)

    global starttime
    starttime = time.time()

    global update_time

    load_backup()

def main():

    global time_now
    global today_time
    global update_time
    global year_m_day
    global show_status

    prev_time = 0

    keyboard.hook(check_activity)

    if (not show_status):
        time1 = 0
        time2 = 0
        time3 = 0

    while True:
        if (not show_status):
            time1 = time.time()

        if (check_activity()):

            if (not show_status):
                time3 = time.time()

            online = get_window("Code.exe")
            if not online:
                online = get_window("Unity.exe")
            if not online:
                online = get_window("Brackets.exe")
            if not online:
                online = get_window("PaintDotNet.exe")
            if not online:
                online = get_window("synfigstudio.exe")
            if not online:
                online = get_window("brave.exe")
                if ("Browsing" in get_focus() or "Other" in get_focus()):
                    online = False
            
            if (not show_status):
                time2 = time.time()
                print("get_window took: {}".format(time2 - time3))

            # locks it to the system time to make sure the function repeats exactly every tick_time no matter how long the function after it takes
            time.sleep(tick_time - ((time.time() - starttime) % tick_time))

            if online:
                today_time += tick_time
                update_time += tick_time

            last_day = time_now["day"]

            if (today_time % 2 == 0):
                time_now = {
                    "year": datetime.now().year,
                    "month": datetime.now().month,
                    "day": datetime.now().day
                }

                focus = get_focus()

                if (show_status):
                    os.system("cls")
                    #print("Tick: " + str(today_time) + " | Next Graph in: " + str(120 - (today_time % 120)) + " ticks | Time since last activity: " + str(activity))
                    print("Current Activity: {0}\nTime Logged: {1}s\nNext Graph() in {2}s\nInactivity Countdown: {3}s".format(focus, today_time, 120 - (today_time % 120), activity))

                year_m_day = str(time_now["year"]) + "_" + str(time_now["month"]) + "_" + str(time_now["day"])

                today = time_now["day"]

                if last_day < today:
                    add_time(last_day, focus)
                    add_time(today, focus)

                    last_day = time_now["day"]

                if last_day > today:
                    time_now = {
                        "year": datetime.now().year,
                        "month": datetime.now().month,
                        "day": datetime.now().day
                    }

                    add_time(last_day, focus)
                    add_time(today, focus)

                    last_day = time_now["day"]

                if (today_time % 120 == 0 and today_time != prev_time):
                    draw_graph()
                    backup()
                
                if last_day == today:
                    add_time(today, focus)

                update_time = 0

                prev_time = today_time

                if (not show_status):
                    time2 = time.time()
                    print(time2 - time1)



def draw_graph():
    global rgb
    global max_partitions_per_bar

    graph = Image.new('RGBA', (base_size["x"], base_size["y"]), rgb.background)
    graph_context = ImageDraw.Draw(graph)
    font = ImageFont.truetype('C:\Windows\Fonts\chinese rocks rg.ttf', 20)
    font_small = ImageFont.truetype('C:\Windows\Fonts\chinese rocks rg.ttf', 15)
    font_large = ImageFont.truetype('C:\Windows\Fonts\chinese rocks rg.ttf', 40)

    year_m = str(time_now["year"]) + "_" + str(time_now["month"]) + "_"
    year_m_fileorder = str(time_now["year"]) + "_" + str(time_now["month"]) + "_" + "fileorder"

    
    for l in range(0, math.ceil(total_hours/hour_segments)):
        color = rgb.dark_div
        width = 1
        if ((l * hour_segments) % (hour_segments*2) == 0):
            color = rgb.light_div
            width = 2

        height = hour_height * (l * hour_segments)

        text = str(l * hour_segments)
        text_size = font.getsize(text)

        far_inner_margin = base_size["x"] - margin_width

        graph_context.line(
            [(margin_width - segment_overextension, invert_from(height)),
            (far_inner_margin, invert_from(height))],
            width=width,
            fill=color)
        
        graph_context.text(
            (margin_width - (text_offset + (text_size[0] / 2)),
            invert_from(height + (text_size[1] / 2) )),
            text,
            font=font,
            fill=color)

    
    # OOF, Out of Frame
    oof_height = invert_from(hour_height * 25)

    graph_context.line(
        [(margin_width, invert_from(0)),
        (margin_width, oof_height)],
        width=3,
        fill=rgb.light_div)

    graph_context.line(
        [(far_inner_margin, invert_from(0)),
        (far_inner_margin, oof_height)],
        width=3,
        fill=rgb.light_div)


    text = months[time_now["month"]-1]
    text_size = font_large.getsize(text)

    header_size = [((base_size["x"] / 2) - (text_size[0] / 2)),
                  invert_to((base_size["y"] + (top_margin/2)) - (text_size[1] / 2))]

    graph_context.text(
        (header_size[0],
        header_size[1]),
        text,
        font=font_large,
        fill=rgb.bright_div)

    m_hours = []

    for h in range(1, month_length[1]+1):
        if year_m + str(h) in time_table:
            hour_partitions = time_table[year_m + str(h)]

            m_hours.append(hour_partitions)
        else:
            m_hours.append(None)

    for x in range(1, month_length[1]+1):
        bar_pos = margin_width + (spacer_width * x) + (bar_width * (x - 1))
        bar_pos2 = bar_pos + bar_width

        if (m_hours[x-1]):

            hour_partitions = sort_partitions(m_hours[x-1])

            # If there are more hour partitions than the max, group the overflowing values into the max hour's value
            if (len(hour_partitions) > max_partitions_per_bar):
                overflow = len(hour_partitions) - max_partitions_per_bar

                overflow_hours = 0
                keys = []

                foo = 0

                for k, v in hour_partitions.copy().items():
                    foo += 1
                    if foo >= len(hour_partitions) - overflow:
                        overflow -= 1
                        overflow_hours += v
                        del hour_partitions[k]
                    else:
                        keys.append(k)

                if "Other" in hour_partitions:
                    hour_partitions["Other"] += overflow_hours
                else:
                    overflow_hours += hour_partitions[keys[len(keys)-1]]
                    del hour_partitions[keys[len(keys)-1]]
                    hour_partitions["Other"] = overflow_hours

            partition_height = 0

            cn = 0
            for k, hr in hour_partitions.items():

                if (k != "Other"):
                    fill_color = rgb.bar[cn]
                    cn += 1
                else:
                    fill_color = rgb.general_hours

                hour_amt = round(hr / 3600, 1)

                seconds_to_pixel = round(3600/hour_height)

                if (hr < seconds_to_pixel):
                    continue

                text = str(hour_amt)
                text_size = font.getsize(text)
                hour = hour_amt * hour_height

                graph_context.rectangle(
                    [(bar_pos, invert_from(partition_height + hour)), (bar_pos2, invert_from(partition_height))],
                    fill=fill_color)

                if (not hour_amt < min_hour_draw):
                    graph_context.text(
                        ((bar_pos + ((bar_width / 2) - (text_size[0] / 2)) ), invert_from(partition_height + hour - 12)),
                        text,
                        font=font,
                        fill=rgb.bar_text)

                partition_height += hour

        day = x

        if (day < 10):
            day = "0" + str(x)
        else:
            day = str(x)

        text = str(day)
        text_size = font.getsize(text)

        color = (70,70,70,255)

        graph_context.text(
            ((bar_pos + ((bar_width / 2) - (text_size[0] / 2)) ), invert_from(-15)),
            text,
            font=font,
            fill=color)

    text = "DAY"
    text_size = font_small.getsize(text)

    graph_context.text(
        ((margin_width - (text_size[0] * 2)), invert_from(-15)),
        text,
        font=font_small,
        fill=(100,100,100,255))

    text = "HOURS"
    text_size = font_small.getsize(text)

    graph_context.text(
        ((margin_width - (text_size[0] * 2.5)), invert_from(((total_hours/2 - 1) * hour_height) + (text_size[1] / 2))),
        text,
        font=font_small,
        fill=(100,100,100,255))

    title = "PerfGraph_" + str(time_now["month"]) + "_" + months[time_now["month"]-1] + "_" + str(time_now["year"]) + ".png"

    graph.save(title, "PNG")

    im = Image.open(title)

    draw_piechart(im)

    im.save(title)


def draw_piechart(im):
    # Guest age group

    year_m_fileorder = str(time_now["year"]) + "_" + str(time_now["month"]) + "_" + "fileorder"

    files = []
    hours = []
    colors = ()

    hour_partitions = sort_partitions(time_table[year_m_fileorder])

    # If there are more hour partitions than the max, group the overflowing values into the max hour's value
    if (len(hour_partitions) > max_partitions_per_bar):
        overflow = len(hour_partitions) - max_partitions_per_bar

        overflow_hours = 0
        keys = []

        foo = 0
        for k, v in hour_partitions.copy().items():
            foo += 1
            if foo >= len(hour_partitions) - overflow:
                overflow -= 1
                overflow_hours += v
                del hour_partitions[k]
            else:
                keys.append(k)

        if "Other" in hour_partitions:
            hour_partitions["Other"] += overflow_hours
        else:
            overflow_hours += hour_partitions[keys[len(keys)-1]]
            del hour_partitions[keys[len(keys)-1]]
            hour_partitions["Other"] = overflow_hours

    something_to_chart = False

    cn = 0
    for k, v in hour_partitions.items():
        if (v < 1800):
            continue
        else:
            something_to_chart = True

        if (round(v/3600, 1) > 10):
            files.append("[{} hrs] {}".format(round(v/3600, 1), k))
        else:
            files.append("[  {} hrs] {}".format(round(v/3600, 1), k))
        hours.append(v)

        if (k != "Other"):
            color_tuple = tuple(ti/255.0 for ti in rgb.bar[cn])
            colors = colors + (color_tuple,)
            cn += 1
        else:
            color_tuple = tuple(ti/255.0 for ti in rgb.general_hours)
            colors = colors + (color_tuple,)

    def actual_value(val):
        return "{}hrs".format(round(val/100.*(sum(hours)/3600), 1))

    if (something_to_chart):
        figureObject, axesObject = plotter.subplots()

        patches = axesObject.pie(hours,
                    colors       = colors,
                    textprops    = {'color':"w"},
                    autopct      = actual_value,
                    startangle   = 0)

        axesObject.axis('equal')

        lgd = plotter.legend(patches[0], files, loc=(1,0.5))

        plotter.savefig('chart.png', transparent=True, bbox_extra_artists=(lgd,), bbox_inches='tight')
        plotter.cla()
        plotter.close(figureObject)


        chart = Image.open('chart.png')

        chart = ImageEnhance.Brightness(chart).enhance(0.75)
        chart = ImageEnhance.Contrast(chart).enhance(1.02)

        im.paste(chart, ((margin_width), invert_from(-50)), chart)


def add_time(day, focus):
    year_m_day = str(time_now["year"]) + "_" + str(time_now["month"]) + "_" + str(day)
    year_m_fileorder = str(time_now["year"]) + "_" + str(time_now["month"]) + "_" + "fileorder"

    if year_m_day in time_table:
        if year_m_fileorder not in time_table:
            time_table[year_m_fileorder] = {}
        if focus not in time_table[year_m_fileorder]:
            time_table[year_m_fileorder][focus] = 0
        if focus not in time_table[year_m_day]:
            time_table[year_m_day][focus] = 0
        time_table[year_m_fileorder][focus] += tick_time
        time_table[year_m_day][focus] += tick_time
    else:
        time_table[year_m_day] = {}


# Load all of the backup data
def load_backup():
    json_data = {}
    global time_table

    try:
        with open("time_table.json", "r") as server_data_file:
            json_data = json.load(server_data_file)

            time_table = json_data
    except Exception as e:
        print(e)
        print("\n**BACKUP MODIFIED OR CORRUPTED**\n")


# Backup all of the data
def backup():
    with open("time_table.json", "w") as server_data_file:
        json.dump(time_table, server_data_file, indent=4, sort_keys=True)


def get_window(name):
    global last_task_check
    global task_table
    found = False
    
    # Bottleneck found in get_window. Now storing subprocess output and only updating it every 30s
    if (time.time() - last_task_check > 30):
        last_task_check = time.time()
        task_table = str(subprocess.check_output(['tasklist'])).split("\\r\\n")

    p = []
    for task in task_table:
        m = re.match("(.+?) +(\d+) (.+?) +(\d+) +(\d+.* K).*",task)
        if m is not None:
            p.append(m.group(1))

    if is_not_in_table(name, p) == False:
        found = True

    return found

def get_focus():
    focus = win32gui.GetWindowText(win32gui.GetForegroundWindow())

    # If the focus is empty, attempt to get the parent window's text. This accounts for a subwindow being in focus
    if (focus == ""):
        try:
            focus = win32gui.GetWindowText( win32gui.GetParent(win32gui.GetForegroundWindow()) )
        except:
            focus = "no_window"

    if (not initialize):
        print(focus)

    if ("Visual Studio Code" in focus):
        focus = search("{} - Visual", focus)
        if (focus):
            focus = focus.fixed[0]
    elif ("Synfig Studio" in focus):
        focus = search("{} - Synfig Studio", focus)
        if (focus):
            focus = "ASSET: " + focus.fixed[0]
    elif ("paint.net" in focus):
        focus = search("{} - paint.net", focus)
        if (focus):
            if ("Untitled" not in focus.fixed[0]):
                focus = "ASSET: " + focus.fixed[0]
    elif ("Unity" in focus and "Personal" in focus):
        focus = search("{} - {} -", focus)
        if (focus):
            focus = "PROJECT: " + focus.fixed[0]
    elif ("Brave" in focus or "Chrome" in focus):
        if ("Google Docs" in focus):
            focus = search("{} - {} -", focus)
            if (focus):
                focus = "DESIGN: " + focus.fixed[0]
        else:
            focus = "Browsing"
    else:
        focus = "Other"

    if isinstance(focus, str):
        if (len(focus) > 50):
            focus = "Other"
    else:
        focus = "Other"

    
    return focus

def check_activity(event = False):
    global activity
    global inactivity_max
    global mouse_pos
    global tick_time

    if (not event):
        if mouse.get_position() == mouse_pos:
            activity = activity - tick_time
        else:
            activity = inactivity_max
            mouse_pos = mouse.get_position()
    else:
        activity = inactivity_max

    return not (activity < 0)


def sort_partitions(parts):
    sorted_dict = {}

    year_m_fileorder = str(time_now["year"]) + "_" + str(time_now["month"]) + "_" + "fileorder"
    fo = time_table[year_m_fileorder]
    fo = dict( sorted(fo.items(), key=operator.itemgetter(1),reverse=True))

    for key in fo:
        if key in parts:
            sorted_dict[key] = parts[key]
        else:
            sorted_dict[key] = 0

    return sorted_dict

def is_not_in_table(text, table):
    result = True
    for i in range(len(table)):
        if text == table[i]:
            result = False
            break

    return result

def invert_from(num):
    return base_size["y"] - (num + bot_margin)

def invert_to(num):
    return base_size["y"] - (num - top_margin)







def exit_handler():
    if (tick_time % 120 > 60):
        draw_graph()

atexit.register(exit_handler)

if (initialize):
    if __name__ == "__main__":
        init()

        if (len(sys.argv) == 1):
            try:
                main()
            except Exception:
                with open("error_dump.json", "w") as error:
                    error.write(traceback.format_exc())
                    error.close()
        else:
            if (sys.argv[1] == "draw"):
                draw_graph()
            else:
                print("Unrecognized command...")
                var = input("'run' or exit")

                if var == "run":
                    main()
                else:
                    exit()
    else:
        with open("tooty.txt", "w") as test:
            test.write("welp")
            
else:
    test()
