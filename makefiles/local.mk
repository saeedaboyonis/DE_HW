SHELL := /bin/bash

# Define the path to the makefiles directory for convenience
MAKEFILES_DIR := $(PWD)/makefiles

# Start the application using the local.start.sh script
local.start:
	@echo "Starting the application..."
	@bash $(MAKEFILES_DIR)/local.start.sh

# Stop the application using the local.stop.sh script
local.stop:
	@echo "Stopping the application..."
	@bash $(MAKEFILES_DIR)/local.stop.sh

# Rebuild the application environment using the local.rebuild.sh script
local.rebuild:
	@echo "Rebuilding the application environment..."
	@bash $(MAKEFILES_DIR)/local.rebuild.sh

# Initialize the application environment using the local.init.sh script
local.init:
	@echo "Initializing the application environment..."
	@bash $(MAKEFILES_DIR)/local.init.sh