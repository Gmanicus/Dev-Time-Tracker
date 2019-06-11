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
from PIL import Image, ImageDraw, ImageFont
import calendar
import atexit

process_names = [
    "Code.exe",
    "Unity.exe",
    "Brackets.exe",
]

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

today_time = 0
tick_time = 2

base_size = {
    "x": 1600,
    "y": 500
}

bar_width = 50
spacer_width = 10
margin_width = 100
bot_margin = 50
hour_height = 20
total_hours = 20

multiplier = 1

def init():
    global time_now
    time_now = {
        "year": datetime.now().year,
        "month": datetime.now().month
    }

    global month_length
    month_length = calendar.monthrange(time_now["year"], time_now["month"])

    global base_size
    base_size["x"] *= multiplier
    base_size["y"] *= multiplier

    global bar_width
    global hour_height

    bar_width = ( (base_size["x"] - (margin_width * 2) ) - (spacer_width * (month_length[1] + 1)) ) / month_length[1]
    hour_height = (base_size["y"] - (bot_margin * 2)) / total_hours

    day = get_day(datetime.now().day)

    global year_m_day
    year_m_day = str(time_now["year"]) + "_" + str(time_now["month"]) + "_" + day

    global starttime
    starttime = time.time()

    global today_time
    today_time = parse_data("get", day)

def main():

    init()

    global time_now
    global today_time
    global year_m_day

    while True:
    
        for name in process_names:
            online = get_window(name)
            if online:
                break
        else:
            online = None

        time.sleep(tick_time - ((time.time() - starttime) % tick_time))

        if online:
            today_time += tick_time

        if (today_time % 2 == 0):
            print("\rtick: " + str(today_time) + "        ", end="")
            #cleared = False

            day = get_day(datetime.now().day)
            year_m_day = str(time_now["year"]) + "_" + str(time_now["month"]) + "_" + day

            last_day = parse_data("get_last_day", "none")
            today = get_day_num(day)

            if last_day < today and last_day != 0:
                parse_data("store", get_day(last_day))
                today_time = 0
                parse_data("store", day)

            if (last_day > today or last_day > month_length[1]):
                time_now = {
                    "year": datetime.now().year,
                    "month": datetime.now().month
                }
                parse_data("store", day)

                #parse_data("clear", "none")
                #cleared = True

            if (today_time % 120 == 0):
                draw_graph()
            
            if last_day == today or last_day == 0:
                parse_data("store", day)



def draw_graph():
    random.seed(time.time())

    graph = Image.new('RGBA', (base_size["x"], base_size["y"]), (25,35,40,255))
    graph_context = ImageDraw.Draw(graph)
    font = ImageFont.truetype('C:\Windows\Fonts\chinese rocks rg.ttf', 20)
    font_small = ImageFont.truetype('C:\Windows\Fonts\chinese rocks rg.ttf', 15)
    font_large = ImageFont.truetype('C:\Windows\Fonts\chinese rocks rg.ttf', 40)

    
    for l in range(0, math.ceil(total_hours/4)):
        color = (70,70,70,255)
        width = 1
        if ((l * 4) % 8 == 0):
            color = (100,100,100,255)
            width = 2

        height = hour_height * (l * 4)

        text = str(l * 4)
        text_size = font.getsize(text)

        graph_context.line([(margin_width - 5, drfbPILsftossd(height)), (base_size["x"] - margin_width, drfbPILsftossd(height))], width=width, fill=color)
        graph_context.text((margin_width - (35 + (text_size[0] / 2)), drfbPILsftossd(height + (text_size[1] / 2) )), text, font=font, fill=color)
    
    graph_context.line([(margin_width, drfbPILsftossd(0)), (margin_width, drfbPILsftossd(hour_height * 25))], width=3, fill=(100,100,100,255))
    graph_context.line([(base_size["x"] - margin_width, drfbPILsftossd(0)), (base_size["x"] - margin_width, drfbPILsftossd(hour_height * 25))], width=3, fill=(100,100,100,255))


    text = months[time_now["month"]-1]
    text_size = font_large.getsize(text)

    graph_context.text((((base_size["x"] / 2) - (text_size[0] / 2)), drfbPILsftossd((base_size["y"] / 1.2) + (text_size[1] / 2) )), text, font=font_large, fill=(125,125,125,255))

    m_hours = []

    for h in range(1, month_length[1]+1):
        hour = round(parse_data("get", get_day(h)) / 3600, 1)

        m_hours.append(hour)


    for x in range(1, month_length[1]+1):
        bar_pos = margin_width + (spacer_width * x) + (bar_width * (x - 1))
        bar_pos2 = bar_pos + bar_width

        hours = m_hours[x-1]

        text = str(hours)
        text_size = font.getsize(text)
        hour = hours * hour_height


        graph_context.rectangle([(bar_pos, drfbPILsftossd(hour)), (bar_pos2, drfbPILsftossd(0))], fill=(50,80,225,255))
        if (not hours < 2):
            graph_context.text(((bar_pos + ((bar_width / 2) - (text_size[0] / 2)) ), drfbPILsftossd(hour-12) ), text, font=font, fill=(35,50,160,255))

        day = x

        if (day < 10):
            day = "0" + str(x)
        else:
            day = str(x)

        text = str(day)
        text_size = font.getsize(text)

        color = (70,70,70,255)

        graph_context.text(((bar_pos + ((bar_width / 2) - (text_size[0] / 2)) ), drfbPILsftossd(-15) ), text, font=font, fill=color)

    text = "DAY"
    text_size = font_small.getsize(text)

    graph_context.text(((margin_width - (text_size[0] * 2)), drfbPILsftossd(-15) ), text, font=font_small, fill=(100,100,100,255))

    text = "HOURS"
    text_size = font_small.getsize(text)

    graph_context.text(((margin_width - (text_size[0] * 2.5)), drfbPILsftossd((12 * hour_height) + (text_size[1] / 2)) ), text, font=font_small, fill=(100,100,100,255))


    graph.save("PerfGraph_" + str(time_now["month"]) + "_" + months[time_now["month"]-1] + "_" + str(time_now["year"]) + ".png", "PNG")


def get_window(name):
    found = False
    tasks = str(subprocess.check_output(['tasklist'])).split("\\r\\n")
    p = []
    for task in tasks:
        m = re.match("(.+?) +(\d+) (.+?) +(\d+) +(\d+.* K).*",task)
        if m is not None:
            p.append(m.group(1))

    if is_not_in_table(name, p) == False:
        found = True

    return found

def parse_data(method, day):
    if os.path.exists("this_graph.txt"):
        graph = open("this_graph.txt", "r")
        data = graph.read()
    else:
        data = ""

    year_m_day = str(time_now["year"]) + "_" + str(time_now["month"]) + "_" + day

    return_data = 0

    if (method == "get"):
        pos = data.find(year_m_day)

        if (pos != -1):
            pos = data.find("=", pos) + 2
            pos2 = data.find("\n", pos)
            
            return_data = int(data[pos:pos2])
            try:
                graph.close()
            except: None

    if (method == "get_last_day"):
        pos = data.rfind("[")

        if (pos != -1):
            pos += 1
            pos2 = data.find("]", pos)
            
            return_data = int(data[pos:pos2])
            try:
                graph.close()
            except: None

    if (method == "store"):
        graph = open("this_graph.txt", "w")

        pos = data.find(year_m_day)

        if (pos != -1):
            pos = data.find("=", pos) + 2
            pos2 = data.find("\n", pos)

            data_back = data[:pos]
            data_forward = data[pos2:]

            data = data_back + str(today_time) + data_forward
        else:
            data += year_m_day + " = " + str(today_time) + "\n"

        graph.write(data)
        graph.close()

    if (method == "clear"):
        open("this_graph.txt", "w").close

    return return_data



def get_day(num):
    if (num < 10):
        num = "0" + str(num)
    else:
        num = str(num)
    
    return "[" + num + "]"


def get_day_num(day):
    day = day[1:]; day = day[:2]
    
    return int(day)



def is_not_in_table(text, table):
    result = True
    for i in range(len(table)):
        if text == table[i]:
            result = False
            break

    return result

def drfbPILsftossd(num):
    return base_size["y"] - (num + bot_margin)







def exit_handler():
    draw_graph()

atexit.register(exit_handler)


init()

if (len(sys.argv) == 1):
    main()
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
