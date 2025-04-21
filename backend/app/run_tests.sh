#!/bin/bash
# Explicitly activate the virtual environment
source /app/venv/bin/activate
# Run pytest
pytest tests/services/test_prompt_service.py
