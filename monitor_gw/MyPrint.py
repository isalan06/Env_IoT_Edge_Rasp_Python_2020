#!/usr/bin/python3
#MyPrint.py

import os

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

def Print_Ori(message, color):
    textString = color
    textString += message
    textString += ANSI_OFF
    print (textString)

def Print(message):
    print(message)

def Print_Red(message):
    color_string = ANSI_RED
    Print_Ori(message, color_string)

def Print_Green(message):
    color_string = ANSI_GREEN
    Print_Ori(message, color_string)

def Print_Yellow(message):
    color_string = ANSI_YELLOW
    Print_Ori(message, color_string)

def Print_Cyan(message):
    color_string = ANSI_CYAN
    Print_Ori(message, color_string)

def Print_White(message):
    color_string = ANSI_WHITE
    Print_Ori(message, color_string)
