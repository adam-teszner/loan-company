#! /usr/bin/bash
input=/home/ubuntu/.env

while read -r line
	do
		[[ "$line" =~ ^#.* ]] && continue
 		 export "$line"
	done < "$input"

echo $SECRET_KEY
