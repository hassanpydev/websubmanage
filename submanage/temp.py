import CloudFlare
import os

import shutil
import subprocess
from mysql.connector import connect


def create_subdomain_dns_record(subdomain):
    cf = CloudFlare.CloudFlare(
        certtoken="v1.0-4ecb6fa2b427c0ec2b66a91c-9b92e59583349702eeb76ee5fee4eab750537c49d011842605e6bb166fc4c14df36781936a3fe92c55e433ccce5ae9085369907a09873fb9e0d60d2a37039e0ab8d4b889bb08a79b35",
        email="akraaonline@gmail.com",
        token="e535e60c2fd491a5b17c1fffac1faecf274da",
    )
    zones = cf.zones.get()
    zone_name = "websubmange.com"

    zone_id = None
    for zone in zones:
        if zone["name"] == zone_name:
            zone_id = zone["id"]
            break

    if not zone_id:
        print(f"Zone ID not found for Zone Name: {zone_name}")
        exit()

    # Specify the DNS record details
    record_type = "A"  # Example: A, CNAME, MX, etc.
    record_name = subdomain  # Example: subdomain.example.com
    record_content = "89.117.50.15"  # Example: IP address or domain name
    record_ttl = 3600  # Example: Time-to-Live value in seconds

    # Construct the DNS record data
    dns_record = {
        "type": record_type,
        "name": record_name,
        "content": record_content,
        "ttl": record_ttl,
        "proxied": True
    }

    # Add DNS record to CloudFlare
    result = cf.zones.dns_records.post(zone_id, data=dns_record)
    print(result)
    # Check if DNS record was added successfully




def build_config(site_name: str, root_dir: str) -> dict:
    """
    crete config file for new site configuration
    """
    server = {
        "listen": "80",
        "server_name": site_name,
        "root": root_dir,
        "index": "index.php",
        "location /": {"try_files": "$uri $uri/ /index.php?$args"},
        "location ~ \\.php$": {
            "include": "fastcgi_params",
            "fastcgi_pass": "unix:/var/run/php/php8.1-fpm.sock",
            "fastcgi_param": "SCRIPT_FILENAME $document_root$fastcgi_script_name",
        },
    }
    return server


def generate_nginx_config(server):
    config = []
    config.append("server {")
    config.append("    listen {};".format(server["listen"]))
    config.append("    server_name {};".format(server["server_name"]))
    config.append("    root {};".format(server["root"]))
    config.append("    index {};".format(server["index"]))
    config.append("    location / {")
    config.append("        try_files {};".format(server["location /"]["try_files"]))
    config.append("    }")
    config.append("    location ~ \\.php$ {")
    for directive, value in server["location ~ \\.php$"].items():
        config.append("        {} {};".format(directive, value))
    config.append("    }")
    config.append("}")
    return "\n".join(config)


def restart_nginx():
    # Define the Nginx restart command
    nginx_restart_command = "service nginx restart"

    # Run the Nginx restart command
    subprocess.run(nginx_restart_command, shell=True, check=True)
    print("Nginx restarted successfully")


def crete_database_for_wordpress(db_name):
    conn = connect(
        host="localhost",
        user="hassan",  # Replace with your MySQL username
        password="hassan1998",  # Replace with your MySQL password
    )

    # Create a new database
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE {db_name}")

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    print(f"Database '{db_name}' created successfully.")


def create_symbolic_link_to_site_enabled(path: os.path, filename):
    source_path = path
    destination_path = os.path.join("/etc/nginx/sites-enabled", filename)

    # Create the symbolic link

    # Check if the symbolic link was created successfully
    if os.path.islink(destination_path):
        print("Symbolic link created successfully.")
    else:
        os.symlink(source_path, destination_path)
        print("Symbolic link created successfully")


def copy_wordpress_files(path: os.path):
    source_file = "/root/Submanage/wordpress"
    destination_file = path

    # Copy the file

    # Check if the file was copied successfully
    if os.path.exists(destination_file):
        print("File copied already.")
    else:
        shutil.copytree(source_file, destination_file)


def add_permissions(path: os.path):
    dir_path = path

    # Set the ownership to www-data:www-data
    os.chown(
        dir_path, 33, 33
    )  # 33 is the uid and gid of www-data on most Linux systems


def create_new_site(site_name: str):
    nginx_path = "/etc/nginx/sites-available"
    filename = site_name
    site_config_path = os.path.join(nginx_path, filename + ".conf")
    wordpress_dir = os.path.join("/var/www/html", filename, "wordpress")
    nginx_config = generate_nginx_config(build_config(filename, wordpress_dir))
    if not os.path.exists(site_config_path):
        with open(site_config_path, "+w") as f:
            f.write(nginx_config)
            f.close()
    copy_wordpress_files(wordpress_dir)
    add_permissions(wordpress_dir)
    create_symbolic_link_to_site_enabled(site_config_path, filename)
    create_subdomain_dns_record(filename)
    # crete_database_for_wordpress(filename.split(".")[0])
    restart_nginx()


create_new_site("t.websubmange.com")
