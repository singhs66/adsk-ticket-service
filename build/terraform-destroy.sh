#!/bin/bash
cd "$(dirname "$0")/../infrastructure" || exit 1
terraform apply --destroy
