# Dev-Time-Tracker
A time tracker &amp; grapher for us devs. It automatically logs the time we spend deving, and encourages us to stop watching YouTube by drawing graphs of our unproductivity. :D

## Forewarnings
It uses the PIL image generation library, so I believe it only works on Windows. I'll look into getting this working on other OSs soon.

It, by default, detects when "Unity.exe", "Code.exe", or "Brackets.exe" are run. I plan on updating to allow the user to type in new processes, such as "Unreal.exe" or "Gamemaker.exe", without having to edit the python file. For now, it will remain as it is.

The seconds for each day of every month and year are also saved in the "this_graph.txt" file that gets created when it is run.

## Conclusion
I went to Windows Scheduler and had it run this with a 60s delay after any logon. Works splendidly!

Here's my actual productivity graphs from the past few months (This was finished in mid-April):

![Productivity graph](https://i.imgur.com/XLTSLCe.png)

![Productivity graph](https://i.imgur.com/IYdnov2.png)
