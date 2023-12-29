# Useful stuff
## Useful commands
### Sync scripts on remote machine through SSH
```
./sync_scrits.sh 
```
### Launch node script
The node script is the script that will send traffic to a TCP server
```
python run node.py <server_ip_address>
```
### Launch server script
The server script does not do anything ; it just listens, receives the TCP messages and outputs them
```
python run dummy_server.py <ip_address_of_self>
```
## Running jobs on Grid5000


