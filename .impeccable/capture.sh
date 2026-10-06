#!/bin/sh
# capture.sh <out.png> <width> <height> [url] : settled screenshot (reduced motion) of the static site
CH="/c/Program Files/Google/Chrome/Application/chrome.exe"
"$CH" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --force-prefers-reduced-motion \
  --window-size="$2,$3" --virtual-time-budget=9000 --screenshot="$(cygpath -w "$PWD/$1")" "${4:-http://127.0.0.1:8611/index.html}" >/dev/null 2>&1
