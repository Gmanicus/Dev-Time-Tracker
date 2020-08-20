# Dev-Time-Tracker
A time tracker &amp; grapher for us devs. It automatically logs the time we spend deving, and encourages us to stop watching YouTube by drawing graphs of our unproductivity. :D

# Updates:

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

![Productivity graph](https://i.imgur.com/Zi0lY0V.png)

![Productivity graph](https://i.imgur.com/N7S2zgI.png)
