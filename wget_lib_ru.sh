#!/bin/sh
wget --wait=5 --waitretry=10 --limit-rate=50K --recursive --no-parent\
  --user-agent=Mozilla --continue --no-clobber az.lib.ru
