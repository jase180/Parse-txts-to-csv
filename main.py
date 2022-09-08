#  This script loops through a directory named 'ABC' inside script directory.
#  'ABC' directory includes only .txt files that are emails including a request and info generated from mainframe
#  Specific information is to be parsed from each .txt file, stored in a list of lists, and written to a csv as out

import csv
import re
import os

# function that uses regex to look for line written by human, therefore regex case insensitive in case of error
# Line always starts with same phrase.
# Puts all matched lines into a list, and returns first match only since it would be latest of email correspondence
def findfruit(txt):
    matched_lines = []
    linenum = 0
    pattern = "(?i)BeSt fRuIts"
    for line in txt:
        linenum += 1
        if re.search(pattern, line) is not None:  # If pattern search finds a match,
            matched_lines.append((linenum, line.rstrip('\n')))
    match = matched_lines[0][1].split()  # [0] to only take first match in entire txt
    fruit = ' '.join(match[2:])
    return fruit

# function that uses regex to look for lines starting with 'GREATEST ..." within mainframe generated text
# Line always starts with same phrase.
# Puts all matched lines into a list, returns maximum of floats found
def findgreatest(txt):
    matched_lines = []  # for debugging if req'd
    ls_numbers = []  # ls of all found max numbers
    linenum = 0
    pattern = 'GREATEST NUMBER OF FRUITS IS'
    for line in txt:
        linenum += 1  # count lines
        if re.search(pattern, line) is not None:  # If pattern found in line, strip line and append lists
            matched_lines.append(linenum)
            linels = line.split()
            number = linels[3]
            ratings.append(number)

    # Find and return greatest rating in rating ls
    greatest = 0
    for n in ls_numbers:
        if float(n) > greatest:
            greatest = float(n)

    return greatest

# function that uses regex to look for lines containing keyword within mainframe generated text
# multiple information to be parsed is around search line.  only first match is required since it would be latest
# Puts all required information into a list and returns list

def findmost(txt):
    matched_lines = []
    lst = []
    linenum = 0
    pattern = re.compile('BANANAS')
    for line in txt:
        linenum += 1
        if pattern.search(line) is not None:  # If pattern search finds a match,
            matched_lines.append(linenum)
    match = matched_lines[0]  # locate 286,000 which is locator that never changes, first entry for newest file in email chain
    apples_oranges_line = match - 11
    grapes = match - 9
    cherries = match - 7
    date = match - 13
    cherries_out = txt[cherries].split()[4]
    grapes_out = txt[grapes].split()[3]
    apples_out = ' '.join(txt[apples_oranges_line].split()[0:2])
    oranges_out = txt[apples_oranges_line].split()[2]
    date_out = ' '.join(txt[date].split()[4:6])
    return [date_out, '', apples_out, grapes_out, cherries_out, oranges_out]

# equivalent to main
out_list = []  # generate output list to write to csv file

# loop through directory containing required txts.  Each loop generates a list called ls and adds all find functions
# into list.
for file in os.listdir('ABC'):
    with open(os.path.join('ABC', file), 'r') as f:
        print("starting " + file)
        txt = []  # read text into a list
        for line in f:
            txt.append(line)

        ls = findmost(txt)
        ls.insert(2, findfruit(txt))
        ls.insert(6, findgreatest(txt))

        out_list.append(ls)

        print(file + " completed")

# write to csv file
with open('output.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    for ls in out_list:
        writer.writerow(ls)

print("Parse completed")