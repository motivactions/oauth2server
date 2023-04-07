test:
	coverage run manage.py test -v 2
	
serve:
	python manage.py runserver 8000
	
tunnel:
	python ./scripts/dev_tunnel.py -l 8000 -d oauth2

celery-beat:
	celery -A server beat -l INFO  --scheduler django_celery_beat.schedulers:DatabaseScheduler

celery-worker:
	celery -A server worker -l INFO

rsa-private-key:
	openssl genrsa -out privatekey.pem 2048

rsa-public-key:
	openssl rsa -in privatekey.pem -out publickey.pem -pubout -outform PEM
