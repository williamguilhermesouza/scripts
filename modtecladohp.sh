#! /bin/bash

# to use with HP wireless keyboard
xmodmap -e "keycode 61 = dead_tilde dead_circumflex"
xmodmap -e "keycode 97 = semicolon colon"


# to use with notebook keyboard
# xmodmap -e "keycode 61 = semicolon colon dead_tilde"
# xmodmap -e "keycode 97 = slash question degree"

