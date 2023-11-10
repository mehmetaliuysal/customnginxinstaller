
# Custom Nginx Installation Script

This repository contains a script for custom installation and configuration of Nginx on a Linux system. The script automates the process of installing Nginx and its dependencies, configuring it with custom parameters, and setting up the necessary system services.


This script not only automates the installation of Nginx but also includes the integration of specific modules like `nginx-module-vts`, `nginx-module-stream-sts`, and `nginx-module-sts`. These modules significantly enhance Nginx's functionality, particularly for proxy server usage, enabling detailed metrics collection at the vhost level, server traffic status monitoring, and more.

### Key Enhancements:

- **nginx-module-vts**: Facilitates detailed metrics collection, offering insights into Nginx's performance as a proxy server.
- **nginx-module-stream-sts** and **nginx-module-sts**: Provide server traffic status monitoring capabilities, essential for managing high-traffic environments.

By incorporating these modules, the script elevates Nginx to a more robust and insightful web server, suitable for environments requiring detailed traffic analysis and control.
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

## Additional Features

This script specifically installs the following Nginx modules for enhanced functionality:

- [nginx-module-vts](https://github.com/vozlt/nginx-module-vts.git): Provides the ability to collect detailed metrics at the vhost level when Nginx is used as a proxy server. This includes detailed status monitoring of upstreams, cache, and more.
- [nginx-module-stream-sts](https://github.com/vozlt/nginx-module-stream-sts): Allows for stream server traffic status monitoring.
- [nginx-module-sts](https://github.com/vozlt/nginx-module-sts): Adds support for server traffic status monitoring.

### Benefits of nginx-module-vts

The `nginx-module-vts` module enables detailed metrics collection and visualization for Nginx. Key features include:

- Detailed monitoring of Nginx server status.
- Real-time statistics of Nginx performance.
- Ability to monitor Nginx as a load balancer and see traffic distribution across upstream servers.
- Facilitates setting up limits and controls at the vhost level, enhancing security and resource management.

By integrating these modules, the script enhances Nginx's capabilities as a robust and versatile web server, particularly for use cases involving high traffic and the need for detailed monitoring and traffic control.
