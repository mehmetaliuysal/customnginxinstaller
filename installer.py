import subprocess
import os
import time
import sys

# Color codes for ANSI
class Colors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def run_command(command, success_message):
    """ Run a shell command and print a success message if it succeeds """
    try:
        subprocess.check_call(command, shell=True)
        print(Colors.OKGREEN + success_message + Colors.ENDC)
    except subprocess.CalledProcessError:
        print(Colors.FAIL + f"Error occurred: {command}" + Colors.ENDC)
        exit(1)



def update_nginx_conf():
    """ Update /etc/nginx/nginx.conf file with necessary modules and configurations """
    modules_to_add = [
        "load_module /usr/lib/nginx/modules/ngx_http_vhost_traffic_status_module.so;",
        "load_module /usr/lib/nginx/modules/ngx_stream_module.so;",
        "load_module /usr/lib/nginx/modules/ngx_stream_server_traffic_status_module.so;",
        "load_module /usr/lib/nginx/modules/ngx_http_stream_server_traffic_status_module.so;"
    ]
    server_block_additions = [
        "vhost_traffic_status_zone;",
        "stream_server_traffic_status_zone;"
    ]
    location_block_additions = [
        "\t\tlocation /nginx_status {\n\t\t\tstub_status;\n\t\t}\n",
        "\t\tlocation /http_traffic_status {\n\t\t\tvhost_traffic_status_bypass_limit on;\n\t\t\tvhost_traffic_status_bypass_stats on;\n\t\t\tvhost_traffic_status_display;\n\t\t\tvhost_traffic_status_display_format json;\n\t\t}\n"
    ]
    try:
        with open('/etc/nginx/nginx.conf', 'r') as file:
            lines = file.readlines()

        with open('/etc/nginx/nginx.conf', 'w') as file:

            # Add modules at the end of the file
            for module in modules_to_add:
                if module + '\n' not in lines:
                    file.write(module + '\n')


            http_block_found = False
            for line in lines:
                if 'http {' in line:
                    file.write(line)
                    http_block_found = True
                    # Add server block additions immediately inside the http block
                    for addition in server_block_additions:
                        if addition + '\n' not in lines:
                            file.write("\t" + addition + "\n")
                    continue

                if 'server {' in line and http_block_found:
                    file.write(line)
                    # Add location blocks inside the first server block
                    for addition in location_block_additions:
                        if addition + '\n' not in lines:
                            file.write("\t" + addition)
                    http_block_found = False  # Prevent further additions
                    continue

                file.write(line)

            print(Colors.OKGREEN + "/etc/nginx/nginx.conf updated successfully." + Colors.ENDC)
    except Exception as e:
        print(Colors.FAIL + f"Failed to update /etc/nginx/nginx.conf: {e}" + Colors.ENDC)




# Argüman kontrolü
if "--update-conf" in sys.argv:
    update_nginx_conf()
    sys.exit()

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
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

print(Colors.HEADER + "Starting Custom Nginx Installer..." + Colors.ENDC)
print(Colors.HEADER + "Waiting 10 seconds for abort [CTRL-C]..." + Colors.ENDC)
time.sleep(10)  # Give the user 10 seconds to abort

# Check if Git is installed and install if not
if not is_git_installed():
    print(Colors.WARNING + "Git is not installed. Installing Git..." + Colors.ENDC)
    run_command("sudo apt-get install git -y", "Git successfully installed.")

# Update package lists and install necessary packages
run_command("sudo apt update", "Package lists updated")
run_command("sudo apt-get install build-essential libpcre3 libpcre3-dev zlib1g zlib1g-dev libssl-dev libgd-dev libxslt1-dev libxml2-dev libgeoip-dev libgoogle-perftools-dev libperl-dev wget -y", "Required packages installed")

# Download, extract, and compile Nginx
os.chdir('/tmp')

run_command("git clone https://github.com/vozlt/nginx-module-vts.git", "VTS module cloned")
run_command("git clone https://github.com/vozlt/nginx-module-sts", "STS module cloned")
run_command("git clone https://github.com/vozlt/nginx-module-stream-sts", "Stream STS module cloned")


run_command("wget http://nginx.org/download/nginx-1.24.0.tar.gz", "Downloaded Nginx tarball")
run_command("tar zxvf nginx-1.24.0.tar.gz", "Extracted Nginx tarball")
os.chdir('/tmp/nginx-1.24.0')
run_command("./configure --prefix=/usr/share/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/lock/nginx.lock --http-client-body-temp-path=/var/lib/nginx/body --http-fastcgi-temp-path=/var/lib/nginx/fastcgi --http-proxy-temp-path=/var/lib/nginx/proxy --http-scgi-temp-path=/var/lib/nginx/scgi --http-uwsgi-temp-path=/var/lib/nginx/uwsgi --user=nginx --group=nginx --with-threads --with-file-aio --with-http_ssl_module --with-http_v2_module --with-http_realip_module --with-http_addition_module --with-http_xslt_module=dynamic --with-http_image_filter_module=dynamic --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_auth_request_module --with-http_random_index_module --with-http_secure_link_module --with-http_degradation_module --with-http_slice_module --with-http_stub_status_module --with-http_perl_module=dynamic --with-pcre --with-pcre-jit --with-stream=dynamic --with-stream_ssl_module --with-mail=dynamic --with-mail_ssl_module --with-google_perftools_module --with-debug --add-dynamic-module=../nginx-module-vts --add-dynamic-module=../nginx-module-sts --add-dynamic-module=../nginx-module-stream-sts", "Nginx configured")
run_command("make", "Nginx build completed")
run_command("sudo make install", "Nginx installed")

# Additional setup for Nginx
run_command("sudo adduser --system --no-create-home --disabled-login --disabled-password --group nginx", "Nginx user created")
run_command("sudo mkdir -p /var/lib/nginx/body && sudo mkdir -p /var/lib/nginx/proxy && sudo mkdir -p /var/lib/nginx/fastcgi && sudo mkdir -p /var/lib/nginx/uwsgi && sudo mkdir -p /var/lib/nginx/scgi && sudo chown -R nginx:nginx /var/lib/nginx", "Nginx directories created and permissions set")

update_nginx_conf()
create_nginx_service()


# Reload system daemon and enable nginx service
run_command("sudo systemctl daemon-reload", "System daemon reloaded")
run_command("sudo systemctl enable nginx", "Nginx service enabled")

print(Colors.HEADER + "Nginx installation and setup completed successfully!" + Colors.ENDC)
