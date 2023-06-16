import socket
import random
import datetime
import os
import requests
from dns import message, query, rdatatype, rdataclass, exception

# Get the IP address or hostname of the system where the code is running
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# List of Pi-hole server IPs, add as many Pi-holes as you want.
servers = [
    "192.168.x.131",
    "192.168.x.132",
    "192.168.x.139"
]

# Log file path
log_file_path = "load_balancer.log"
max_log_size = 1024 * 1024  # 1 MB

# Discord webhook URL for notification
webhook_url = "https://discord.com/api/webhooks/add_your_web_hook_info"

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
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to your server IP and port 53, add the IP that will run this code, be sure to point to it in your DNS settings for your router. Ensure your host firewall is open for port 53 UDP. 
        sock.bind(("192.168.x.x", 53))

        # Receive a DNS request and its address with a larger buffer size (4096)
        data, addr = sock.recvfrom(4096)

        # Select a random Pi-hole server
        server = random.choice(servers)

        try:
            # Create a DNS request message from the received data
            request = message.from_wire(data)

            # Send the DNS request to the selected server and receive the response
            response = query.tcp(request, server)

            # Check if the response is valid
            if response and response.rcode() == 0:
                # Get the domain name from the question section of the request
                question = request.question[0]
                domain_name = question.name.to_text()

                # Forward the response to the original requester
                sock.sendto(response.to_wire(), addr)

                # Create a log message with timestamp, domain name, and (UDP)
                log_message = "[{}] Request ({}) forwarded to {}:{} (UDP)\n".format(datetime.datetime.now(), domain_name, server, 53)

                # Print log message to console
                print(log_message)

                # Write log message to log file
                with open(log_file_path, "a") as log_file:
                    log_file.write(log_message)

        except exception.DNSException as e:
            print("Error processing DNS request:", str(e))

        finally:
            # Close the socket
            sock.close()

    except Exception as e:
        print("Error receiving DNS request:", str(e))
        # If an exception occurs, send a Discord notification
        send_discord_notification()
