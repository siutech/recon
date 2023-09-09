import sys
import os
import optparse
import re
from colorama import Fore, Back, Style
import string
import requests
import time
import json
import datetime
#from optparse import OptionGroup


def uscan(quer,apkey,fpath,kword):
   headreqs = {
      "Content-Type": "application/json",
      "API-Key": apkey
   }
   if(kword == 'domain'):
      base_url = 'https://urlscan.io/api/v1/search/?q='+kword+':*.'+quer+'&size=1000'
   elif(kword != 'domain'):
      base_url = 'https://urlscan.io/api/v1/search/?q='+kword+':'+quer+'&size=1000'
   now = str(datetime.datetime.now())
   file_save = fpath+'urlscan.io_'+quer+'_'+now
   try:
      requ = requests.get(base_url,headers=headreqs,timeout=60)
      response_pack = requ.json()
      if(kword == 'domain'):
         with open(file_save+'.md','a') as subfile:
            for i in range(len(response_pack['results'])):
               subfile.write(response_pack['results'][i]['task']['domain']+'\n')
               if('apexDomain' in response_pack['results'][i]['task']):
                  subfile.write(response_pack['results'][i]['task']['apexDomain']+'\n')
            subfile.close()
      elif(kword != 'domain'):
         with open(file_save+'.json','a') as subfile:
            if('results' in response_pack):
               if(len(response_pack['results']) > 0):
                  subfile.write(json.dumps(response_pack['results']))
               elif(len(response_pack['results']) <= 0):
                  subfile.write(json.dumps('''Searched keyword didn't return any results'''))
            elif('results' not in response_pack):
               subfile.write(json.dumps(response_pack['message']))
            subfile.close()
   except Exception as err:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      print(Fore.RED)
      print(str(err)+'\t -> ERROR IN LINE: '+str(exc_tb.tb_lineno))
      print(sys.exc_info())
      print(Style.RESET_ALL)
      sys.exit()



if __name__=='__main__':
   parser = optparse.OptionParser()
   parser.add_option('-q', action='store', dest='quer' , type='string' , help='query that you want to search in github')
   parser.add_option('-k', action='store', dest='apkey' , default='<YOUR_API_KEY>' , type='string' , help='api key')
   parser.add_option('-f', action='store', dest='fpath' , type='string' , help='file path to save results')
   parser.add_option('-w', action='store', dest='kword' , default='domain' , type='string' , help='search keyword')
   # https://urlscan.io/docs/search/ search keywords
   options,_ = parser.parse_args()
	#
   if (options.quer and options.apkey and options.fpath and options.kword):
      uscan(options.quer,options.apkey,options.fpath,options.kword.lower())
   else:
      parser.print_help()
      print(Style.RESET_ALL)
      sys.exit()
