#!/bin/sh
wget https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz
tar -xzf geckodriver-v0.19.1-linux64.tar.gz
mv geckodriver /usr/local/bin
ls /usr/local/bin | grep gecko
echo $MOZ_CRASHREPORTER_SHUTDOWN
echo $DISPLAY
