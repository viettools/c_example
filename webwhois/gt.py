# -*- coding: utf-8 -*-
# https://check.rs/

import requests
import re
from bs4 import BeautifulSoup

def parse_gt_data(regex_input, next_regex, raw_data):
    result = False
    pre_result = []
    if raw_data:
        raw_data = raw_data.replace('\n', '')
        raw_data = raw_data.replace('\t', '')
        
        regex_data = re.findall(regex_input, raw_data, re.DOTALL|re.M)
        if regex_data:
            regex_item_data = re.findall(next_regex, regex_data[0], re.DOTALL|re.M)
            for arr in regex_item_data:
                clean_data = BeautifulSoup(arr, features='html.parser').get_text()
                if clean_data:
                    clean_data = clean_data.replace('\xa0', '')
                    clean_data = result = re.sub('\s{2,}', ' ', clean_data)
                    clean_data = clean_data.strip()
                    
                    pre_result.append(clean_data)
    if pre_result:
        result = '\n\t'.join(pre_result)
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
        req_get = req.get('https://www.gt/sitio/whois.php?dn={0}.&lang=en'.format(domain), headers=headers, verify=False)
    except:
        pass
    
    result = []
    raw_data = ''
    if req_get and req_get.status_code == 200 and req_get.text:
        raw_data = req_get.text
        if raw_data:
            
            registrant = parse_gt_data('Entitled Organization(.*?)Servers', '</label>(.*?)</div>', raw_data)
            if registrant:
                result.append('Registry Registrant:\n\t{0}'.format(registrant))
            
            admin = parse_gt_data('ADMINISTRATIVE(.*?)TECHNICAL', '</label>(.*?)</div>', raw_data)
            if admin:
                result.append('Registry Admin:\n\t{0}'.format(admin))
                
            tech = parse_gt_data('TECHNICAL(.*?)<script', '</label>(.*?)</div>', raw_data)
            if tech:
                result.append('Registry Tech:\n\t{0}'.format(tech))
                
            expiry = parse_gt_data('Domain Name Information(.*?)Entitled Organization', '<strong>(.*?)</strong>', raw_data)
            if expiry:
                expiry = expiry.replace('Expiration:', 'Registry Expiry Date:')
                result.append(expiry)
            
            ns_server = parse_gt_data('Servers(.*?)ADMINISTRATIVE', '<strong>(.*?)</strong>', raw_data)
            if ns_server:
                arr_ns_server = ns_server.split('\n')
                for item_ns in arr_ns_server:
                    item_ns = item_ns.strip()
                    if item_ns:
                        result.append('Name Server: {0}'.format(item_ns))
            
    if result:
        result.append('Full WHOIS: https://www.gt')
        final_result = {
            'status': True,
            'result': '\n'.join(result)
        }
    
    return final_result