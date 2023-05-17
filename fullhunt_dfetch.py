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


def dfetch(dom,apkey,rel,fpath):
   dom_url = 'https://fullhunt.io/api/v1/domain/'+dom+'/details'
   subdom_url = 'https://fullhunt.io/api/v1/domain/'+dom+'/subdomains'
   host_url = 'https://fullhunt.io/api/v1/host/'+dom
   subs = []
   a_rec = []
   aaaa_rec = []
   dns_ptr = []
   Dcname = []
   ip_addrr = []
   asn_num = []
   isp_name = []
   available_ports = []
   try:
      if(rel == 'domain'):
         base_url = dom_url
      elif(rel == 'host'):
         base_url = host_url
      else:
         base_url = subdom_url
      req = requests.get(base_url, headers={'X-API-KEY':apkey})
   except Exception as erra:
      print(Fore.RED)
      print(erra)
      print(Style.RESET_ALL)
      sys.exit()
   presub = req.json()
   if(rel == 'subdomains'):
      for i in range(len(presub['hosts'])):
         subs.append(presub['hosts'][i])
   if(rel == 'domain'):
      for i in range(len(presub['hosts'][0]['dns']['a'])):
         a_rec.append(presub['hosts'][0]['dns']['a'][i])
      if(presub['hosts'][0]['dns']['cname'] is not None):
         for i in range(len(presub['hosts'][0]['dns']['cname'])):
            Dcname.append(presub['hosts'][0]['dns']['cname'][i])
      ip_addrr.append(presub['hosts'][0]['ip_address'])
      if(isinstance(presub['hosts'][0]['ip_metadata']['asn'] , int)):
         asn_num.append(presub['hosts'][0]['ip_metadata']['asn'])
      else:
         for i in range(len(presub['hosts'][0]['ip_metadata']['asn'])):
            asn_num.append(presub['hosts'][0]['ip_metadata']['asn'][i])
      for i in range(len(presub['hosts'][0]['network_ports'])):
         available_ports.append(presub['hosts'][0]['network_ports'][i])
   elif(rel == 'host'):
      for i in range(len(presub['dns']['a'])):
         a_rec.append(presub['dns']['a'][i])
      if(presub['dns']['aaaa'] is not None):
         for i in range(len(presub['dns']['aaaa'])):
            aaaa_rec.append(presub['dns']['aaaa'][i])
      for i in range(len(presub['dns']['cname'])):
         Dcname.append(presub['dns']['cname'][i])
      for i in range(len(presub['dns']['ptr'])):
         dns_ptr.append(presub['dns']['ptr'][i])
      ip_addrr.append(presub['ip_address'])
      if(isinstance(presub['ip_metadata']['asn'] , int)):
         asn_num.append(presub['ip_metadata']['asn'])
      else:
         for i in range(len(presub['ip_metadata']['asn'])):
            asn_num.append(presub['ip_metadata']['asn'][i])
      isp_name.append(presub['ip_metadata']['isp'])
      for i in range(len(presub['network_ports'])):
         available_ports.append(presub['network_ports'][i])
   #
   now = str(datetime.datetime.now())
   file_save = fpath+'fullhunt_'+dom+'_'+now+'_'+rel+'.md'
   with open(file_save,'a') as p2_file:
      if(rel == 'subdomains'):
         for i in range(len(subs)):
            p2_file.write(subs[i]+'\n')
      elif(rel == 'domain'):
         p2_file.write('* DNS A record:\n')
         for i in range(len(a_rec)):
            p2_file.write('\t'+str(a_rec[i])+'\n')
         p2_file.write('\n* DNS CNAME record:\n')
         for i in range(len(Dcname)):
            p2_file.write('\t'+str(Dcname[i])+'\n')
         p2_file.write('\n* Available IP Addresses:\n')
         for i in range(len(ip_addrr)):
            p2_file.write('\t'+str(ip_addrr[i])+'\n')
         p2_file.write('\n* ASN Addresses:\n')
         for i in range(len(asn_num)):
            p2_file.write('\t'+str(asn_num[i])+'\n')
         p2_file.write('\n* ISP name:\n')
         for i in range(len(isp_name)):
            p2_file.write('\t'+str(isp_name[i])+'\n')
         p2_file.write('\n* Available TCP ports:\n')
         for i in range(len(available_ports)):
            p2_file.write('\t'+str(available_ports[i])+'\n')
      elif(rel == 'host'):
         p2_file.write('* DNS A record:\n')
         for i in range(len(a_rec)):
            p2_file.write('\t'+str(a_rec[i])+'\n')
         p2_file.write('\n* DNS AAAA record:\n')
         for i in range(len(aaaa_rec)):
            p2_file.write('\t'+str(aaaa_rec[i])+'\n')
         p2_file.write('\n* DNS ptr record:\n')
         for i in range(len(dns_ptr)):
            p2_file.write('\t'+str(dns_ptr[i])+'\n')
         p2_file.write('\n* DNS CNAME record:\n')
         for i in range(len(Dcname)):
            p2_file.write('\t'+str(Dcname[i])+'\n')
         p2_file.write('\n* Available IP Addresses:\n')
         for i in range(len(ip_addrr)):
            p2_file.write('\t'+str(ip_addrr[i])+'\n')
         p2_file.write('\n* ASN Addresses:\n')
         for i in range(len(asn_num)):
            p2_file.write('\t'+str(asn_num[i])+'\n')
         p2_file.write('\n* ISP name:\n')
         for i in range(len(isp_name)):
            p2_file.write('\t'+str(isp_name[i])+'\n')
         p2_file.write('\n* Available TCP ports:\n')
         for i in range(len(available_ports)):
            p2_file.write('\t'+str(available_ports[i])+'\n')
      #
      p2_file.close()



if __name__=='__main__':
   parser = optparse.OptionParser()
   parser.add_option('-d', action='store', dest='domain' , type='string' , help='target domain name')
   parser.add_option('-k', action='store', dest='apkey' , default='<YOUR_API_KEY>' , type='string' , help='api key')
   parser.add_option('-e', action='store', dest='funct' , default='subdomains' , type='string' , help='which type of details to find\ndomain,host,subdomains')
   parser.add_option('-f', action='store', dest='fpath' , type='string' , help='file path to save results')
   # https://api-docs.fullhunt.io/
   options,_ = parser.parse_args()
	#
   if (options.domain and options.apkey and options.funct and options.fpath):
      dfetch(options.domain.lower(),options.apkey,options.funct.lower(),options.fpath)
   else:
      parser.print_help()
      print(Style.RESET_ALL)
      sys.exit()
