# mayday
This mini repository contains a single ultra-lightweight python script (vide coded) which constantly monitors system mem, cpu and temperature and force shutdowns it if reaches threshold.

## To-Do
These can be added/extended [anyone looking for oss contribution]
- add os env variable control for threshold and testing
- very dumb just tirelessly monitors resource utility for single threshold value but can be made smart by identifying sudden spikes and similar checks instead
- can core dump for all running processes and re-run from the exact same point upon restart