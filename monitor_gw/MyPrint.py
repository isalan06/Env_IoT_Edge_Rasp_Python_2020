#!/usr/bin/python3
#MyPrint.py

import os
from datetime import datetime

if os.getenv('C', '1') == '0':
    ANSI_RED = ''
    ANSI_GREEN = ''
    ANSI_YELLOW = ''
    ANSI_CYAN = ''
    ANSI_WHITE = ''
    ANSI_OFF = ''
else:
    ANSI_CSI = "\033["
    ANSI_RED = ANSI_CSI + '31m'
    ANSI_GREEN = ANSI_CSI + '32m'
    ANSI_YELLOW = ANSI_CSI + '33m'
    ANSI_CYAN = ANSI_CSI + '36m'
    ANSI_WHITE = ANSI_CSI + '37m'
    ANSI_OFF = ANSI_CSI + '0m'

def Print_Ori(message, color, title=''):
    textString = color

    textString += '@'
    textString += datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    textString += ' - '    

    if title != '':
        textString += '['
        textString += title
        textString += ']'
    
    textString += message
    textString += ANSI_OFF
    print (textString)

def Print(message):
    print(message)

def Print_Red(message, title=''):
    color_string = ANSI_RED
    Print_Ori(message, color_string, title)

def Print_Green(message, title=''):
    color_string = ANSI_GREEN
    Print_Ori(message, color_string, title)

def Print_Yellow(message, title=''):
    color_string = ANSI_YELLOW
    Print_Ori(message, color_string, title)

def Print_Cyan(message, title=''):
    color_string = ANSI_CYAN
    Print_Ori(message, color_string, title)

def Print_White(message, title=''):
    color_string = ANSI_WHITE
    Print_Ori(message, color_string, title)
