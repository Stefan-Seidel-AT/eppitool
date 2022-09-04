#!/usr/bin/env python3


# This takes name of the logfile and number of eppoints submitted and
# stores them in the logfile together with the current date. A plot is created
# that shows the amount of eppoints submitted over time

import matplotlib.pyplot as plt     # for plotting
import numpy as np                  # for arrayhandling
import re                           # for regex
from datetime import date           # for optaining date/time
from statistics import mean         # for statistics

def show_stats(logfile, nr_of_eppoints):
    logfile = 'stats.txt'
    today = date.today()
    #eppoints = '72'
    eppoints = nr_of_eppoints

    # read from statsfile with option to write
    in_file = open(logfile, 'r')
    Lines = in_file.readlines()

    # close file after extraction of info
    in_file.close()

    info_dict = []
    date_and_points = []
    a_date = []

    a_submitted_points = []


    # reading in statsfile and store information
    for line in Lines:
        if re.match('^#.*',line):
            if re.match('times\s+', line):
                a_usage_counter = line.split(':',line)
                s_usage_counter = a_usage_counter[1]
                print ("s_usage_counter = ", s_usage_counter)
            next
        else:
            date_and_points = line.split()

            # fill date and points into array
            a_date.append(date_and_points[0])
        
            # temp variable for adding number to list
            sub_eppoint=date_and_points[1]
            a_submitted_points.append(int(sub_eppoint))


# add information from current run #########################

    # set date format and define as string
    date_today = str(today.strftime("%d-%b-%Y"))
    a_date.append(date_today)

# eppoints
    sub_eppoint=eppoints
    a_submitted_points.append(int(sub_eppoint))


    # get lenght of array
    array_len = len(a_date)

# control statement
# print ( "date: ", a_date)

# set as integers
#print ( "points: ",a_submitted_points)
#print ( "convert to numpy integer ")

    # plot statistics:
    print( " Statistics to eppoint submission:")
    average = mean(a_submitted_points)
    average = int(average)

    print( "average_points_submitted/submission: ", average )


##################################################

    # append current data to logfile
    in_file = open(logfile, 'a')

    # store current date and current submitted eppoints:
    c_date = str(a_date[-1])
    c_submitted_points = str(a_submitted_points[-1])

    # format for writing to file
    current_date_points = c_date+"\t"+c_submitted_points+"\n"

    # append to and close logfile
    in_file.write(current_date_points)
    in_file.close()

##########################################################

#######################
# create plot
#######################
    fig = plt.figure()

    ax = fig.add_subplot()
    x = a_date
    y = a_submitted_points
    plt.plot(x, y, marker = '.')
    plt.title("Eppoints submitted over time\n on date")

    # x-axis labeling
    plt.xlabel("Date")

    # set to 5 shown x-labels
    nr_of_unique_date = set(a_date)
    number_of_ticklabel_steps=(len(nr_of_unique_date)/5)
    ax.set_xticks(np.arange(0, len(nr_of_unique_date)+1, number_of_ticklabel_steps))

    # y-Axis labeling
    plt.ylabel("Eppoints submitted")
    plt.autoscale()
    plt.show()

    # wait to close plot
    #plt.waitforbuttonpress(0)
    plt.close('all')

