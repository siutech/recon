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


def gitter(quer,apkey,fpath):
   page_num = 1
   base_url = 'https://api.github.com/search/code?q='+quer+'&per_page=100&page='+str(page_num)
   headreqs = {
      "Accept": "application/vnd.github+json",
      "Authorization": "Bearer "+apkey,
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "Awesome-kotlet-konande-App"
   }
   response_pack = {}
   try:
      requ = requests.get(base_url,headers=headreqs,timeout=60)
      firstresp = requ.json()
      for i in range(len(firstresp['items'])):
         response_pack[i] = firstresp['items'][i]
         data_index = i
      if((int(firstresp['total_count'])/100) > (int(firstresp['total_count'])//100)):
         max_page = (int(firstresp['total_count'])//100) + 1
      elif((int(firstresp['total_count'])/100) == (int(firstresp['total_count'])//100)):
         max_page = (int(firstresp['total_count'])//100)
      if(max_page < 11):
         for i in range(2,max_page+1,1):
            time.sleep(7)
            made_url = 'https://api.github.com/search/code?q='+quer+'&per_page=100&page='+str(i)
            next_req = requests.get(made_url,headers=headreqs,timeout=60)
            next_res = next_req.json()
            for j in range(len(next_res['items'])):
               data_index += 1
               response_pack[data_index] = next_res['items'][j]
      elif(max_page > 10):
         for i in range(2,11,1):
            time.sleep(7)
            made_url = 'https://api.github.com/search/code?q='+quer+'&per_page=100&page='+str(i)
            next_req = requests.get(made_url,headers=headreqs,timeout=60)
            next_res = next_req.json()
            for j in range(len(next_res['items'])):
               data_index += 1
               response_pack[data_index] = next_res['items'][j]
      now = str(datetime.datetime.now())
      file_save = fpath+'github_'+quer+'_'+now+'.json'
      with open(file_save,'a') as outfile:
         outfile.write(json.dumps(response_pack))
         outfile.close()
   except Exception as err:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      if(response_pack):
         now = str(datetime.datetime.now())
         file_save = fpath+'github_'+quer+'_'+now+'.json'
         with open(file_save,'a') as outfile:
            outfile.write(json.dumps(response_pack))
            outfile.close()
      print(Fore.RED)
      print(str(err)+'\t -> ERROR IN LINE: '+str(exc_tb.tb_lineno))
      print(Style.RESET_ALL)
      sys.exit()



if __name__=='__main__':
   parser = optparse.OptionParser()
   parser.add_option('-q', action='store', dest='quer' , type='string' , help='query that you want to search in github')
   parser.add_option('-k', action='store', dest='apkey' , default='<YOUR_API_KEY>' , type='string' , help='api key')
   parser.add_option('-f', action='store', dest='fpath' , type='string' , help='file path to save results')
   # https://developers.virustotal.com/reference/domains-1#relationships
   options,_ = parser.parse_args()
	#
   if (options.quer and options.apkey and options.fpath):
      gitter(options.quer,options.apkey,options.fpath)
   else:
      parser.print_help()
      print(Style.RESET_ALL)
      sys.exit()
