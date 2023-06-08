Needed to build a quick "forwarding" service for my 3 GEN 1, Raspberry Pis which can't run K3s. The things the user must do to get this running is simple:
1. Ensure PiHoles are accessible by forwarder.
2. Install the required Python libraries called out at the top of the code. User can utilize: https://github.com/antoinesylvia/Homelab_and_GPT_Playground/blob/main/Project%201%20-%20Forwarding%20for%20Multiple%20Pi-Holes/libraries_check.py
3. Edit and add your own server list for PiHoles.
4. Edit and add in the IP where the forwarder is ran from.
5. Edit and add your webhook URL for Discord (will get a notification if the code fails).

Due to socket access this needs to be ran with admin priviledges or will fail. 

![Sample Image](https://github.com/antoinesylvia/Homelab_and_GPT_Playground/blob/737c3e5a32ceda8e51dba54bc229fcf1f300cfcc/Project%201%20-%20Forwarding%20for%20Multiple%20Pi-Holes/sample.png)

NGINX can also handle this function but you would need to compile it with the "streams" module: https://www.nginx.com/blog/announcing-udp-load-balancing/

Sample Flow: User > Unifi Security Gateway > Forwarder/Load Balancer(s) for DNS x2 > PiHole x3 > DNScrypt Proxy (DNS over TLS or DNS over HTTPS) > Public DNS (with no logging) or fallback to Unbound (recursive DNS installed locally x2).
