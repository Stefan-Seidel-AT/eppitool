# Eppitool

##################################################################################
## Information for the End user:  ##
######################################
# If you use this program package you agree that this software comes with NO WARRANTY and 
# NO LEGAL CLAIMS can be derived towards the author. Feel free to share and use responsibly.

 The program "playwright_eppi_login.py" accesses an user account after providing
 "username" and "password" of your Eppendorf account at  the Eppendorf homepage
  ( https://www.eppendorf.com/at-de/ ) and enters "Eppoint-codes" stored in one 
 column in the "Eppicodes.txt" file.
 Please keep in mind that this walkthough is written for Linux based environments

 Therefore please make sure that the "Eppicodes.txt"-file
        - is stored in the same folder as the executable "playwright_eppi_login.pl"
        - the "Eppicode.txt"-file must NOT be renamed!
        - follow the instructions in the "Eppicodes.txt" file for entering the format
          of the codes

 after you have entered the codes into the Eppicode file, save it.
 execute playwright_eppi_login.py by entering "./playwright_eppi_login.py" to the command line

 The codes are automatically submitted to the webservice and after the file
 processed, the codes are deleted and the application logs out from the
 user account. Further the actual credits are shown on the terminal.




#####################################################################################
## requirements to run:   ##
############################

stored in same folder:
- "playwright_eppi_login.py" -> executable file
- "show_stats.py" -> executable file
- "Eppicode.txt" -> text file where you enter your Eppoint codes (without spaces!) (has to be read- and writeable)
- "stats.txt" -> text file where the stats are stored (has to be read- and writeable)


You need a pyhton interpreter to run and following modules that you can download using pip:

 install required modules in bash:
 pip3 install playwright
 playwright install
 pip3 install bs4


and maybe these modules if not already installed on your pc
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError # for web automation
import requests                                                              # for webrequests
from bs4 import BeautifulSoup                                                # data collection from websites
import re                                                                    # for regex
import argparse                                                              # parsing arguments from command line
import getpass                                                               # parsing password
import time
import show_stats                                                            # showing statistics of eppitransfer (custom module)



!!!! if you access the internet via a proxy_server you need to change the script:
CAVE: !!! this has not been tested yet !!!
- delete the first '#' in the beginning of the line in line 97 to line 102
- update the username and password for the proxyserver


#####################################################################

for further questions or input please mailto: "stefan_seidel@gmx.at"

######################################################################
