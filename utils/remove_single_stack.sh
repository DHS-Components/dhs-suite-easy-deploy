#!/bin/bash

docker stack ls | grep $1 | awk '{print $1}' | while read stackname

do
        docker stack rm $stackname

        if [ $? -eq 0 ]; then

                echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] $stackname removed "

        fi

done
