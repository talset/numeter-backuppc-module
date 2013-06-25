numeter-backuppc-module
=======================

Backuppc module for Numeter poller.

#Description
Read backups file contained into $Conf{TopDir}/pc
numeter-backuppc-module interpret backups logs and make statistics

* Backup duration
* Files Transfered
* Files errors
* Backup Size
* Compression Rate

#Installation

```bash
  git clone git@github.com:talset/numeter-backuppc-module.git
  python setup.py install
```

#Configuration

You hate to fix logpath ($Conf{TopDir}/pc) in numeter_poller.cfg
```bash
  vim /etc/numeter/numeter_poller.cfg 
  [backuppcModule]
  logpath = /home/backuppc/pc
```
