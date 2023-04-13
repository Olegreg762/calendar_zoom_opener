import webbrowser
from datetime import datetime
import time
import re

# Set today's date
now_date = datetime.now().strftime('%Y-%m-%d')
now_time = datetime.now().strftime('%H:%M')

# Define time to open Zoom link
zoom_time =datetime.strptime('18:29', '%H:%M').strftime('%H:%M')


# Define a dictionary to store the links by date
links_by_date = {}

# Open the calendar file
with open('your_file_here', 'r') as ics_file:
    # read the lines of the file
    lines = ics_file.readlines()

# Concatenate wrapped lines
lines = [line.strip() for line in lines]
for i in range(len(lines)-1):
    if lines[i].endswith('='):
        lines[i] = lines[i][:-1] + lines[i+1]
        lines[i+1] = ''

# Loop through the lines and search for those that contain a Zoom link
for line in lines:
    if re.search(r'DTSTART:', line):

        dt_str = (line.strip('DTSTART:'))
        dt_obj = datetime.strptime(dt_str, '%Y%m%dT%H%M%SZ')
        date_str = dt_obj.date().isoformat()

    if re.search(r'zoom\.us/', line):
        link=line.strip('X-ALT-DESC;FMTTYPE=text/html:<p><a href=').replace('"', '')
        # Add the link to the dictionary under the corresponding date
        if date_str not in links_by_date:
            links_by_date[date_str] = []
        links_by_date[date_str].append(link)

# Variable that when set to 'True' by upcoming while loop will allow loop to end.
link_opened = False

while now_time <= zoom_time and not link_opened:
    now_time = datetime.now().strftime('%H:%M')
    print('Not Time Yet!')
    time.sleep(10)
# Check if today's date is a key in the dictionary
    if now_date in links_by_date:
        # Checks if today's date is a key if so open the corresponding Zoom link
        zoom_links = links_by_date[now_date]
        for link in zoom_links:
            webbrowser.open(link)
            link_opened = True
            break
    else:
        # If today's date is not a key, print a message that there are no Zoom links for today
        print('No Zoom links for today')
        break
