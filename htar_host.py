import sys
import os
import optparse
import re
from colorama import Fore, Back, Style
import string
import requests
import json
import datetime
#from optparse import OptionGroup


def htar(dom,fpath):
   subs = []
   ips = []
   now = str(datetime.datetime.now())
   try:
      base_url = 'https://api.hackertarget.com/hostsearch/?q='+dom
      sub_save = fpath+'hackertarget_subs_'+dom+'_'+now+'.md'
      ip_save = fpath+'hackertarget_ips_'+dom+'_'+now+'.md'
      req_cs = requests.get(base_url)
      resul = req_cs.text.split('\n')
      for i in range(len(resul)-1):
         subs.append(resul[i].split(',')[0])
         ips.append(resul[i].split(',')[1])
      with open(sub_save,'a') as sub_file:
         for i in range(len(subs)):
            sub_file.write(str(subs[i])+'\n')
         sub_file.close()
      with open(ip_save,'a') as ip_file:
         for i in range(len(ips)):
            ip_file.write(str(ips[i])+'\n')
         ip_file.close()
   except Exception as err:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      print(Fore.RED)
      print(str(err)+'\t -> ERROR IN LINE: '+str(exc_tb.tb_lineno))
      print(Style.RESET_ALL)
      sys.exit()



if __name__=='__main__':
   parser = optparse.OptionParser()
   parser.add_option('-d', action='store', dest='domain' , type='string' , help='target domain name')
   parser.add_option('-f', action='store', dest='fpath' , type='string' , help='file path to save results')
   options,_ = parser.parse_args()
	#
   if (options.domain and options.fpath):
      htar(options.domain.lower(),options.fpath)
   else:
      parser.print_help()
      print(Style.RESET_ALL)
      sys.exit()