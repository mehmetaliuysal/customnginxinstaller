
# Custom Nginx Installation Script

This repository contains a script for custom installation and configuration of Nginx on a Linux system. The script automates the process of installing Nginx and its dependencies, configuring it with custom parameters, and setting up the necessary system services.

## Features

- Checks for and installs necessary dependencies including Nginx and its modules.
- Configures Nginx with a custom set of parameters.
- Updates the Nginx configuration file to include specified modules.
- Creates and configures a systemd service file for Nginx.
- Provides clear, colored output for each step of the process.

## Prerequisites

Before running the script, ensure that:
- You have Python 3 installed on your system.
- You have sufficient permissions (possibly root access) to install packages and write to system directories.

## Usage

1. Clone the repository or download the script.
2. Make the script executable: `chmod +x custom_nginx_install.py`
3. Run the script: `sudo ./custom_nginx_install.py`
4. Follow the on-screen instructions.

## Script Workflow

1. **Initial Setup**: The script starts by updating package lists and installing necessary build tools and libraries.
2. **Nginx Installation**: Downloads and extracts Nginx, then compiles it with custom configuration options.
3. **Configuration**: Updates `/etc/nginx/nginx.conf` with specified modules if they are not already included.
4. **Service File Creation**: Creates a systemd service file for Nginx, enabling it to be managed as a service.
5. **Final Steps**: Reloads the system daemon and enables the Nginx service.

## Notes

- The script provides colored output to distinguish between different stages and to highlight success or failure messages.
- In case of any errors during the execution, the script will stop and display an error message.

## License

This script is released under the MIT License.
