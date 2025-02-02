#!/bin/bash

echo "Checking permissions for /dev/input/* devices..."

# checks if user has 'input' group permissions, otherwise adds the user for permissions
if groups $USER | grep -q "\binput\b"; then
    echo "User is already a member of the 'input' group."
else
    echo "Adding $USER to the 'input' group..."
    sudo usermod -aG input $USER
    echo "Log out and back in for the changes to take effect." 
fi

# sets temporary permissions for the current session
echo "Setting temporary read/write permissions for /dev/input/*"
sudo chmod a+rw /dev/input/*
echo "Setup complete. Run the script now." 
