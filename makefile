.PHONY: help start stop init rebuild create-dirs set-permissions

# Display this help text
help:
	@echo "Usage:"
	@echo "  make [command]"
	@echo "Commands:"
	@echo "  start       		Start all services in detached mode"
	@echo "  stop        		Stop all services and remove containers"
	@echo "  init        		Initialize the environment, create directories, set permissions, and start Airflow initialization"
	@echo "  rebuild     		Rebuild the environment, recreate and rebuild all services"
	@echo "  create-dirs 		Create required directories for the project"
	@echo "  set-permissions 	Set proper permissions for project directories"

start: local.start

stop: local.stop

init: create-dirs set-permissions local.init

rebuild: create-dirs set-permissions local.rebuild


create-dirs:
	mkdir -p ./data ./logs

set-permissions:
	chmod -R 777 ./logs
	chmod -R 777 ./data

include makefiles/local.mk