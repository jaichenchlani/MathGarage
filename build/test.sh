#!/bin/bash

# Source the utils shell script
source $HOME/playground/automation/myscripts/utils.sh
source $HOME/playground/automation/myscripts/utilities.sh

# build_folder=$(jq -r '.build_folder' mathgarageconfig.json)
# app_name=$(jq -r '.app_name' mathgarageconfig.json)
# app_version=$(jq -r '.app_version' mathgarageconfig.json)

# echo $build_folder
# echo $app_name
# echo $app_version

# e_header "I am a sample script"
# e_arrow "I am an arrow message"
# e_success "I am a success message"
# e_error "I am an error message"
# e_warning "I am a warning message"
# e_underline "I am underlined text"
# e_bold "I am bold text"
# e_note "I am a note"

# present_directory=$(pwd)
# echo $present_directory

gcloud init
status=$?

echo $status

