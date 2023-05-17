.PHONY: build run ssh clean

build:
	docker-compose build

run:
	docker-compose up -d

ssh:
	docker-compose exec python-app bash

clean:
	docker-compose down --volumes
