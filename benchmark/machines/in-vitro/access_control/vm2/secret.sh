#!/bin/bash 

echo $RANDOM | md5sum | head -c 20 > /dev/null

