#!/bin/bash
docker node ls | grep -v HOSTNAME | sed 's/\*//' | awk '{print $2}' | while read node 

do
	
	docker node update --label-rm $1 $node  > /dev/null 2>&1
	
	if [ $? -eq 0 ]; then 

		echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] $1 removed from node $node"

	fi
	
done
