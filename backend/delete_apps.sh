#!/bin/bash
# Script to delete the old apps/ directory structure

echo "Removing old apps/ directory..."

# Remove all files in apps/
find backend/apps -type f -delete
find backend/apps -type d -empty -delete

echo "Done!"
