#!/bin/bash

# Check if the pkill command is available
if ! command -v pkill &> /dev/null; then
    echo "pkill command not found. Please install pkill or use an alternative method."
    exit 1
fi

# Use pkill to send a SIGKILL signal to all processes named "qemu-x86_64"
pkill -9 -f "qemu-x86_64"

# Check if any processes are still running
if [ $? -eq 0 ]; then
    echo "All processes named 'qemu-x86_64' have been terminated with SIGKILL (signal 9)."
else
    echo "No processes named 'qemu-x86_64' were found."
fi

