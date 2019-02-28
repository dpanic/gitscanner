#!/usr/bin/python
import sys


# define BLACK   "\033[30m"      /* Black */
# define RED     "\033[31m"      /* Red */
# define GREEN   "\033[32m"      /* Green */
# define YELLOW  "\033[33m"      /* Yellow */
# define BLUE    "\033[34m"      /* Blue */
# define MAGENTA "\033[35m"      /* Magenta */
# define CYAN    "\033[36m"      /* Cyan */
# define WHITE   "\033[37m"      /* White */
# define BOLDBLACK   "\033[1m\033[30m"      /* Bold Black */
# define BOLDRED     "\033[1m\033[31m"      /* Bold Red */
# define BOLDGREEN   "\033[1m\033[32m"      /* Bold Green */
# define BOLDYELLOW  "\033[1m\033[33m"      /* Bold Yellow */
# define BOLDBLUE    "\033[1m\033[34m"      /* Bold Blue */
# define BOLDMAGENTA "\033[1m\033[35m"      /* Bold Magenta */
# define BOLDCYAN    "\033[1m\033[36m"      /* Bold Cyan */
# define BOLDWHITE   "\033[1m\033[37m"      /* Bold White */

class bcolors:
    HEADER = '\033[1m\033[37m'
    OKBLUE = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
    



def dump(msg, msg_type):
    try:
        msg = str(msg)
    except:
        pass
    

    try:
        msg = msg.decode('utf8', errors='ignore')
    except:
        pass
    

    try:
        if msg_type == "critical": 
            print(bcolors.FAIL + msg + bcolors.ENDC)
        

        if msg_type == "warning": 
            print(bcolors.WARNING + msg + bcolors.ENDC)
        

        if msg_type == "error":
            print(bcolors.FAIL + msg + bcolors.ENDC)
        

        if msg_type == "info":
            print(bcolors.OKBLUE + msg + bcolors.ENDC)
        

        if msg_type == "good":
            print(bcolors.OKGREEN + msg + bcolors.ENDC)
        

        if msg_type == "debug":
            print(bcolors.HEADER + msg + bcolors.ENDC)
        
    except:
        pass
    

