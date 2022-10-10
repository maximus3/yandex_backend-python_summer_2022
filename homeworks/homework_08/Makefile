test:
	docker-compose -f yandex_tank_test_one/docker-compose.yml up
	docker rm yandex_tank_test_one_tester_1

test-nginx:
	docker-compose -f yandex_tank_test_nginx/docker-compose.yml up
	docker rm yandex_tank_test_nginx_tester_1

tester-bash:
	docker run --rm -it --entrypoint /bin/bash --network="host" direvius/yandex-tank

docker-up: ## Docker up
	docker-compose up

docker-up-d: ## Docker up detach
	docker-compose up -d

docker-build: ## Docker build
	docker-compose build

docker-clean: ## Docker prune -f
	docker image prune -f

down: ## Docker down
	docker-compose down

up: docker-clean docker-build docker-up-d ## Docker prune, up detach, run