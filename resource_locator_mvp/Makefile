SHELL := /bin/bash

.PHONY: run install check test

# Start the development server using the py310 conda environment.
run:
	@echo "Starting development server (py310)..."
	@source $(HOME)/miniconda3/etc/profile.d/conda.sh && conda activate py310 && python manage.py runserver 0.0.0.0:8082

# Install Python dependencies into the active environment (expects py310 activated),
# or use `make install CONDA_ENV=py310` to install into a named conda env.
install:
	@echo "Installing dependencies into active environment..."
	@pip install -r requirements.txt

check:
	@echo "Running Django system checks..."
	@python manage.py check

test:
	@echo "(No automated tests configured)"
