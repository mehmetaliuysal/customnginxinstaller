import subprocess
import os
import time

# Color codes for ANSI
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


print(Colors.HEADER + "Starting Custom Nginx Installer..." + Colors.ENDC)
print(Colors.HEADER + "Waiting 10 seconds for abort [CTRL-C]..." + Colors.ENDC)
time.sleep(10)  # Give the user 10 seconds to abort


def run_command(command, success_message, change_dir=False):
    """ Run a shell command and print a success message if it succeeds """
    try:
        if change_dir and command.startswith('cd'):
            os.chdir(command.replace('cd ', ''))
        else:
            subprocess.check_call(command, shell=True)

        print(Colors.OKGREEN + success_message + Colors.ENDC)
    except subprocess.CalledProcessError:
        print(Colors.FAIL + f"Error occurred: {command}" + Colors.ENDC)
        exit(1)


def update_nginx_conf():
    """ Update /etc/nginx/nginx.conf file with necessary modules """
    modules_to_add = [
        "load_module /usr/lib/nginx/modules/ngx_http_vhost_traffic_status_module.so;",
        "load_module /usr/lib/nginx/modules/ngx_stream_module.so;",
        "load_module /usr/lib/nginx/modules/ngx_stream_server_traffic_status_module.so;",
        "load_module /usr/lib/nginx/modules/ngx_http_stream_server_traffic_status_module.so;"
    ]
    try:
        with open('/etc/nginx/nginx.conf', 'r+') as file:
            lines = file.readlines()
            file.seek(0)

            for module in modules_to_add:
                if module not in lines:
                    file.write(module + '\n')

            file.writelines(lines)
            print(Colors.OKGREEN + "/etc/nginx/nginx.conf updated successfully." + Colors.ENDC)
    except Exception as e:
        print(Colors.FAIL + f"Failed to update /etc/nginx/nginx.conf: {e}" + Colors.ENDC)

def create_nginx_service():
    """ Create and write the nginx.service file """
    nginx_service_content = """
[Unit]
Description=Nginx - high performance web server
Documentation=http://nginx.org/en/docs/
After=network.target

[Service]
Type=forking
PIDFile=/run/nginx.pid
ExecStartPre=/usr/sbin/nginx -t -q -g 'daemon on; master_process on;'
ExecStart=/usr/sbin/nginx -g 'daemon on; master_process on;'
ExecReload=/usr/sbin/nginx -g 'daemon on; master_process on;' -s reload
ExecStop=/usr/sbin/nginx -s quit

[Install]
WantedBy=multi-user.target
    """

    try:
        with open('/etc/systemd/system/nginx.service', 'w') as file:
            file.write(nginx_service_content.strip())
            print(Colors.OKGREEN + "/etc/systemd/system/nginx.service file created successfully." + Colors.ENDC)
    except Exception as e:
        print(Colors.FAIL + f"Failed to create /etc/systemd/system/nginx.service: {e}" + Colors.ENDC)


def is_git_installed():
    """ Check if Git is installed """
    try:
        subprocess.check_call(["git", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False




if not is_git_installed():
    print(Colors.WARNING + "Git is not installed. Installing Git..." + Colors.ENDC)
    run_command("sudo apt-get install git -y", "Git successfully installed.")

# Initial setup commands
initial_commands = [
    ("cd /tmp", "Changed directory to /tmp", True),
    ("sudo apt update", "Package lists updated",True),
    ("sudo apt-get install build-essential libpcre3 libpcre3-dev zlib1g zlib1g-dev libssl-dev libgd-dev libxslt1-dev libxml2-dev libgeoip-dev libgoogle-perftools-dev libperl-dev git wget -y", "Required packages installed",True),
]

# Running the initial setup commands
for cmd, message, change_dir in initial_commands:
    run_command(cmd, message, change_dir)


# Nginx configuration and installation commands
commands = [
    ("cd /tmp && wget http://nginx.org/download/nginx-1.24.0.tar.gz && tar zxvf nginx-1.24.0.tar.gz", "Downloaded and extracted Nginx", True),
    ("cd /tmp/nginx-1.24.0 && ./configure --prefix=/usr/share/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/lock/nginx.lock --http-client-body-temp-path=/var/lib/nginx/body --http-fastcgi-temp-path=/var/lib/nginx/fastcgi --http-proxy-temp-path=/var/lib/nginx/proxy --http-scgi-temp-path=/var/lib/nginx/scgi --http-uwsgi-temp-path=/var/lib/nginx/uwsgi --user=nginx --group=nginx --with-threads --with-file-aio --with-http_ssl_module --with-http_v2_module --with-http_realip_module --with-http_addition_module --with-http_xslt_module=dynamic --with-http_image_filter_module=dynamic --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_auth_request_module --with-http_random_index_module --with-http_secure_link_module --with-http_degradation_module --with-http_slice_module --with-http_stub_status_module --with-http_perl_module=dynamic --with-pcre --with-pcre-jit --with-stream=dynamic --with-stream_ssl_module --with-mail=dynamic --with-mail_ssl_module --with-google_perftools_module --with-debug --add-dynamic-module=../nginx-module-vts --add-dynamic-module=../nginx-module-sts --add-dynamic-module=../nginx-module-stream-sts", "Nginx configured", True),
    ("cd /tmp/nginx-1.24.0 && make", "Nginx build completed", True),
    ("cd /tmp/nginx-1.24.0 && sudo make install", "Nginx installed", True),
    # Add other commands here...
]

# Running the commands
for cmd, message, change_dir in commands:
    run_command(cmd, message, change_dir)

# Additional setup commands
setup_commands = [
    ("sudo adduser --system --no-create-home --disabled-login --disabled-password --group nginx", "Nginx user created",True),
    ("sudo mkdir -p /var/lib/nginx/body && sudo mkdir -p /var/lib/nginx/proxy && sudo mkdir -p /var/lib/nginx/fastcgi && sudo mkdir -p /var/lib/nginx/uwsgi && sudo mkdir -p /var/lib/nginx/scgi && sudo chown -R nginx:nginx /var/lib/nginx", "Nginx directories created and permissions set", True),
    # Add the code for updating /etc/nginx/nginx.conf and creating the service file here...
]

# Running the additional setup commands
for cmd, message in setup_commands:
    run_command(cmd, message)

# Update nginx.conf file and create systemd service file here...
update_nginx_conf()
create_nginx_service()
# Note: File manipulation in Python requires careful handling to avoid corrupting the files.

# Final system commands
final_commands = [
    ("sudo systemctl daemon-reload", "System daemon reloaded", True),
    ("sudo systemctl enable nginx", "Nginx service enabled", True),
]

# Running the final system commands
for cmd, message in final_commands:
    run_command(cmd, message)

print(Colors.HEADER + "Nginx installation and setup completed successfully!" + Colors.ENDC)
