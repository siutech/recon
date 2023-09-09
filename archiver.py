import sys
import os
import optparse
import re
from colorama import Fore, Back, Style
import string
import requests
import json
from urllib.parse import urlparse
import datetime
#from optparse import OptionGroup


def archiver(dom,fpath):
   base_url = 'https://web.archive.org/cdx/search/cdx?url=*.'+dom+'/*&output=json&fl=original&collapse=urlkey'
   subs = []
   try:
      req = requests.get(base_url)
   except Exception as erra:
      print(Fore.RED)
      print(erra)
      print(Style.RESET_ALL)
      sys.exit()
   presub = req.json()
   for i in range(len(presub)):
      if(i != 0):
         subs.append(urlparse(presub[i][0]).netloc)
   subs = list(set(subs))
   now = str(datetime.datetime.now())
   file_save = fpath+'archive.org_'+dom+'_'+now+'.md'
   with open(file_save,'a') as subfile:
      for i in range(len(subs)):
         subfile.write(subs[i]+'\n')
      subfile.close()


if __name__=='__main__':
   parser = optparse.OptionParser()
   parser.add_option('-d', action='store', dest='domain' , type='string' , help='target domain name')
   parser.add_option('-f', action='store', dest='fpath' , type='string' , help='file path to save results')
   # https://web.archive.org/cdx/search/cdx?url=*.<target_domain>/*&output=json&fl=original&collapse=urlkey
   options,_ = parser.parse_args()
	#
   if (options.domain and options.fpath):
      archiver(options.domain.lower(),options.fpath)
   else:
      parser.print_help()
      print(Style.RESET_ALL)
      sys.exit()