# mayday
This mini repository contains a single ultra-lightweight python script (vide coded) which constantly monitors system mem, cpu and temperature and force **shutdowns** it if reaches threshold.

## To-Do
These can be added/extended [anyone looking for oss contribution]
- add os env variable control for threshold and testing
- very dumb just tirelessly monitors resource utility for single threshold value but can be made smart by identifying sudden spikes and similar checks instead
- can core dump for all running processes and re-run from the exact same point upon restart

## Get it working
Steps and details to create a daemon of this script and also add rotated logs for the daemon

1. create `mayday.service` file within `/etc/systemd/system/` directory

2. create a `mayday.log` file within `/var/log/`

3. create rotated log file `mayday` within `/etc/logrotate.d/`

4. run the following command to register daemon:
```bash
sudo systemctl daemon-reload
```

5. now enable and start the mayday service:
```bash
sudo systemctl enable mayday
sudo systemctl start mayday.service
```