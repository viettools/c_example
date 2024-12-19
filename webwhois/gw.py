# -*- coding: utf-8 -*-
# https://check.rs/

import requests
import re
from bs4 import BeautifulSoup

def parse_gw_general_data(regex_input, next_regex, raw_data):
    result = False
    pre_result = []
    if raw_data:
        raw_data = raw_data.replace('\n', '')
        raw_data = raw_data.replace('\t', '')
        raw_data = raw_data.replace('\r', '')
        
        regex_data = re.findall(regex_input, raw_data, re.DOTALL|re.M)
        if regex_data:
            if next_regex:
                regex_item_data = re.findall(next_regex, regex_data[0], re.DOTALL|re.M)
            else:
                regex_item_data = regex_data
            for arr in regex_item_data:
                clean_data = BeautifulSoup(arr, features='html.parser').get_text()
                if clean_data:
                    clean_data = result = re.sub('\s{2,}', ' ', clean_data)
                    clean_data = clean_data.strip()
                    
                    pre_result.append(clean_data)
    if pre_result:
        result = '\n'.join(pre_result)
    return result

def parse_gw_contact_data(regex_input, raw_data):
    result = False
    if raw_data:
        arr_rep = [['\n', ''], ['\t', ''], ['\r', ''], ['<label>', '\n'], ['</label>', ' ']]
        for item_rep in arr_rep:
            raw_data = raw_data.replace(item_rep[0], item_rep[1])
        
        regex_data = re.findall(regex_input, raw_data, re.DOTALL|re.M)
        if regex_data:
            clean_data = BeautifulSoup(regex_data[0], features='html.parser').get_text()
            
            if clean_data:
                spl_clean = clean_data.split('\n')
                pre_result = []
                for item_spl in spl_clean:
                    item_spl = item_spl.strip()
                    if item_spl:
                        pre_result.append(item_spl)
                
                if pre_result:
                    result = '\n\t'.join(pre_result)
                del clean_data
    
    return result

def whois_via_web(USER_AGENT, domain, domain_type):
    headers = {
        'User-Agent': USER_AGENT
    }
    
    final_result = {
        'status': False,
        'result': False
    }
    
    req = requests.Session()
    req_get = False
    try:
        req_get = req.get('https://registar.nic.gw/whois/{0}/'.format(domain), headers=headers, verify=False)
    except:
        pass
    
    result = []
    raw_data = ''
    if req_get and req_get.status_code == 200 and req_get.text:
        raw_data = req_get.text
        if raw_data:
                
            creation_details = parse_gw_general_data('<label>Data Submissão:</label>(.*?)<label>Data Expiração:</label>', False, raw_data)
            if creation_details:
                result.append('Creation Date: {0}'.format(creation_details))
            
            expiry_details = parse_gw_general_data('<label>Data Expiração:</label>(.*?)<label>Estado:</label>', False, raw_data)
            if expiry_details:
                result.append('Registry Expiry Date: {0}'.format(expiry_details))
            
            status_details = parse_gw_general_data('<label>Estado:</label>(.*?)</fieldset>', False, raw_data)
            if status_details:
                result.append('Domain Status: {0} {1}'.format(status_details, 'https://icann.org'))
            
    if result:
        result.append('Full WHOIS: https://nic.gw/en/')
        final_result = {
            'status': True,
            'result': '\n'.join(result)
        }
    
    return final_result