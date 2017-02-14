#!/usr/bin/env bash

cd /crawl_film/
slist=$(scrapy list)

while :
do
    for element in ${slist##* }
    do
       scrapy crawl "$element" -s LOG_FILE=logs/"$element"_`date +%Y-%m-%d"_"%H-%M-%S`.log
    done
    sleep 1d

done
