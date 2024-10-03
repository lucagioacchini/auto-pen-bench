BENCHMARK := benchmark
MACHINES := $(BENCHMARK)/machines
SOLUTIONS := $(BENCHMARK)/solutions
MILESTONES := $(BENCHMARK)/milestones
CMD_MILESTONES := $(MILESTONES)/command_milestones
STG_MILESTONES := $(MILESTONES)/stage_milestones

build:
	$(eval DC := $(shell find benchmark -name 'docker-compose.yml' -print0 | xargs -0 -I {} echo "-f {}" | grep -v "benchmark/machines/docker-compose.yml"))
	docker-compose -f benchmark/machines/docker-compose.yml $(DC) build

install:build
	setup/setup.sh

test:
	@docker-compose -f benchmark/machines/docker-compose.yml -f benchmark/machines/$(category)/$(task_type)/docker-compose.yml build
	@python3 benchmark/tests/machine_test.py $(category) $(task_type) $(vm)

create:
	@$(MAKE) create_structure CATEGORY=$(category) TASK_TYPE=$(task_type) VM=$(vm)

# Helper function to pass the positional arguments
create_structure: 
	@echo "Creating directories for $(CATEGORY), $(TASK_TYPE), $(VM)..."
	@$(MAKE) $(MACHINES)/$(CATEGORY)/$(TASK_TYPE)/vm$(VM)/done CATEGORY=$(CATEGORY) TASK_TYPE=$(TASK_TYPE) VM=$(VM)


# Check if CATEGORY folder exists, if not, create it
$(MACHINES)/$(CATEGORY):
	mkdir -p $(MACHINES)/$(CATEGORY)
	mkdir -p $(CMD_MILESTONES)/$(CATEGORY)
	mkdir -p $(STG_MILESTONES)/$(CATEGORY)
	mkdir -p $(SOLUTIONS)/$(CATEGORY)


# Check if TASK_TYPE folder exists inside CATEGORY, if not, create it
$(MACHINES)/$(CATEGORY)/$(TASK_TYPE): $(MACHINES)/$(CATEGORY)
	mkdir -p $(MACHINES)/$(CATEGORY)/$(TASK_TYPE)
	mkdir -p $(CMD_MILESTONES)/$(CATEGORY)/$(TASK_TYPE)
	mkdir -p $(STG_MILESTONES)/$(CATEGORY)/$(TASK_TYPE)
	mkdir -p $(SOLUTIONS)/$(CATEGORY)/$(TASK_TYPE)

	python3 setup/manage_docker_compose.py create $(BENCHMARK) $(CATEGORY) $(TASK_TYPE) $(VM)


# Check if VM folder exists inside TASK_TYPE, if not, create it
$(MACHINES)/$(CATEGORY)/$(TASK_TYPE)/vm$(VM): $(MACHINES)/$(CATEGORY)/$(TASK_TYPE)
	# Create empty Dockerfile and flag for the machine to develop
	mkdir -p $(MACHINES)/$(CATEGORY)/$(TASK_TYPE)/vm$(VM)
	touch $(MACHINES)/$(CATEGORY)/$(TASK_TYPE)/vm$(VM)/flag.txt
	touch $(MACHINES)/$(CATEGORY)/$(TASK_TYPE)/vm$(VM)/Dockerfile
	
	# Create empty files for milestones and solutions
	touch $(CMD_MILESTONES)/$(CATEGORY)/$(TASK_TYPE)/vm$(VM).txt
	touch $(STG_MILESTONES)/$(CATEGORY)/$(TASK_TYPE)/vm$(VM).txt
	touch $(SOLUTIONS)/$(CATEGORY)/$(TASK_TYPE)/vm$(VM).txt

	# Update the docker-compose with a default service
	python3 setup/manage_docker_compose.py update $(BENCHMARK) $(CATEGORY) $(TASK_TYPE) $(VM)
	# Udate the input file
	python3 setup/manage_input_data.py $(CATEGORY) $(TASK_TYPE) $(VM)


# Final target to ensure VM exists and 'done' file is created
$(MACHINES)/$(CATEGORY)/$(TASK_TYPE)/vm$(VM)/done: $(MACHINES)/$(CATEGORY)/$(TASK_TYPE)/vm$(VM)
	@echo "All folders created. Doing final task in $(VM)..."

# Set variables to hold positional parameters from MAKECMDGOALS
category := $(word 2, $(MAKECMDGOALS))
task_type := $(word 3, $(MAKECMDGOALS))
vm := $(word 4, $(MAKECMDGOALS))

# Prevent 'create' from being confused with the folder names
%:
	@:
