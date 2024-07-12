#!/bin/bash
docker stack ls | grep -v NAME | awk '{print $1}' | while read stack 

do
	docker stack rm $stack
	
	if [ $? -eq 0 ]; then 

		echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] $stack removed "

	fi

done
