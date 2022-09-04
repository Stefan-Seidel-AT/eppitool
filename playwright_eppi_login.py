#!/usr/bin/env python3

# Author: Stefan Seidel 2022

# basic code used from introduction: "Login and Scrape Data with Playwright and
# Python" from John Watson Rooney(2021)
# https://www.youtube.com/watch?v=H2-5ecFwHHQ
# https://playwright.dev/docs/selectors#selecting-visible-elements

# install required modules in bash:
# pip3 install playwright
# playwright install
# pip3 install bs4


from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError # for web automation
import requests                                                              # for webrequests
from bs4 import BeautifulSoup                                                # data collection from websites
import re                                                                    # for regex
import argparse                                                              # parsing arguments from command line
import getpass                                                               # parsing password
import time
import show_stats                                                            # showing statistics of eppitransfer (custom module)

# parse arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument("-q", "--quiet",
                action="store_true", default=False,
                help="do not show actions of program in internet browser window")
parser.add_argument("-n", "--no_stats",
                action="store_true", default=False,
                help="do not add information to/or show stats file")

args = parser.parse_args()


# get user credentials from command line
user=input("Please insert user-name of your Eppoint account:\n")
password=getpass.getpass(prompt="Now please enter your password!\n")
print("Thank you!\n")

##############################################
# get eppoints from file
# eppoints from from file into an array

eppi_file = 'Eppicodes.txt'

# useing readlines
file1 = open(eppi_file, 'r')
Lines = file1.readlines()

count = 0
headers_of_eppifile = []
eppicodes_array = []
wrong_eppicodes_array = []

# strips newline character
for line in Lines:
    if re.match("^#.*", line):
        # parse headers of eppifile
        headers_of_eppifile.append(line)
    else:
        count +=1
        # capitalize as codes are only valid if in capital letters
        line = line.upper()
        eppicodes_array.append(line.strip())

# close file
file1.close()


# clear content of eppifile except the headers ('#') to
# get a clean file without eppicodes for next usage of program
file1 = open(eppi_file , 'w')
file1.writelines((headers_of_eppifile))
file1.close



#########################################################
# start browser and navigate through website

# switch for visible header: true by default
header = True

if args.quiet:
    print( "Program is running...")
    header = False

with sync_playwright() as p:

    if args.quiet:
        browser = p.chromium.launch(headless=True, slow_mo=50

            
    #### if proxy required adapt follwing code and remove last ")"  CAVE: NOT tested!!! #### 
    #       { proxy: { 
    #           server: 'http://myproxy.com:3128',
    #           username: 'usr',
    #           password: 'pwd'
    #                  }
    #     });
    ######################################################################
    
           )
    else:
        browser = p.chromium.launch(headless=False, slow_mo=100)

    page = browser.new_page()
    
    # set browserwindowsize
    page.set_viewport_size({"width": 960, "height": 720})
    
    # browse to loginpage
    page.goto('https://www.eppendorf.com/at-de/')
    page.goto('https://www.eppendorf.com/at-de/login')
    

    # confirm popup window to allow cookies 
    page.locator('#onetrust-accept-btn-handler').click()

    #set visible and fill field for "username"
    page.locator('input[name=j_username] >> visible=true').fill(user)

    #set visible and fill field for "password"
    page.locator('input[name=j_password] >> visible=true').fill(password)
    page.click('button#loginButton[type=submit]')

    # check if login successful
    #print(page.url)

    if (re.match(".*\?error.*", page.url)):
            print("\nOops! Username or Password are incorrect.\nPlease check your credentials and try again!")
            exit()

    #else: 
    page.goto('https://www.eppendorf.com/AT-de/discover/eppoints-portal/eppoints-start/')
    


    # now login to epPoints-portal
    #set visible and fill field for "user"
    page.locator('input[name=user] >> visible=true').fill(user)
    
    #set visible and fill field for "pass"
    page.locator('input[name=pass] >> visible=true').fill(password)
    page.click('button#loginButton[type=submit]')
    
    #page.goto('https://www.eppendorf.com/eppoints/')
    page.goto('https://www.eppendorf.com/AT-de/myeppendorf/eppoints/')
    #page.click()


    # testcase
    # eppicodes_array.append('Z3PU1DWKZJ')

    # get nr_of_eppicodes
    nr_of_eppicodes_all=len(eppicodes_array)

    # looping through the array containing eppicodes and post them to the website
    for i in eppicodes_array:
        code = i
        # fill in eppoints:
        page.locator('input#epInput >> visible=true').fill(code)
   
        # move mouse and click somewhere to enable dropdown menue
        page.mouse.move(0,0)
        page.mouse.down()
        page.mouse.click(0,0)

        try:
            # select dropdown: 
            page.select_option('select#epSelect', '696', timeout=100) # option: Dual Filter tips
        except PlaywrightTimeoutError:
            print ("Code incorrect:",i)
            # collect wrong codes
            wrong_eppicodes_array.append(i)
            next

    # read out eppoint balance:
    eppoint_balance = page.locator('div.epPointsRewardscategory_only.gutter-bottom-small').first
    
    # print("Eppoints Stand: ", eppoint_balance.inner_text() , "\n")
    
    # assign to variable
    eppoint_balance_clear = eppoint_balance.inner_text()
    array = eppoint_balance_clear.split(" ")
    print("\nYour current epPoint balance is:\n", array[-1] , " epPoints\n")


    #balance_text = eppoint_balance.inner_text()
    #print("bal text: ", re.match("^epPoints Stand [0-9]{2,4}", balance_text))
    
    # logout
    page.locator("text=Abmelden").click()

    # close browser
    browser.close()

if args.no_stats:

    # wait for user input
    print("press <Enter/Return> to continue...")
    input()

else:
    # show_stats requires statistics file (where stats are stored and
    # nr_of_eppoints transferred that run


    # get nr_of_eppicodes
    nr_of_eppicodes_transferred = nr_of_eppicodes_all - len(wrong_eppicodes_array)
    # print( "nr of eppicods: ", nr_of_eppicodes_transferred)
    
    # get nr_of_eppoints = nr_of_eppicodes times 10
    nr_of_eppicodes_transferred = nr_of_eppicodes_transferred*10

    show_stats.show_stats('stats.txt', nr_of_eppicodes_transferred)

    # wait for user input
    print("press <Enter/Return> to continue...")
    input()
    
    # check if login-logout successful
    # print(page.url)

    # for submitting eppoints:


      # now things to do: 
       # -read out epPoint balance
       # -fill in eppicodes!!!





