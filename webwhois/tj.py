# -*- coding: utf-8 -*-
# https://check.rs/

import requests
import re
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
        req_get = req.get('https://nets.tj/nic/?domain={0}'.format(domain), headers=headers, verify=False)
    except:
        pass
    
    result = []
    if req_get and req_get.status_code == 200 and req_get.text:
        json_data = req_get.json()
        if json_data:
            if json_data.get('registrar', False):
                result.append('Registrar: {0}'.format(json_data['registrar']))
            if json_data.get('hostname', False):
                result.append('Name Server: {0}'.format(json_data['hostname']))
            if json_data.get('registration date', False):
                result.append('Creation Date: {0}'.format(json_data.get('registration date')))
            if json_data.get('status', False):
                result.append('Domain Status: {0} https://icann.org/epp'.format(json_data.get('status')))
        
        if result:
            result.append('Full WHOIS: http://www.nic.tj/whois.html')
            final_result = {
                'status': True,
                'result': '\n'.join(result)
            }
    
    return final_result