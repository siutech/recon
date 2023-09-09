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


def htar(tip,fpath):
   rev_domains = []
   rev_ips = []
   now = str(datetime.datetime.now())
   revip = 'https://api.hackertarget.com/reverseiplookup/?q='+tip
   revdns = 'https://api.hackertarget.com/reversedns/?q='+tip
   dom = str(input(Fore.CYAN+'\nEnter target name: '+Style.RESET_ALL))
   rev_dom = fpath+'hackertarget_Domains_reverseQueries_'+dom+'_'+now+'.md'
   rev_ip = fpath+'hackertarget_IPs_reverseQueries_'+dom+'_'+now+'.md'
   try:
      req_ip = requests.get(revip)
      req_dns = requests.get(revdns)
      ip_resul = req_ip.text.split('\n')
      dns_resul = req_dns.text.split('\n')
      for i in range(len(ip_resul)):
         rev_domains.append(ip_resul[i])
      for i in range(len(dns_resul)):
         rev_domains.append(dns_resul[i].split(' ')[1])
         rev_ips.append(dns_resul[i].split(' ')[0])
      with open(rev_dom,'a') as subfile:
         for i in range(len(rev_domains)):
            subfile.write(str(rev_domains[i])+'\n')
         subfile.close()
      with open(rev_ip,'a') as ipfile:
         for i in range(len(rev_ips)):
            ipfile.write(str(rev_ips[i])+'\n')
         ipfile.close()
   except Exception as err:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      print(Fore.RED)
      print(str(err)+'\t -> ERROR IN LINE: '+str(exc_tb.tb_lineno))
      print(Style.RESET_ALL)
      sys.exit()



if __name__=='__main__':
   parser = optparse.OptionParser()
   parser.add_option('-d', action='store', dest='tip' , type='string' , help='target ip address')
   parser.add_option('-f', action='store', dest='fpath' , type='string' , help='file path to save results')
   options,_ = parser.parse_args()
	#
   if (options.tip and options.fpath):
      htar(options.tip,options.fpath)
   else:
      parser.print_help()
      print(Style.RESET_ALL)
      sys.exit()
