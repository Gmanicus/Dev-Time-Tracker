# Dev Time Tracker
# By: Grant Scritsmier @ Geek Overdrive Studio


import subprocess
import re
import os
import sys
import string
import time
import math
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import calendar
import atexit

# Thanks to Ippo343 and Michele Ippolito (Just realized that's probably the same person)
#
# Enter your process names here. TimeTracker will run through and check these.
process_names = [
    "Code.exe",
    "Unity.exe",
    "Brackets.exe",
]

# Months for correlating dates. Datetime returns a month number, so we just grab that index from this list to get its name.
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

today_time = 0 # Don't touch this unless you want to always start the day off with a head start
tick_time = 2 # How many seconds should there be between checks? (regulated to always be accurate)

# Want your graph to be larger? Here's the (x, y) values. Change these as you need. TimeTracker will adapt to new sizes.
base_size = {
    "x": 1600,
    "y": 500
}

# These values are in pixels
bar_width = 50
spacer_width = 10   # Space between each bar
margin_width = 100  # Space on the sides of the graph (Be sure not to set this too low, or text will be hidden)
bot_margin = 50     # Space between the bottom of the graph and the bottom of the image
hour_height = 20    # How high should each hour be?

total_hours = 20    # How many hours should we graph for?

multiplier = 1      # This multiplies the base_size. You can provide an aspect ratio and use this if you like, but beware,
                    # text doesn't change size. Too large, and you won't be able to read anything.

def init():
    # Setup all global variables

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

    # initialize all the variables so we don't have issues
    init()

    global time_now
    global today_time
    global year_m_day

    while True:
    
        # Run through each name in the process_names list and check if they're online
        # Thanks again for this push by Ippo/Michele/Ippo and Michele.
        for name in process_names:
            online = get_window(name)
            if online:
                break
        else:
            online = None

        time.sleep(tick_time - ((time.time() - starttime) % tick_time)) # This has the loop sleep for the calculated time to make it run exactly every tick_time seconds.

        if online:
            today_time += tick_time

        if (today_time % 2 == 0): # Run every 2 seconds when we're online.

            # Print today's logged time into the console. It overwrites the last line with several spaces. This'll work fine unless you don't sleep for apx 115 days striaght.
            print("\rtick: " + str(today_time) + "        ", end="")

            day = get_day(datetime.now().day)
            year_m_day = str(time_now["year"]) + "_" + str(time_now["month"]) + "_" + day

            last_day = parse_data("get_last_day", "none")
            today = get_day_num(day)

            if last_day < today and last_day != 0:      # If the hour has turned past 11:59pm and it is the next day
                # Store the current time and reset for the new day
                parse_data("store", get_day(last_day))
                today_time = 0
                parse_data("store", day)

            if (last_day > today or last_day > month_length[1]):    # If the hour has turned past 11:59pm and it is the next month
                # Store the current time, reset for the new day, and update the time_now dict.
                time_now = {
                    "year": datetime.now().year,
                    "month": datetime.now().month
                }

                parse_data("store", get_day(last_day))
                today_time = 0
                parse_data("store", day)

                #parse_data("clear", "none")
                #cleared = True

            if (today_time % 120 == 0):     # Every two minutes we're online
                # Draw our pretty little graph
                draw_graph()
            
            if last_day == today or last_day == 0:  # If the date hasn't changed
                # Store today's logged time
                parse_data("store", day)



def draw_graph():

    # Draw our graph image with its background color
    graph = Image.new('RGBA', (base_size["x"], base_size["y"]), (25,35,40,255))
    graph_context = ImageDraw.Draw(graph)
    font = ImageFont.truetype('font.ttf', 20)
    font_small = ImageFont.truetype('font.ttf', 15)
    font_large = ImageFont.truetype('font.ttf', 40)

    # Draw the graph context lines and the text next to them
    for l in range(0, math.ceil(total_hours/4)):    # Draw a line once for every four hours
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
    
    # Draw the graph edges
    graph_context.line([(margin_width, drfbPILsftossd(0)), (margin_width, drfbPILsftossd(hour_height * 25))], width=3, fill=(100,100,100,255))
    graph_context.line([(base_size["x"] - margin_width, drfbPILsftossd(0)), (base_size["x"] - margin_width, drfbPILsftossd(hour_height * 25))], width=3, fill=(100,100,100,255))


    text = months[time_now["month"]-1]
    text_size = font_large.getsize(text)

    # This draws the month name
    graph_context.text((((base_size["x"] / 2) - (text_size[0] / 2)), drfbPILsftossd((base_size["y"] / 1.2) + (text_size[1] / 2) )), text, font=font_large, fill=(125,125,125,255))

    m_hours = []

    # Get each stored time for this month
    for h in range(1, month_length[1]+1):
        hour = round(parse_data("get", get_day(h)) / 3600, 1)

        m_hours.append(hour)


    # For every stored time for this month...
    for x in range(1, month_length[1]+1):
        # Draw this day's bar in the graph

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

    # Draw the "Day" and "Hour" text to mark that vertical is hours and horizontal is days.

    text = "DAY"
    text_size = font_small.getsize(text)

    graph_context.text(((margin_width - (text_size[0] * 2)), drfbPILsftossd(-15) ), text, font=font_small, fill=(100,100,100,255))

    text = "HOURS"
    text_size = font_small.getsize(text)

    graph_context.text(((margin_width - (text_size[0] * 2.5)), drfbPILsftossd((12 * hour_height) + (text_size[1] / 2)) ), text, font=font_small, fill=(100,100,100,255))


    # Save our graph file
    graph.save("PerfGraph_" + str(time_now["month"]) + "_" + months[time_now["month"]-1] + "_" + str(time_now["year"]) + ".png", "PNG")


def get_window(name):   # Check the windows task list for the given process "name"
    found = False
    tasks = str(subprocess.check_output(['tasklist'])).split("\\r\\n")
    p = []
    for task in tasks:
        m = re.match("(.+?) +(\d+) (.+?) +(\d+) +(\d+.* K).*",task)
        if m is not None:
            p.append(m.group(1))

    if is_not_in_table(name, p) == False:   # Not sure why I made the function force a double negative, but alright
        found = True

    return found

def parse_data(method, day):    # Parse the data from the log file with the given method, for the given day
    if os.path.exists("this_graph.txt"):
        graph = open("this_graph.txt", "r")
        data = graph.read()
    else:
        data = ""

    year_m_day = str(time_now["year"]) + "_" + str(time_now["month"]) + "_" + day

    return_data = 0

    if (method == "get"):   # Get the given day's stored time
        pos = data.find(year_m_day)

        if (pos != -1):
            pos = data.find("=", pos) + 2
            pos2 = data.find("\n", pos)
            
            return_data = int(data[pos:pos2])
            try:
                graph.close()
            except: None

    if (method == "get_last_day"):  # Get the last day that was stored on the list
        pos = data.rfind("[")

        if (pos != -1):
            pos += 1
            pos2 = data.find("]", pos)
            
            return_data = int(data[pos:pos2])
            try:
                graph.close()
            except: None

    if (method == "store"):     # Store the given day's logged time
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

    if (method == "clear"):     # Clear the log file data
        open("this_graph.txt", "w").close

    return return_data



def get_day(num):   # Given a number, turn it into string. Day 1 would be "[01]", Day 21 would be "[21]", etc
    if (num < 10):
        num = "0" + str(num)
    else:
        num = str(num)
    
    return "[" + num + "]"


def get_day_num(day):   # Inverse of the above function
    day = day[1:]; day = day[:2]
    
    return int(day)



def is_not_in_table(text, table):   # Not quite sure why I made this function return a negative, but alright...
                                    # Checks to see if the string is found in the given table
    result = True
    for i in range(len(table)):
        if text == table[i]:
            result = False
            break

    return result

def drfbPILsftossd(num):    # This function is abbreviated from a very angry function when I remembered that drawing is typically done with a reversed y-axis
                            # This reverses that logic once again so that lower numbers are lower in height than higher numbers. 0 < 1
    return base_size["y"] - (num + bot_margin)







def exit_handler():     # If we close unexpectedly (Shut down, file exited)
    draw_graph()        # Draw the graph

atexit.register(exit_handler)


init()  # Initialize the variables. Not going to touch this, but I believe this was done for the system argument functionality, which would mean it can be moved 5 lines down

if (len(sys.argv) == 1):    # If there are no sys args, run
    main()
else:
    if (sys.argv[1] == "draw"): # Run if the sys arg is "draw" (In commandline: TimeTracker.py -draw)
        draw_graph()
    else:
        print("Unrecognized command...")   # If anything else, give the option to run the file
        var = input("'run' or exit")

        if var == "run":
            main()
        else:
            exit()
