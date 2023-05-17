import sys
import os
import optparse
import re
from colorama import Fore, Style
import json
from OTXv2 import OTXv2
import IndicatorTypes
import datetime
#from optparse import OptionGroup

def aliendom(tdom,fpath,otx):
   now = str(datetime.datetime.now())
   file_save = fpath+'alienvault_'+tdom+'_'+now
   full_result = otx.get_indicator_details_full(IndicatorTypes.DOMAIN, tdom)
   pdata = input(Fore.CYAN+'\nSpecify which type of data you want to be saved\nAvailable options are(full , general , geo , malware , url_list , passive_dns , whois , http_scans): '+Style.RESET_ALL)
   if(str(pdata).lower() == 'full'):
      with open(file_save+'_FullData.json','a') as fullfile:
         fullfile.write(json.dumps(full_result))
         fullfile.close()
   elif(str(pdata).lower() == 'general'):
      if('general' in full_result):
         with open(file_save+'_general.json','a') as fullfile:
            fullfile.write(json.dumps(full_result['general']))
            fullfile.close()
   elif(str(pdata).lower() == 'geo'):
      if('geo' in full_result):
         with open(file_save+'_geo.json','a') as fullfile:
            fullfile.write(json.dumps(full_result['geo']))
            fullfile.close()
   elif(str(pdata).lower() == 'malware'):
      if('malware' in full_result):
         with open(file_save+'_malware.json','a') as fullfile:
            fullfile.write(json.dumps(full_result['malware']))
            fullfile.close()
   elif(str(pdata).lower() == 'url_list'):
      if('url_list' in full_result):
         with open(file_save+'_url_list.json','a') as fullfile:
            fullfile.write(json.dumps(full_result['url_list']))
            fullfile.close()
   elif(str(pdata).lower() == 'passive_dns'):
      if('passive_dns' in full_result):
         for i in range(len(full_result['passive_dns']['passive_dns'])):
            with open(file_save+'_passive_dns.md','a') as fullfile:
               fullfile.write(str(full_result['passive_dns']['passive_dns'][i]['hostname'])+'\n')
               if(str(full_result['passive_dns']['passive_dns'][i]['record_type']).lower() == 'cname'):
                  fullfile.write(str(full_result['passive_dns']['passive_dns'][i]['address'])+'\n')
               fullfile.close()
   elif(str(pdata).lower() == 'whois'):
      if('whois' in full_result):
         with open(file_save+'_whois.json','a') as fullfile:
            fullfile.write(json.dumps(full_result['whois']))
            fullfile.close()
   elif(str(pdata).lower() == 'http_scans'):
      if('http_scans' in full_result):
         with open(file_save+'_http_scans.json','a') as fullfile:
            fullfile.write(json.dumps(full_result['http_scans']))
            fullfile.close()
   else:
      with open(file_save+'_http_scans.md','a') as fullfile:
         fullfile.write('[!] PROVIDED DATA TYPE IS NOT AVAILABLE [!]\n')
         fullfile.close()


def alienip(tip,fpath,otx):
   now = str(datetime.datetime.now())
   file_save = fpath+'alienvault_ip_'+tip+'_'+now
   full_result = otx.get_indicator_details_full(IndicatorTypes.IPv4, tip)
   with open(file_save+'.json','a') as fullfile:
      fullfile.write(json.dumps(full_result))
      fullfile.close()


def alienhost(thost,fpath,otx):
   now = str(datetime.datetime.now())
   file_save = fpath+'alienvault_host_'+thost+'_'+now
   full_result = otx.get_indicator_details_full(IndicatorTypes.HOSTNAME, thost)
   with open(file_save+'.json','a') as fullfile:
      fullfile.write(json.dumps(full_result))
      fullfile.close()


def alienurl(turl,fpath,otx):
   now = str(datetime.datetime.now())
   file_save = fpath+'alienvault_url_'+turl+'_'+now
   full_result = otx.get_indicator_details_full(IndicatorTypes.URL, turl)
   with open(file_save+'.json','a') as fullfile:
      fullfile.write(json.dumps(full_result))
      fullfile.close()


def alienmd5(tmd5,fpath,otx):
   now = str(datetime.datetime.now())
   file_save = fpath+'alienvault_MD5_'+tmd5+'_'+now
   full_result = otx.get_indicator_details_full(IndicatorTypes.FILE_HASH_MD5, tmd5)
   with open(file_save+'.json','a') as fullfile:
      fullfile.write(json.dumps(full_result))
      fullfile.close()


def alienpulse(tpulse,fpath,otx):
   now = str(datetime.datetime.now())
   file_save = fpath+'alienvault_pulse_'+tpulse+'_'+now
   full_result = otx.search_pulses(tpulse)
   with open(file_save+'.json','a') as fullfile:
      fullfile.write(json.dumps(full_result))
      fullfile.close()


def aliensubscribed(usubs,fpath,otx):
   now = str(datetime.datetime.now())
   file_save = fpath+'alienvault_subscribed_'+usubs+'_'+now
   full_result = otx.getall(max_items=3, limit=5)
   with open(file_save+'.json','a') as fullfile:
      fullfile.write(json.dumps(full_result))
      fullfile.close()




if __name__=='__main__':
   parser = optparse.OptionParser()
   parser.add_option('-d', action='store', dest='tdom' , type='string' , help='Domain eg; alienvault.com')
   parser.add_option('-k', action='store', dest='apkey' , default='<YOUR_API_KEY>' , type='string' , help='api key')
   parser.add_option('-f', action='store', dest='fpath' , type='string' , help='file path to save results')
   parser.add_option('-i', action='store', dest='tip' , type='string' , help='IP eg; 4.4.4.4')
   parser.add_option('-w', action='store', dest='thost' , type='string' , help='Hostname eg; www.alienvault.com')
   parser.add_option('-u', action='store', dest='turl' , type='string' , help='URL eg; http://www.alienvault.com')
   parser.add_option('-m', action='store', dest='tmd5' , type='string' , help='MD5 Hash of a file eg; 7b42b35832855ab4ff37ae9b8fa9e571')
   parser.add_option('-p', action='store', dest='tpulse' , type='string' , help='Search pulses for a string eg; Dridex')
   parser.add_option('-s', action='store', dest='usubs' , type='string' , help='Get pulses you subscribed to')
   # https://otx.alienvault.com/assets/static/external_api.html
   options,_ = parser.parse_args()
	#
   otx = OTXv2(options.apkey)
   if (options.tdom,options.fpath):
      aliendom(options.tdom,options.fpath,otx)
   elif (options.tip,options.fpath):
      alienip(options.tdip,options.fpath,otx)
   elif (options.thost,options.fpath):
      alienhost(options.thost,options.fpath,otx)
   elif (options.turl,options.fpath):
      alienurl(options.turl,options.fpath,otx)
   elif (options.tmd5,options.fpath):
      alienmd5(options.tmd5,options.fpath,otx)
   elif (options.tpulse,options.fpath):
      alienpulse(options.tpulse,options.fpath,otx)
   elif (options.usubs,options.fpath):
      aliensubscribed(options.usubs,options.fpath,otx)
   else:
      print(Fore.LIGHTMAGENTA_EX)
      parser.print_help()
      print(Style.RESET_ALL)
      sys.exit()
