
// author: Bartlomiej "furas" Burek (https://blog.furas.pl)
// date: 2023.11.02

### systemd - starting after system restart ###

# copy configuration file 
```
sudo cp flask-piec.system /etc/systemd/system/
```

# check if service works
```
systemctrl status flask-piec.system
```

# reload all services
```
sudo systemctrl deamon-reload
```

# enable and start service
```
sudo systemctrl enable flask-piec.system
sudo systemctrl start flask-piec.system
```
