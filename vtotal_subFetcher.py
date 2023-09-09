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


def vt_sub(dom,apkey,rel,fpath):
   base_url = 'https://www.virustotal.com/api/v3/domains/'+dom+'/'+rel
   subs = []
   try:
      req = requests.get(base_url, headers={'X-Apikey':apkey})
   except Exception as erra:
      print(Fore.RED)
      print(erra)
      print(Style.RESET_ALL)
      sys.exit()
   presub = req.json()
   sub_count = presub['meta']['count']
   fetch_url = base_url+'?limit='+str(sub_count+1)
   try:
      mreq = requests.get(fetch_url, headers={'X-Apikey':apkey})
   except Exception as err:
      print(Fore.RED)
      print(err)
      print(Style.RESET_ALL)
      sys.exit()
   sub_j = mreq.json()
   for cou in range(sub_count):
      subs.append(sub_j['data'][cou]['id'])
   #
   now = str(datetime.datetime.now())
   file_save = fpath+'vt_'+dom+'_'+now+'_'+rel+'.md'
   with open(file_save,'a') as p2_file:
      for i in range(len(subs)):
         p2_file.write(subs[i]+'\n')
      p2_file.close()



if __name__=='__main__':
   parser = optparse.OptionParser()
   parser.add_option('-d', action='store', dest='domain' , type='string' , help='target domain name')
   parser.add_option('-k', action='store', dest='apkey' , default='<YOUR_API_KEY>' , type='string' , help='api key')
   parser.add_option('-r', action='store', dest='rel' , default='subdomains' , type='string' , help='relation type - default is subdomains\nthese relations are available with free api key:subdomains, historical_ssl_certificates, historical_whois, immediate_parent, parent, referrer_files, resolutions, siblings')
   parser.add_option('-f', action='store', dest='fpath' , type='string' , help='file path to save results')
   # https://developers.virustotal.com/reference/domains-1#relationships
   options,_ = parser.parse_args()
	#
   if (options.domain and options.apkey and options.rel and options.fpath):
      vt_sub(options.domain.lower(),options.apkey,options.rel,options.fpath)
   else:
      parser.print_help()
      print(Style.RESET_ALL)
      sys.exit()
