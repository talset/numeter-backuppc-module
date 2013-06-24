#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
import os
import re

class backuppcModule: 
    "Module Backuppc"

    def  __init__(self,logger,configParser=None):
        "Load configuration and start connexion"
        self._logger= logger
        self._logger.info("Plugin Backuppc start")
        self._logpath = './pc'
        self._STATUS = {}


    
    def pluginsRefresh(self):
        "Return plugins info for refresh"
#        infos=   [{    'Plugin': plugin, 
#                      'Base': '1000', 
#                      'Describ': '', 
#                      'Title': plugin, 
#                      'Vlabel': '', 
#                      'Order': '', 
#                      'Infos': {
#                            "id":{"type": "COUNTER", "id": "down", "label": "received"},
#                            "id":{"type": "COUNTER", "id": "up", "label": "upload"},
#                       
#                 }]
# /!\ Attention chaque DS doit avoir une entré dans Infos pour ne pas étre ignoré. par exemple "id":{"id": "up"} au moins !


    def getData(self):
        "get and return all data collected"
        for pc in os.listdir(self._logpath):
            path = self._logpath+'/'+pc+'/'+'backups'
            #STATUS = self._parserLog(path)
            self._STATUS[pc] = self._parserLog(path)

        DATAS = []
        
        for pc in self._STATUS.keys():
            print pc
            #Temps de backup
            DATAS.extend(self._backupDuration(pc,'fetch'))

        return DATAS


    def _backupDuration(self,pc,mode):
        "return the duration of last backup time"
        now = time.strftime("%Y %m %d %H:%M", time.localtime())
        nowTimestamp = "%.0f" % time.mktime(time.strptime(now, '%Y %m %d %H:%M'))


        if mode == 'fetch': # DATAS
            DATAS = []
            print "updated %s -> %s,\n" % (time.ctime(int(self._STATUS[pc]['startTime'])), time.ctime(int(self._STATUS[pc]['endTime'])));
            duration = int(self._STATUS[pc]['endTime']) - int(self._STATUS[pc]['startTime'])
            if duration <= 0: duration = 1
            #print "%.1f" % (duration/60)
            duration = "%.1f" % (duration/60)

            DATAS.append({
                    'TimeStamp': nowTimestamp,
                    'Plugin': 'duration_' + pc,
                    'Values': {
                                'time': duration,
                                'full': duration if self._STATUS[pc]['backupType'] == 'full' else 0,
                                'incr': duration if self._STATUS[pc]['backupType'] == 'incr' else 0,
                               }
            })
            return DATAS

        else: # INFOS
            dsInfos = {
                    'time': {"type": "GAUGE",
                         "id": 'time',
                         "draw": 'line',
                         "label": 'time'},
                    'incr': {"type": "GAUGE",
                         "id": 'incr',
                         "draw": 'line',
                         "label": 'incr'},
                    'full': {"type": "GAUGE",
                         "id": 'full',
                         "draw": 'line',
                         "label": 'full'},
            }

            INFOS = {
               'Plugin': 'backupDuration',
               'Describ': 'Backup Duration in min',
               'Category': 'Backuppc',
               'Base': '1000',
               'Title': 'Backup Duration',
               'Vlabel': 'min',
               'Infos': dsInfos,
            }

            return INFOS

    def _parserLog(self, path):
        "parse backuppc log and return hash table"
        f = open (path, 'r')
        lineList = f.readlines()
        f.close()

        #Create status hash whith value in backups
        STATUS = {}
        
        lastline = lineList[-1]
        print (lastline)

        head = ['backupID', 'backupType', 'startTime', 'endTime', 'totalFileTransf', 'totalFileSize', 'ExistFile', 'totalSizeExist', 'NewFile', 'totalSizeNew', 'nbErreurTransfert', 'nbErreurFile', 'nbErreurShare', 'nbErreurTar', 'compressionLvl', 'totalSizeExistFileCompr', 'totalSizeNewFileCompr']
        for value in re.split("\s", lastline):
            if head:
                #print head[0]+" - "+ value
                STATUS[head.pop(0)] = value
           # else:
           #     print " - "+ value

#Temps de backup
#Nombre de fichier transféré
#Nombre Erreurs
#Taille total transféré
#Taille total compressé transféré
#Niveau de Compression 



#        data=   [{      'TimeStamp': nowTimestamp, 
#                        'Plugin': 'df', 
#                        'Values': {
#                                    'dev_sda' : 40,
#                                    'dev_sdb' : 15,
#                                  }
#                }]
#        now              = time.strftime("%Y %m %d %H:%M", time.localtime())
#        nowTimestamp     = "%.0f" % time.mktime(time.strptime(now, '%Y %m %d %H:%M')) # "%.0f" % supprime le .0 aprés le
        return STATUS






if __name__ == "__main__":
    logger = logging.getLogger('backuppc')
    fh = logging.FileHandler('/tmp/backuppc.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

    stats = backuppcModule(logger,None)

    print str(stats.getData())
#    print str(stats.pluginsRefresh())
