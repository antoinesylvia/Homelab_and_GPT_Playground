import socket
import random
import datetime
import os
import requests

# Get the IP address or hostname of the system where the code is running
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# List of Pi-hole server IPs and ports, add as many Pi-holes as you want.
servers = [
    ("192.168.x.x", 53),
    ("192.168.x.x", 53),
    ("192.168.x.x", 53)
]

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to your server IP and port 53. Add IP for server running the forwarding service.
sock.bind(("192.168.x.x", 53))

# Function to select a random server
def select_server():
    return random.choice(servers)

# Log file path
log_file_path = "load_balancer.log"
max_log_size = 1024 * 1024  # 1 MB

# Check log file size and rotate if necessary
if os.path.isfile(log_file_path) and os.path.getsize(log_file_path) >= max_log_size:
    # Create a backup file with ".bak" extension
    backup_path = log_file_path + ".bak"
    # Remove the backup file if it already exists
    if os.path.isfile(backup_path):
        os.remove(backup_path)
    # Rename the log file to the backup file
    os.rename(log_file_path, backup_path)

# Discord webhook URL for notification
webhook_url = "https://discord.com/api/webhooks/add_your_webhook_url"

# Function to send a Discord notification
def send_discord_notification():
    message = "PiHole forwarding application is down on {} ({}).".format(ip_address, hostname)

    payload = {
        "content": message
    }
    requests.post(webhook_url, json=payload)

# Main event loop
while True:
    try:
        # Receive a DNS request and its address with a larger buffer size (4096)
        data, addr = sock.recvfrom(4096)

        try:
            # Extract the domain name from the DNS request
            domain_name = ""
            current_index = 12
            while True:
                label_length = data[current_index]
                if label_length == 0:
                    break
                label = data[current_index+1:current_index+label_length+1].decode()
                domain_name += label + "."
                current_index += label_length + 1

            # Remove the trailing dot
            domain_name = domain_name.rstrip(".")

            # Select a random Pi-hole server
            server = select_server()

            # Forward the request to the selected server
            sock.sendto(data, server)

            # Create a log message with timestamp, domain name, and (UDP)
            log_message = "[{}] Request ({}) forwarded to {}:{} (UDP)\n".format(datetime.datetime.now(), domain_name, server[0], server[1])

            # Print log message to console
            print(log_message)

            # Write log message to log file
            with open(log_file_path, "a") as log_file:
                log_file.write(log_message)
        except Exception as e:
            print("Error processing DNS request:", str(e))
            continue  # Skip this iteration and move to the next one
    except Exception as e:
        # If an exception occurs, send a Discord notification
        send_discord_notification()
        raise e
