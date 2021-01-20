import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime
from autolabel import autolabel
import argparse

parser = argparse.ArgumentParser(description='Display statistics about a Messenger or Instagram conversation extract')
parser.add_argument('-w', dest='width', action='store', metavar='width', type=float, default=1, help='width of the rects [default=1]')
parser.add_argument('-m', dest='min_month', action='store', metavar='min_month', type=int, default=0, help='month of the start date [default=0]')
parser.add_argument('-y', dest='min_year', action='store', metavar='min_year', type=int, default=0, help='year of the start date [default=0]')
parser.add_argument('-M', dest='max_month', action='store', metavar='max_month', type=int, default=9999, help='month of the end date [default=9999]')
parser.add_argument('-Y', dest='max_year', action='store', metavar='max_year', type=int, default=9999, help='year of the end date [default=9999]')
parser.add_argument('files', metavar='files', nargs='+',help='path of the conversations (json format)')
args = parser.parse_args()

width = args.width
min_month = args.min_month
min_year = args.min_year
max_month = args.max_month
max_year = args.max_year
files = args.files


start = True
stats = {}
participants = []
for file in files:
    f = open(file)
    data = json.load(f)
    messages = data["messages"]

    if start:
        for participant in data["participants"]:
            participants.append(participant["name"])
        start = False

    for message in messages:
       sender = message["sender_name"]
       timestamp = int(message["timestamp_ms"]/1000)
       year = datetime.fromtimestamp(timestamp).year
       month = datetime.fromtimestamp(timestamp).month

       if year < min_year:
          continue
       if year <= min_year and month < min_month:
          continue
       if year > max_year:
          continue
       if year >= max_year and month > max_month:
          continue

       month = str(year)[2:] + "-" + str(month).zfill(2)

       try:
           old = stats[month]
           try:
               s = old[sender]
               stats[month][sender] = stats[month][sender] + 1
           except:
               stats[month][sender] = 1
       except:
           stats[month] = {sender: 1}
    f.close()

p_list = {}
m_list = []
plots = []
participant_name_len_max = 0
for participant in participants:
    if participant_name_len_max < len(participant):
        participant_name_len_max = len(participant)
    p_list[participant] = []

for month, stat in stats.items():
    for participant in participants:
        try:
            p = stat[participant]
        except:
            p = 0
        p_list[participant].insert(0, p)
    m_list.insert(0, month)

ind = np.arange(len(m_list))*(1+width*len(participants))
i = int((1 - len(participants))/2)
for participant in participants:
    p = plt.bar(ind+width*(i-1/2), p_list[participant], width)
    autolabel(p)
    plots.append(p[0])
    i = i + 1
plt.ylabel('Messages')
plt.title('Messages per month')
plt.xticks(ind, m_list)
plt.legend(plots, participants)

total = 0
for participant in participants:
    sub = sum(p_list[participant])
    print(participant.ljust(participant_name_len_max+1) + str(sub))
    total = total + sub
print()
print("Total messages: " + str(total))
plt.show()
