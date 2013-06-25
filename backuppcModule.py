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
        self._configParser=configParser


        if self._configParser:
        # Get logfile
            if self._configParser.has_option('backuppcModule', 'logpath') \
            and self._configParser.get('backuppcModule', 'logpath'):
                self._logpath = self._configParser.get('backuppcModule'
                                            , 'logpath')


    
    def pluginsRefresh(self):
        "Return plugins info for refresh"
        for pc in os.listdir(self._logpath):
            filename = self._logpath+'/'+pc+'/'+'backups'
            if os.path.isfile(filename):
                path = filename
                #STATUS = self._parserLog(path)
                self._STATUS[pc] = self._parserLog(path)
        INFOS = []
        
        for pc in self._STATUS.keys():
            # Backup duration
            INFOS.append(self._backupDuration(pc,'config'))
            # Files Transfered
            INFOS.append(self._filesTransfered(pc,'config'))
            # Files errors
            INFOS.append(self._numberErrors(pc,'config'))
            # Backup Size
            INFOS.append(self._backupSize(pc,'config'))
            # Compression Rate
            INFOS.append(self._compressionRate(pc,'config'))

        return INFOS



    def getData(self):
        "get and return all data collected"
        for pc in os.listdir(self._logpath):
            filename = self._logpath+'/'+pc+'/'+'backups'
            if os.path.isfile(filename):
                path = filename
                #STATUS = self._parserLog(path)
                self._STATUS[pc] = self._parserLog(path)
        DATAS = []
        
        for pc in self._STATUS.keys():
            # Backup duration
            DATAS.append(self._backupDuration(pc,'fetch'))
            # Files Transfered
            DATAS.append(self._filesTransfered(pc,'fetch'))
            # Files errors
            DATAS.append(self._numberErrors(pc,'fetch'))
            # Backup Size
            DATAS.append(self._backupSize(pc,'fetch'))
            # Compression Rate
            DATAS.append(self._compressionRate(pc,'fetch'))

        return DATAS


    def _backupDuration(self,pc,mode):
        "return the duration of last backup time"
        now = time.strftime("%Y %m %d %H:%M", time.localtime())
        nowTimestamp = "%.0f" % time.mktime(time.strptime(now, '%Y %m %d %H:%M'))


        if mode == 'fetch': # DATAS
            #print "updated %s -> %s,\n" % (time.ctime(int(self._STATUS[pc]['startTime'])), time.ctime(int(self._STATUS[pc]['endTime'])));
            duration = int(self._STATUS[pc]['endTime']) - int(self._STATUS[pc]['startTime'])
            if duration <= 0: duration = 1
            #print "%.1f" % (duration/60)
            duration = "%.1f" % (duration/60)

            datas = {
                    'TimeStamp': nowTimestamp,
                    'Plugin': 'duration_' + pc,
                    'Values': {
                                'time': duration,
                                'full': duration if self._STATUS[pc]['backupType'] == 'full' else 0,
                                'incr': duration if self._STATUS[pc]['backupType'] == 'incr' else 0,
                               }
            }
            return datas

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

            infos = {
               'Plugin': 'duration_' + pc,
               'Describ': 'Backup Duration in min',
               'Category': 'Backup '+ pc,
               'Base': '1000',
               'Title': 'Backup Duration',
               'Vlabel': 'min',
               'Infos': dsInfos,
            }

            return infos




        #Nombre de fichier transféré
        #   - #7 : Fichiers existants
        #   - #9 : Nouveaux fichiers
        #   - #5 : Fichiers existants + Nouveaux fichiers
        #print "\nGRAPH : Nombre de fichier transféré\n";
        #print $totalFileTransf."\n".$ExistFile."\n".$NewFile."\n";

    def _filesTransfered(self,pc,mode):
        "return number of files transfered"
        now = time.strftime("%Y %m %d %H:%M", time.localtime())
        nowTimestamp = "%.0f" % time.mktime(time.strptime(now, '%Y %m %d %H:%M'))


        if mode == 'fetch': # DATAS
            datas = {
                    'TimeStamp': nowTimestamp,
                    'Plugin': 'filesTransfered_' + pc,
                    'Values': {
                                'Exist': self._STATUS[pc]['ExistFile'],
                                'New': self._STATUS[pc]['NewFile'],
                                'Total': self._STATUS[pc]['totalFileTransf'],
                               }
            }
            return datas

        else: # INFOS
            dsInfos = {
                    'Exist': {"type": "GAUGE",
                         "id": 'Exist',
                         "draw": 'line',
                         "label": 'Exist'},
                    'New': {"type": "GAUGE",
                         "id": 'New',
                         "draw": 'line',
                         "label": 'New'},
                    'Total': {"type": "GAUGE",
                         "id": 'Total',
                         "draw": 'line',
                         "label": 'Total'},
            }

            infos = {
               'Plugin': 'filesTransfered_' + pc,
               'Describ': 'Number of files transfered',
               'Category': 'Backup '+ pc,
               'Base': '1000',
               'Order': 'Exist New Total',
               'Title': 'Files Transfered',
               'Vlabel': 'Number of files',
               'Infos': dsInfos,
            }

            return infos


    def _numberErrors(self,pc,mode):
        "return number of errors files"
        now = time.strftime("%Y %m %d %H:%M", time.localtime())
        nowTimestamp = "%.0f" % time.mktime(time.strptime(now, '%Y %m %d %H:%M'))


        if mode == 'fetch': # DATAS
            datas = {
                    'TimeStamp': nowTimestamp,
                    'Plugin': 'numberErrors_' + pc,
                    'Values': {
                                'Transfert': self._STATUS[pc]['nbErreurTransfert'],
                                'File': self._STATUS[pc]['nbErreurFile'],
                                'Share': self._STATUS[pc]['nbErreurShare'],
                                'Tar': self._STATUS[pc]['nbErreurTar'],
                                'Total': (self._STATUS[pc]['nbErreurTransfert']+self._STATUS[pc]['nbErreurFile']+self._STATUS[pc]['nbErreurShare']+self._STATUS[pc]['nbErreurTar']),
                               }
            }
            return datas

        else: # INFOS
            dsInfos = {
                    'Transfert': {"type": "GAUGE",
                         "id": 'Transfert',
                         "draw": 'line',
                         "label": 'Transfert'},
                    'File': {"type": "GAUGE",
                         "id": 'File',
                         "draw": 'line',
                         "label": 'File'},
                    'Share': {"type": "GAUGE",
                         "id": 'Share',
                         "draw": 'line',
                         "label": 'Share'},
                    'Tar': {"type": "GAUGE",
                         "id": 'Tar',
                         "draw": 'line',
                         "label": 'Tar'},
                    'Total': {"type": "GAUGE",
                         "id": 'Total',
                         "draw": 'line',
                         "label": 'Total'},
            }

            infos = {
               'Plugin': 'numberErrors_' + pc,
               'Describ': 'Number of files errors',
               'Category': 'Backup '+ pc,
               'Base': '1000',
               'Title': 'Files errors',
               'Vlabel': 'Number of errors',
               'Infos': dsInfos,
            }

            return infos




#        #Taille total transféré
#        #   - #8 : taille Fichiers existants   totalSizeExist
#        #   - #10 : taille Nouveaux fichiers   totalSizeNew
#        print "\nGRAPH : Taille total transféré\n";
#        print $totalFileSize."\n".$totalSizeExist."\n".$totalSizeNew."\n";
#
#
#        #Taille total compressé transféré
#        #   - # 16 : taille Fichiers existants compressé   totalSizeExistFileCompr
#        #   - # 17 : taille Nouveaux fichiers compressé    totalSizeNewFileCompr
#        print "\nGRAPH : Taille total compressé transféré\n";
#        print "Niveau comression : $compressionLvl\n";
#        print $totalSizeExistFileCompr."\n".$totalSizeNewFileCompr."\n";
#
#
#        #Niveau de Compression 
#        #   - #6 : taille Fichiers existants + Nouveaux fichiers    totalFileSize
#        #   - taille compressé  Fichiers existants + Nouveaux fichiers
#        print "\nGRAPH : Niveau de Compression \n";
#        my $tauxCompression = (100 - ( ($totalSizeExistFileCompr+$totalSizeNewFileCompr) * 100) / $totalFileSize );
#        print "taux compression : $tauxCompression\n";
#        print $totalFileSize."\n";
#        print ($totalSizeExistFileCompr+$totalSizeNewFileCompr);
#        print "\n";

    def _backupSize(self,pc,mode):
        "return number of errors files"
        now = time.strftime("%Y %m %d %H:%M", time.localtime())
        nowTimestamp = "%.0f" % time.mktime(time.strptime(now, '%Y %m %d %H:%M'))


        if mode == 'fetch': # DATAS
            datas = {
                    'TimeStamp': nowTimestamp,
                    'Plugin': 'backupSize_' + pc,
                    'Values': {
                                'SizeExistFiles': self._STATUS[pc]['totalSizeExist'],
                                'SizeNewFiles': self._STATUS[pc]['totalSizeNew'],
                                'CompSizeExistFiles': self._STATUS[pc]['totalSizeExistFileCompr'],
                                'CompSizeNewFiles': self._STATUS[pc]['totalSizeNewFileCompr'],
                                'totalCompSize': int(self._STATUS[pc]['totalSizeExistFileCompr'])+int(self._STATUS[pc]['totalSizeNewFileCompr']),
                                'totalSize': int(self._STATUS[pc]['totalSizeExist'])+int(self._STATUS[pc]['totalSizeNew']),
                               }
            }
            return datas

        else: # INFOS
            dsInfos = {
                    'SizeExistFiles': {"type": "GAUGE",
                         "id": 'SizeExistFiles',
                         "draw": 'line',
                         "label": 'SizeExistFiles'},
                    'SizeNewFiles': {"type": "GAUGE",
                         "id": 'SizeNewFiles',
                         "draw": 'line',
                         "label": 'SizeNewFiles'},
                    'CompSizeExistFiles': {"type": "GAUGE",
                         "id": 'CompSizeExistFiles',
                         "draw": 'line',
                         "label": 'CompSizeExistFiles'},
                    'CompSizeNewFiles': {"type": "GAUGE",
                         "id": 'CompSizeNewFiles',
                         "draw": 'line',
                         "label": 'CompSizeNewFiles'},
                    'totalCompSize': {"type": "GAUGE",
                         "id": 'totalCompSize',
                         "draw": 'line',
                         "label": 'totalCompSize'},
                    'totalSize': {"type": "GAUGE",
                         "id": 'totalSize',
                         "draw": 'line',
                         "label": 'totalSize'},
            }

            infos = {
               'Plugin': 'backupSize_' + pc,
               'Describ': 'Size of backup',
               'Category': 'Backup '+ pc,
               'Base': '1000',
               'Order': 'CompSizeExistFiles CompSizeNewFiles SizeExistFiles SizeNewFiles totalCompSize totalSize',
               'Title': 'Size Backup',
               'Vlabel': 'Size in Mo',
               'Infos': dsInfos,
            }

            return infos


    def _compressionRate(self,pc,mode):
        "return the compression rate"
        now = time.strftime("%Y %m %d %H:%M", time.localtime())
        nowTimestamp = "%.0f" % time.mktime(time.strptime(now, '%Y %m %d %H:%M'))


        if mode == 'fetch': # DATAS
            datas = {
                    'TimeStamp': nowTimestamp,
                    'Plugin': 'compressionRate_' + pc,
                    'Values': {
                                'withoutCompression': 0,
                                'Compressed': 100,
                                'CompressionRate': (100 - ((int(self._STATUS[pc]['totalSizeExistFileCompr']) + int(self._STATUS[pc]['totalSizeNewFileCompr']))*100) / int(self._STATUS[pc]['totalFileSize'])),
                               }
            }
            return datas

        else: # INFOS
            dsInfos = {
                    'CompressionRate': {"type": "GAUGE",
                         "id": 'CompressionRate',
                         "draw": 'line',
                         "label": 'CompressionRate'},
            }

            infos = {
               'Plugin': 'compressionRate_' + pc,
               'Describ': 'Backup Compression Rate',
               'Category': 'Backup '+ pc,
               'Order': 'withoutCompression CompressionRate Compressed',
               'Base': '1000',
               'Title': 'Compression Rate',
               'Vlabel': 'Rate in %',
               'Infos': dsInfos,
            }

            return infos

    def _parserLog(self, path):
        "parse backuppc log and return hash table"
        with open (path, 'r') as f:
            lineList = f.readlines()

        #Create status hash whith value in backups
        STATUS = {}
        
        lastline = lineList[-1]
        #print (lastline)

        head = ['backupID', 'backupType', 'startTime', 'endTime', 'totalFileTransf', 'totalFileSize', 'ExistFile', 'totalSizeExist', 'NewFile', 'totalSizeNew', 'nbErreurTransfert', 'nbErreurFile', 'nbErreurShare', 'nbErreurTar', 'compressionLvl', 'totalSizeExistFileCompr', 'totalSizeNewFileCompr']
        for value in re.split("\s", lastline):
            if head:
                #print head[0]+" - "+ value
                STATUS[head.pop(0)] = value
           # else:
           #     print " - "+ value
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
    print str(stats.pluginsRefresh())
