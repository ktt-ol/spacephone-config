# Spacephone config

We've setup an Asterisk server with old Cisco 7911 IP phones. You'll find here the our installation and many configuration files.

More information about this phone: https://www.cisco.com/c/en/us/support/collaboration-endpoints/unified-ip-phone-7911g/model.html


# Installation

## Server

We use the Asterisk server for SIP and a tftp server that distributes the configuration to the phones.

```
apt-get install asterisk atftpd
```

Edit `/etc/default/atftpd`

```
USE_INETD=false
# OPTIONS below are used only with init script
OPTIONS="--tftpd-timeout 300 --port 69 --retry-timeout 5 --mcast-port 1758 --mcast-addr 239.239.239.0-255 --mcast-ttl 1 --maxthread 100 --verbose=5 /srv/tftp"
```

See `asterisk/` folder for the configuration files, run `./makeConfig.sh` in that folder and copy all `.conf` files to `/etc/asterisk/`.


## Install as VM

The server runs as a kvm image.

```
virt-install \
 -n spacephone \
 --description "Asterisk" \
 --os-type=Linux \
 --ram=512 \
 --vcpus=1 \
 --disk path=....../spacephone.qcow2,bus=virtio \
 --network bridge:br0 \
 --accelerate \
 --import \
 --os-type=linux \
 --os-variant=debianetch \
 --noautoconsole \
 --vnc
 ```

# Phone config files

Download the SIP firmware [from here](https://goo.gl/ozAUrw). Use the zip version and unzip the content into `tftp/`

Create and edit the secrets file.
```
cd phone
cp secrets.example.txt secrets.txt
./makeConfig.sh
```

copy the `tftp/` folder to `/srv/ftfp`


# Debug

Use this credentials after ssh login:
User/Pass: debug/debug

## Network

```
tcpdump -vvlenx -s 1500 -X port 5060 or port 5061
tcpdump -vvlenx -s 1500 -X ether host e8:40:40:a2:3b:ef
```

## Asterisk

Open asterisk console:
```
asterisk -crvvvvv
```

Helpful commands
```
sip set debug on
sip reload
core reload
```
