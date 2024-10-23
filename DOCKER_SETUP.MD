# Docker Container Setup Documentation

This document provides instructions for pulling, renaming, and running the Docker containers for the Arduino data and air quality checker applications.

## Prerequisites

- Ensure you have [Docker](https://www.docker.com/products/docker-desktop) installed on your machine.
- Open a terminal or command prompt.

## Step 1: Pull the Docker Containers

### Pull `govardhan06/arduino_data:latest`

1. Run the following command to pull the Arduino data container:

   ```bash
   docker pull govardhan06/arduino_data:latest
   ```

### Pull `govardhan06/air_quality_checker:latest`

2. Next, pull the air quality checker container:

   ```bash
   docker pull govardhan06/air_quality_checker:latest
   ```

## Step 2: Rename the Docker Containers

### Rename `govardhan06/arduino_data:latest`

1. After pulling, rename the Arduino data container with the following command:

   ```bash
   docker tag govardhan06/arduino_data:latest arduino_data:latest
   ```

### Rename `govardhan06/air_quality_checker:latest`

2. Rename the air quality checker container similarly:

   ```bash
   docker tag govardhan06/air_quality_checker:latest air_quality_checker:latest
   ```

## Step 3: Verify the Renamed Containers

1. To confirm that the containers have been renamed, list all Docker images:

   ```bash
   docker images
   ```

   You should see `arduino_data:latest` and `air_quality_checker:latest` in the list.

## Step 4: Run the Docker Containers (in two separate terminal tabs)

### Run `arduino_data:latest`

1. To run the Arduino data container, use the following command:

   ```bash
   docker run arduino_data:latest
   ```

### Run `air_quality_checker:latest`

2. To run the air quality checker container, execute:

   ```bash
   docker run -p 8000:8000 air_quality_checker:latest
   ```

## Conclusion

You have successfully pulled, renamed, and run the Docker containers for the Arduino data and air quality checker applications.

For further information or troubleshooting, refer to the [Docker documentation](https://docs.docker.com/).
