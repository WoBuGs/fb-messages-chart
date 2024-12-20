import argparse
import json
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from rich_argparse import RichHelpFormatter
from tqdm.rich import tqdm

from utils import autolabel, natural_keys

# Set up argument parser
parser = argparse.ArgumentParser(
    description="Display statistics about a Messenger or Instagram conversation extract",
    formatter_class=RichHelpFormatter,
)

# Define arguments
parser.add_argument(
    "-w",
    dest="width",
    action="store",
    metavar="width",
    type=float,
    default=1,
    help="width of the rects (default=1)",
)
parser.add_argument(
    "-m",
    dest="min_month",
    action="store",
    metavar="min_month",
    type=int,
    default=0,
    help="month of the start date (default=0)",
)
parser.add_argument(
    "-y",
    dest="min_year",
    action="store",
    metavar="min_year",
    type=int,
    default=0,
    help="year of the start date (default=0)",
)
parser.add_argument(
    "-M",
    dest="max_month",
    action="store",
    metavar="max_month",
    type=int,
    default=9999,
    help="month of the end date (default=9999)",
)
parser.add_argument(
    "-Y",
    dest="max_year",
    action="store",
    metavar="max_year",
    type=int,
    default=9999,
    help="year of the end date (default=9999)",
)
parser.add_argument(
    "inputs",
    metavar="inputs",
    nargs="+",
    help="path of the conversations (json format), file or dir",
)
args = parser.parse_args()

# Extract arguments
width = args.width
min_month = args.min_month
min_year = args.min_year
max_month = args.max_month
max_year = args.max_year
inputs = args.inputs

# Collect input files
files = []
for input in inputs:
    if os.path.isdir(input):
        for subfile in os.listdir(input):
            files.append(input + "/" + subfile)
    else:
        files.append(input)

# Natural sort of input files (e.g., messages_1.json, messages_2.json, messages_10.json)
files.sort(key=natural_keys)

# Initialize variables
start = True
stats = {}
participants = []

# Process each file
for file in tqdm(files):
    f = open(file)
    data = json.load(f)
    messages = data["messages"]

    # Collect participants' names
    if start:
        for participant in data["participants"]:
            participants.append(participant["name"])
        start = False

    # Process each message
    for message in messages:
        sender = message["sender_name"]
        timestamp = int(message["timestamp_ms"] / 1000)
        year = datetime.fromtimestamp(timestamp).year
        month = datetime.fromtimestamp(timestamp).month

        # Filter messages by date range
        if year < min_year:
            continue
        if year <= min_year and month < min_month:
            continue
        if year > max_year:
            continue
        if year >= max_year and month > max_month:
            continue

        # Format month key
        month = str(year)[2:] + "-" + str(month).zfill(2)

        # Update stats
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

# Prepare data for plotting
p_list = {}
m_list = []
plots = []
participant_name_len_max = 0
for participant in participants:
    if participant_name_len_max < len(participant):
        participant_name_len_max = len(participant)
    p_list[participant] = []

# Organize stats by month
for month, stat in stats.items():
    for participant in participants:
        try:
            p = stat[participant]
        except:
            p = 0
        p_list[participant].insert(0, p)
    m_list.insert(0, month)

# Plot data
ind = np.arange(len(m_list)) * (1 + width * len(participants))
i = int((1 - len(participants)) / 2)
for participant in participants:
    p = plt.bar(ind + width * (i - 1 / 2), p_list[participant], width)
    autolabel(p)
    plots.append(p[0])
    i = i + 1
plt.ylabel("Messages")
plt.title("Messages per month")
plt.xticks(ind, m_list)
plt.legend(plots, participants)

# Print total messages per participant
total = 0
for participant in participants:
    sub = sum(p_list[participant])
    print(participant.ljust(participant_name_len_max + 1) + str(sub))
    total = total + sub
print()
print("Total messages: " + str(total))
plt.show()
