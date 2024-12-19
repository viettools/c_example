# -*- coding: utf-8 -*-
# https://check.rs/

import requests
import re, json
from bs4 import BeautifulSoup

def parse_gm_data(regex_input, raw_data):
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
    
    if domain and domain_type:
        domain_type = '.{0}'.format(domain_type)
        domain = domain.replace(domain_type, '')
    
    final_result = {
        'status': False,
        'result': False
    }
    
    req = requests.Session()
    req_get = False
    try:
        req_get = req.get('http://www.nic.gm/nic-scripts/checkdom.aspx?dname={0}'.format(domain), headers=headers, verify=False)
    except:
        pass
    
    result = []
    if req_get and req_get.status_code == 200 and req_get.text:
        raw_data = req_get.text
        if raw_data:
            registrar_details = parse_gm_data('Registrar \(Company\):(.*?)</p>', raw_data)
            admin_details = parse_gm_data('Admin. contact \(Company\):(.*?)</p>', raw_data)
            technical_details = parse_gm_data('Tech. contact \(Company\):(.*?)</p>', raw_data)
            creation_details = parse_gm_data('Registration date:(.*?)</p>', raw_data)
            
            if registrar_details:
                result.append('Registrar: {0}'.format(registrar_details))
            if admin_details:
                result.append('Admin Name: {0}'.format(admin_details))
            if technical_details:
                result.append('Tech Name: {0}'.format(technical_details))
            if creation_details:
                result.append('Creation Date: {0}'.format(creation_details))
            
            for i in range(0, 10):
                ns_details = parse_gm_data('Name server #{0}:(.*?)</p>'.format(i), raw_data)
                if ns_details:
                    result.append('Name Server: {0}'.format(ns_details))
            
    if result:
        result.append('Full WHOIS: http://www.nic.gm')
        final_result = {
            'status': True,
            'result': '\n'.join(result)
        }
    
    return final_result