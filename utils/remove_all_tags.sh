#!/bin/bash
docker node ls | grep -v HOSTNAME | sed 's/\*//' | awk '{print $2}' | while read node 

do

docker node inspect $node --format '{{ .Spec.Labels }}' | awk -F"[" '{print $2}' |awk -F"]" '{print $1}'|  awk -F '[: ]' '{for (i=1; i<=NF; i+=2) print $i}' | while read tag 
	
	do
	
	docker node update --label-rm $tag $node  > /dev/null 2>&1
	
	if [ $? -eq 0 ]; then 

		echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] $tag removed from node $node"

	fi
	
	done

done
