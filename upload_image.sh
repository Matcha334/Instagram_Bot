#!/bin/sh

osascript <<EOS
    tell application "System Events"
        key code 102 -- 英数キー
        delay 1
        key code 44 -- スラッシュ
        delay 1
        keystroke "Users/hamadakanako/Desktop/instagram_hashtag2auto_likes_tool-master/download.jpg"
        delay 1
        key code 76 -- エンター
        delay 1
        key code 76 -- エンター
    end tell
    return
EOS