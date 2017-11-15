#!/bin/sh
wget https://github.com/mozilla/geckodriver/releases/download/v0.11.1/geckodriver-v0.11.1-linux64.tar.gz
mkdir geckodriver
tar -xzf geckodriver-v0.11.1-linux64.tar.gz -C geckodriver
export PATH=$PATH:$PWD/geckodriver
