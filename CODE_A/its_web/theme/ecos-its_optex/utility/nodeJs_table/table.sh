#!/bin/bash
kill -9 $(pidof node table.js)
node table.js $1 $2 $3 &
echo "command [0/1]"
