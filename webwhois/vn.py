# -*- coding: utf-8 -*-
# https://check.rs/

import requests
import re, json
from bs4 import BeautifulSoup

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
        req_get = req.get('https://whois.inet.vn', headers=headers)
    except:
        pass
    
    req_cookie = req.cookies.get_dict()
    
    try:
        req_get = req.get('https://whois.inet.vn/api/whois/domainspecify/{0}'.format(domain), headers=headers, cookies=req_cookie)
    except:
        pass
    
    result = []
    if req_get and req_get.status_code == 200 and req_get.text:
        json_data = req_get.json()
        
        if json_data.get('registrantName', False):
            result.append('Registrant Name: {0}'.format(json_data.get('registrantName')))
        if json_data.get('registrar', False):
            result.append('Registrar: {0}'.format(json_data.get('registrar')))
        if json_data.get('creationDate', False):
            result.append('Creation Date: {0}'.format(json_data.get('creationDate')))
        if json_data.get('expirationDate', False):
            result.append('Registry Expiry Date: {0}'.format(json_data.get('expirationDate')))
        
        for item in json_data.get('nameServer', []):
            result.append('Name Server: {0}'.format(item))
        for item in json_data.get('status', []):
            result.append('Domain Status: {0} https://icann.org/epp'.format(item))
            
    if result:
        result.append('Full WHOIS: https://tracuutenmien.gov.vn/ or https://vnnic.vn/en/whois-information?lang=en')
        final_result = {
            'status': True,
            'result': '\n'.join(result)
        }
    
    return final_result