- 18.04 Ubuntu only.
- Build dkms wireguard on each start if it not exists for current kernel.
- If $IFACE defined (default "wg0") set up iface and generate private key to /mnt/
- If $CONTROLLER defined (it must be URL) start polling each 5 second it URL for network config

Request examlpe:
```
POST /update/ HTTP/1.1
hostname=example-hostname&pubkey=HeyDjeriYhh&port=60000
```
Response:

`{"result": "unassigned"}` - remove IP, routes and peer

`{"result": "ok", "peer": "12.45.12.3:54310", "pubkey": "Iasasdasdqweqwe", "ip": "192.168.19.14", "routes": ["10.0.0.0/8", "192.168.0.0/16", "172.16.0.0/12",]}` - add peer, IP and routes.



Build wireguard module only:
```
docker run  --privileged --rm -ti -e 'IFACE=""' paucpauc/wireguard_agent
```
Build module and set up wg0:
```
docker run  --privileged -v /mnt/wg/:/mnt/ --network=host --rm -ti -d --name wg_agent paucpauc/wireguard_agent
```
Build module and start agent:
```
docker run  --privileged -v /mnt/wg/:/mnt/ --network=host --restart unless-stopped -d --name wg_agent -e 'CONTROLLER=https://api.controller.examlpe.com/update/' paucpauc/wireguard_agent
```
