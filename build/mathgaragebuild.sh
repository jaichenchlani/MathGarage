#!/bin/bash

# Build and Deploy Mathgarage App

# Source the utils shell script
source utilities.sh

e_header "Mathgarage Build Script Start"

# Parse the Config filename from the passed Arguments
if [ -z "$1" ]; then
    e_error "Config file name is a mandatory parameter."
    exit 1
else
    config_file_name=$1
fi

# Validate the config file existence. 
if check_file_exists ${config_file_name}; then
    e_success "${config_file_name} exists."
else
    e_error "${config_file_name} does not exist. Please retry with a valid file name. Exiting."
    exit 1
fi

e_warning "Reading Mathgarage config parameters..."

# Read and Validate Build Folder
build_folder=$(jq -r '.build_folder' $config_file_name)
if [ -z ${build_folder} ]; then
    e_error "Build folder is a required config parameter. Exiting."
    exit 1
fi

# Read and Validate App Name
app_name=$(jq -r '.app_name' $config_file_name)
if [ -z ${app_name} ]; then
    e_error "App Name is a required config parameter. Exiting."
    exit 1
fi

# Read and Validate App Version
app_version=$(jq -r '.app_version' $config_file_name)
if [ -z ${app_version} ]; then
    e_error "App Version is a required config parameter. Exiting."
    exit 1
fi

# Read and Validate GCP Project ID
gcp_project_id=$(jq -r '.gcp_project_id' $config_file_name)
if [ -z ${gcp_project_id} ]; then
    e_error "GCP Project ID is a required config parameter. Exiting."
    exit 1
fi

# Read and Validate GCR Image Prefix
gcr_image_prefix=$(jq -r '.gcr_image_prefix' $config_file_name)
if [ -z ${gcr_image_prefix} ]; then
    e_error "GCP Image Prefix is a required config parameter. Exiting."
    exit 1
fi

# Read and Validate the Build Flag
build_flag=$(jq -r '.build_flag' $config_file_name)
if [ -z ${build_flag} ]; then
    # Assume 0 (i.e. Do the Build.)
    build_flag=0
fi
# Read and Validate the Deploy Flag
deploy_flag=$(jq -r '.deploy_flag' $config_file_name)
if [ -z ${deploy_flag} ]; then
    # Assume 0 (i.e. Do the Deploy.)
    deploy_flag=0
fi

e_success "Read Mathgarage config parameters."

# Validate the Build Folder existence
if check_folder_exists $HOME/${build_folder}; then
    e_success "$HOME/${build_folder} exists."
else
    e_error "$HOME/${build_folder} does not exist. Please retry with a valid path. Exiting."
    exit 1
fi

e_success "Starting Mathgarage Build..."

e_success "Navigate to mathgarage folder."
cd $HOME/${build_folder}

e_warning "Pulling the latest code from master branch..."
git pull origin master
if [ $? -ne 0 ]; then
    e_error "Error pulling the latest code from Github. Exiting."
    exit 1
else
    e_success "Pulled the latest code from GitHub."
fi

e_warning "Building helper variable names for Docker commands..."
# Build the app_tag name using parameters from config
app_tag+=$app_name
app_tag+=":"
app_tag+=$app_version

# Build the gcr_image name using parameters from config
gcr_image+=$gcr_image_prefix
gcr_image+="/"
gcr_image+=$gcp_project_id
gcr_image+="/"
gcr_image+=$app_tag
e_success "Helper variables build completed successfully."

# Check the build flag, and proceed/skip with build.
if [ ${build_flag} -eq 1 ]; then
    # Proceed with Build, Tag and Push
    # Initiating Docker Build (Example: "docker build -t mathgarage:v0.94 .")
    e_warning "Docker Build in progress..."
    docker build -t ${app_tag} .
    if [ $? -ne 0 ]; then
        e_error "Error encounered during Docker Build. Exiting."
        exit 1
    else
        e_success "Docker build completed successfully."
    fi

    # Initiating Docker Tag (Example: "docker tag mathgarage:v0.94 gcr.io/mathgarage/mathgarage:v0.94")
    e_warning "Docker Tag in progress..."
    docker tag ${app_tag} ${gcr_image}
    if [ $? -ne 0 ]; then
        e_error "Error encounered during Docker Tag. Exiting."
        exit 1
    else
        e_success "Docker tag completed successfully."
    fi

    # Initiating Docker Push (Example: "docker push gcr.io/mathgarage/mathgarage:v0.94")
    e_warning "Docker Push to push the image to Google Container registry in progress..."
    docker push ${gcr_image}
    if [ $? -ne 0 ]; then
        e_error "Error encounered during Docker Push. Exiting."
        exit 1
    else
        e_success "Docker push completed successfully."
    fi
else
    e_warning "Skipping the Build, based on config parameter."
fi

# Check the deploy flag, and proceed/skip with deploy.
if [ ${deploy_flag} -eq 1 ]; then
    # Initiating Deploy to GAE
    e_warning "GAE Deployment in progress..."
    gcloud app deploy
    if [ $? -ne 0 ]; then
        e_error "Error encounered during GAE Deployment. Exiting."
        exit 1
    else
        e_success "GAE Deployment completed successfully."
    fi
else
    e_warning "Skipping the Deploy, based on config parameter."    
fi

e_header "Mathgarage Build Script End"
