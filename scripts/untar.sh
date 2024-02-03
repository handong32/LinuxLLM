#!/bin/bash

# Function to untar a file and rename the folder
untar() {
    local file="$1"
    local target_dir="$2"
    local folder_name="$(basename "$file" .tar.gz)"

    echo "$file $target_dir $folder_name"
    #mkdir -p "$target_dir"
    tar -xzf "$file" -C "$target_dir"
    mv "$target_dir/linux" "$target_dir/$folder_name"
}

# Function to process directories
process_directory() {
    local dir="$1"

    for file in "$dir"/linux*.tar.gz; do
	if [ -f "$file" ]; then
	    echo "Untarring: $file"
	    untar "$file" "$dir"
	fi
    done

    for subdirectory in "$dir"/*; do
	if [ -d "$subdirectory" ]; then
	    process_directory "$subdirectory"
	fi
    done
}

# Check for command-line argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Start processing from the specified directory
target_directory="$1"
if [ -d "$target_directory" ]; then
    process_directory "$target_directory"
else
    echo "Error: Directory not found."
fi
