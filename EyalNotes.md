to run airgeddon:
  cd desktom/airgeddon
  sudo bash airgeddon.sh

To display listening  TCP connections, run the command:
  ss -tl
  or:
  sudo netstat -tulpn
  or: 
  sudo lsof -i :53

How to stop using portd-resolved using port 53 on Ubuntu:
  sudo nano /etc/systemd/resolved.conf
  and change the following line:
  DNS=
  to:
  DNS=1.1.1.1
  and the line:
  DNSStubListener=yes
  to:
  DNSStubListener=no
  
  and then restart the service:
  sudo systemctl restart systemd-resolved.service

How to revert back to using portd-resolved using port 53 on Ubuntu:
  sudo nano /etc/systemd/resolved.conf
  and change the following line:
  DNS=
  to:
  DNS=
  and the line:
  DNSStubListener=no
  to:
  DNSStubListener=yes

  and then restart the service:
  sudo systemctl restart systemd-resolved.service

