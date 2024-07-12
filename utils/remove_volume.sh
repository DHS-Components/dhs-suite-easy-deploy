#!/bin/bash
docker volume ls | grep $1 | awk '{print $2}' | while read volume

do
	
	docker volume rm $volume > /dev/null 2>&1
	
	if [ $? -eq 0 ]; then 

		echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] volume $volume removed "

	fi
	
done
