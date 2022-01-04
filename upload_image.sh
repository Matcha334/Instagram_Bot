#!/bin/sh

osascript <<EOS
    tell application "System Events"
        key code 102 -- 英数キー
        key code 44 -- スラッシュ
        keystroke "Users/serpent/Desktop/work/python/original_instagram_bot/download.jpg"
        key code 76 -- エンター
        key code 76 -- エンター
    end tell
    return
EOS