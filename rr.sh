export $(cat /home/ubuntu/.env | sed -e /^$/d -e /^#/d | xargs)
