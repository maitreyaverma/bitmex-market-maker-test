#!/bin/bash
a='https://s3-eu-west-1.amazonaws.com/public.bitmex.com/data/quote/'
date=$1
full_url="${a}${date}.csv.gz"
file_compressed="${date}.csv.gz"
file="${date}.csv"
axel -n 10 $full_url
gunzip $file_compressed
mv ${file} market_maker/backtest/data
python runBackTest.py XBTUSD ${date}.csv>${date}
