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


def cspot(dom,fpath):
   subs = []
   now = str(datetime.datetime.now())
   try:
      base_url = 'https://api.certspotter.com/v1/issuances?domain='+dom+'&include_subdomains=true&expand=dns_names&expand=issuer&expand=revocation&expand=problem_reporting&expand=cert_der'
      file_save = fpath+'certspotter'+dom+'_'+now+'_.md'
      req_cs = requests.get(base_url)
      resul = req_cs.json()
      for i in range(len(resul)):
         for j in range(len(resul[i]['dns_names'])):
            subs.append(resul[i]['dns_names'][j])
      with open(file_save,'a') as res_file:
         for i in range(len(subs)):
            res_file.write(str(subs[i])+'\n')
         res_file.close()
   except Exception as err:
      print(Fore.RED)
      print(err)
      print(Style.RESET_ALL)
      sys.exit()



if __name__=='__main__':
   parser = optparse.OptionParser()
   parser.add_option('-d', action='store', dest='domain' , type='string' , help='target domain name')
   parser.add_option('-f', action='store', dest='fpath' , type='string' , help='file path to save results')
   options,_ = parser.parse_args()
	#
   if (options.domain and options.fpath):
      cspot(options.domain.lower(),options.fpath)
   else:
      parser.print_help()
      print(Style.RESET_ALL)
      sys.exit()