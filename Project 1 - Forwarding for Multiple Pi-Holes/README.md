Needed to build a quick "forwarding" service for my 3 GEN 1, Raspberry Pis which can't run K3s. The things the user must do to get this running is simple:
1. Ensure PiHoles are accessible by forwarder.
2. Install the required Python libraries called out at the top of the code.
3. Edit and add your own server list for PiHoles.
4. Edit and add in the IP where the forwarder is ran from.
5. Edit and add your webhook URL for Discord (will get a notification if the code fails).

Note: Due to socket access this needs to be ran with admin priviledges or will fail. 
