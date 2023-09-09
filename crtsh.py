import sys
import os
import optparse
from colorama import Fore, Style
import json
import datetime
import requests
#from optparse import OptionGroup

def crtsher(quer,fpath):
   now = str(datetime.datetime.now())
   file_save = fpath+'crt.sh_'+quer+'_'+now+'.md'
   base_url = 'https://crt.sh/?q='+quer+'&output=json'
   try:
      req = requests.get(base_url,timeout=600)
      fullres = req.json()
      with open(file_save,'a') as resfile:
         for i in range(len(fullres)):
            resfile.write(str(fullres[i]['common_name'])+'\n')
         resfile.close()
   except Exception as err:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      print(Fore.RED)
      print(str(err)+'\t -> ERROR IN LINE: '+str(exc_tb.tb_lineno))
      print(sys.exc_info())
      print(Style.RESET_ALL)
      sys.exit()



if __name__=='__main__':
   parser = optparse.OptionParser()
   parser.add_option('-q', action='store', dest='squer' , type='string' , help='query you want to search about it')
   parser.add_option('-f', action='store', dest='fpath' , type='string' , help='file path to save results')
   # https://crt.sh/?q=<target_domain>&output=json
   # https://crt.sh/?a=1 - advanced search in crt.sh
   options,_ = parser.parse_args()
	#
   if (options.squer,options.fpath):
      crtsher(options.squer,options.fpath)
   else:
      print(Fore.LIGHTMAGENTA_EX)
      parser.print_help()
      print(Style.RESET_ALL)
      sys.exit()
