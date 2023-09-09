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


def sfetch(dom,apkey,rel,fpath,tip):
   dns_words = ['a','aaaa','ns','mx','soa','txt'] # cname still is not implemented for now in securitytrails
   subs = []
   base_url = []
   now = str(datetime.datetime.now())
   huk = 0
   try:
      if(rel=='subdomains'):
         sub_url = 'https://api.securitytrails.com/v1/domain/'+dom+'/subdomains?apikey='+apkey+'&children_only=false&include_inactive=true'
         near_url = 'https://api.securitytrails.com/v1/ips/nearby/'+tip+'?apikey='+apkey
         out_form = 'md'
      elif(rel=='associated'):
         base_url.append('https://api.securitytrails.com/v1/domain/'+dom+'/associated?apikey='+apkey)
         out_form = 'js'
      elif(rel=='whois'):
         base_url.append('https://api.securitytrails.com/v1/history/'+dom+'/whois?apikey='+apkey)
         out_form = 'js'
      elif(rel=='dns'):
         for i in range(len(dns_words)):
            base_url.append('https://api.securitytrails.com/v1/history/<target_domain>/dns/'+dns_words[i]+'?apikey='+apkey)
         out_form = 'js'
      file_save = fpath+'secuiritytrails_'+dom+'_'+now+'_'+rel+'.'+out_form
      if(out_form == 'js'):
         with open(file_save,'a') as res_file:
            for i in range(len(base_url)):
               req = requests.get(base_url)
               resul = req.json()
               res_file.write(str(resul)+'\n\n\n')
            res_file.close()
      elif(out_form == 'md'):
         sreq = requests.get(sub_url)
         sresp = sreq.json()
         for x in range(len(sresp['subdomains'])):
            subs.append(str(sresp['subdomains'][x])+'.'+dom)
         nreq = requests.get(near_url)
         nresp = nreq.json()
         for z in range(len(nresp['blocks'])):
            for j in range(len(nresp['blocks'][z]['hostnames'])):
               subs.append(str(nresp['blocks'][z]['hostnames'][j]))
               huk += 1
         with open(file_save,'a') as res_file:
            for k in range(len(subs)):
               res_file.write(str(subs[k])+'\n')
            res_file.close()
   except Exception as err:
      print(Fore.RED)
      print(err)
      print(Style.RESET_ALL)
      sys.exit()
   #



if __name__=='__main__':
   parser = optparse.OptionParser()
   parser.add_option('-d', action='store', dest='domain' , type='string' , help='target domain name')
   parser.add_option('-i', action='store', dest='tip' , type='string' , help='target ip address(it is necessary for nearby and ip)')
   parser.add_option('-k', action='store', dest='apkey' , default='<YOUR_API_KEY>' , type='string' , help='api key')
   parser.add_option('-e', action='store', dest='funct' , default='subdomains' , type='string' , help='which type of details to find\nsubdomains(will get all subs)\nassociated(needs premium api)\nwhois\ndns(this option is different from finding subdomains using dns records)')
   parser.add_option('-f', action='store', dest='fpath' , type='string' , help='file path to save results')
   # https://docs.securitytrails.com/reference/usage
   # https://securitytrails.com/blog/subdomain-enum-script
   # https://securitytrails.com/corp/api
   # https://api.securitytrails.com/v1/history/<target_domain>/dns/(dns rec names - cname is not accepted)?apikey=<YOUR_API_KEY>
   # https://api.securitytrails.com/v1/domain/<target_domain>/subdomains?apikey=<YOUR_API_KEY>
   # https://api.securitytrails.com/v1/domain/<target_domain>?apikey=<YOUR_API_KEY>
   # https://api.securitytrails.com/v1/ips/nearby/<target_ip>?apikey=<YOUR_API_KEY>
   # https://api.securitytrails.com/v1/history/<target_domain>/whois?apikey=<YOUR_API_KEY>
   # https://api.securitytrails.com/v1/domain/<target_domain>/associated?apikey=<YOUR_API_KEY>
   # https://api.securitytrails.com/v1/ips/stats?ip=<target_ip>&apikey=<YOUR_API_KEY>
   # https://api.securitytrails.com/v1/ips/stats?ptr_part=<target_domain>&apikey=<YOUR_API_KEY>

   options,_ = parser.parse_args()
	#
   if (options.domain and options.apkey and options.funct and options.fpath and options.tip):
      sfetch(options.domain.lower(),options.apkey,options.funct.lower(),options.fpath,options.tip)
   else:
      parser.print_help()
      print(Style.RESET_ALL)
      sys.exit()
