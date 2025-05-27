#!/bin/bash
#Set working directory to the infrastructure folder relative to the project root
cd "$(dirname "$0")/../infrastructure" || exit 1
terraform init
