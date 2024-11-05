#!/bin/bash
d="1"
command -v docker >/dev/null || d="0"
if [[ "$d" == "0" ]];then
	echo 'docker is not installed'
else
	docker build -t khatamat:latest .
	docker run khatamat:latest
fi

