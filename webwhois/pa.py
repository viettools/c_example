# -*- coding: utf-8 -*-
# https://check.rs/

import requests
import re, json
from bs4 import BeautifulSoup

def parse_pa_data(regex_input, raw_data):
    result = False
    if raw_data:
        regex_data = re.findall(regex_input, raw_data, re.DOTALL|re.M)
        if regex_data:
            pre_clean_data = regex_data[0]
            clean_data = BeautifulSoup(pre_clean_data, features='html.parser').get_text()
            if clean_data:
                result = clean_data.strip()
                del clean_data
    
    if result:
        result = re.sub(r'\n(?=\n)', '', result)
        result = re.sub('\s{2,}', ' ', result)
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
        req_get = req.get('https://nic.pa:8080/whois/{0}'.format(domain), headers=headers, verify=False)
    except:
        pass
    
    result = []
    if req_get and req_get.status_code == 200 and req_get.json():
        raw_data = req_get.json()
        if raw_data and raw_data.get('status', False) == 200 and raw_data.get('payload', {}):
            creation_details = raw_data['payload']['fecha_creacion']
            updated_date_details = raw_data['payload']['fecha_actualizacion']
            expiry_date_details = raw_data['payload']['fecha_expiracion']
            status_details = raw_data['payload']['Estatus']
            
            if creation_details:
                result.append('Creation Date: {0}'.format(creation_details))
            if updated_date_details:
                result.append('Updated Date: {0}'.format(updated_date_details))
            if expiry_date_details:
                result.append('Registry Expiry Date: {0}'.format(expiry_date_details))
            if status_details:
                result.append('Domain Status: {0} https://icann.org/epp'.format(status_details))
            
            ns_details = raw_data['payload']['NS']
            for ns_server in ns_details:
                result.append('Name Server: {0}'.format(ns_server.strip()))
            
    if result:
        result.append('Full WHOIS: https://nic.pa/en/whois')
        final_result = {
            'status': True,
            'result': '\n'.join(result)
        }
    
    return final_result