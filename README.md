# Dev-Time-Tracker
A time tracker &amp; grapher for us devs. It automatically logs the time we spend deving, and encourages us to stop watching YouTube by drawing graphs of our unproductivity. :D

# Updates:

November 27th, 2020 - Major Updates include:
- Added numerous more colors to chart individual items. Colors are assigned in relation to the amount of time spent on an individual label.
- Search the task list was causing a performance bottleneck, due to the fact that it was being requested every iteration. The data is now stored, referred to, and refreshed every 30s.
- It should now be drawing the chart when the program is closed. This is a "nice to have" thing, and just keeps the chart up to date with what is in the file (theoretically, as it's been a while since I tested whether this was working as intended).
- The program now checks for the __main__ namespace. This solved some issues with commandline functionality.
- You can now run TimeTracker.py with one optional argument. If ran with `TimeTracker.py draw`, it will draw the chart and end the program.
- Large improvement in window checks. Previously, subwindows would show a blank focus and be filed under "Other". It will now get the name of the parent window and be filed under the correct project properly.
- Any time spent on a label without a color available will be overflowed into the "Other" segment. I seem to remember it not doing this previously, but I can't confirm as I didn't keep dev notes on this project.
- The graph now shows hours on the legend, and has it offset so that it doesn't cover the pie chart. These are sorted most-least top-bottom.


April 4th, 2020 - Major Updates include:
- Overhaul to use JSON instead of my personal parsing and saving method, which was tremendously inferior and harder to work with.
- Added Bar Segments, which allow you to see all of the *individual* things you worked on throughout the day. These are color coded and match up with the pie chart
- Added a pie chart. It displays everything you worked on (up to 14 items) in segments of hrs/total hrs deving, while also displaying how many hours were put into each segment.
- Lowered the hour range to 10. This was done to look better for personal averages. It can be adjusted by changing `total_hours`
- It now stops counting after 120s of inactivity (no keyboard presses or mouse movement). If a "development" window is open but none of the types recognized are in focus, time is added to the "other" category. 

## Forewarnings
It uses the PIL image generation library, so I believe it only works on Windows. I'll look into getting this working on other OSs soon.

It, by default, detects when Unity, Visual Studio Code, or Synfig Studio is running and pulls the project name from the window. If you want to add others, please make a request or add them in the `get_focus()` function. Because each program displays project names in different formats, each program needs its own parsing format.

The seconds for each day of every month and year saved in the "time_table.json" file that gets created when it is run.

## Conclusion
I went to Windows Scheduler and had it run this with a 60s delay after any logon. Works splendidly!

Here's my actual productivity graphs from the past few months (As of the last major update):

![Productivity graph](https://i.imgur.com/SelXfVi.png)

![Productivity graph](https://i.imgur.com/uq1mSvK.png)
