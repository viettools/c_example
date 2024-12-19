# -*- coding: utf-8 -*-
# https://check.rs/

import requests
import re
from bs4 import BeautifulSoup

def parse_bt_data(regex_input, raw_data):
    result = False
    if raw_data:
        regex_data = re.findall(regex_input, raw_data, re.DOTALL|re.M)
        if regex_data:
            pre_clean_data = regex_data[0]
            clean_data = BeautifulSoup(pre_clean_data, features='html.parser').get_text()
            if clean_data:
                result = clean_data.strip()
                del clean_data
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
        req_get = req.get('https://nic.bt/search?query={0}&ext={1}'.format(domain, domain_type), headers=headers, verify=False)
    except:
        pass
    
    result = []
    if req_get and req_get.status_code == 200 and req_get.text:
        raw_data = req_get.text
        if raw_data:
            domain_details = parse_bt_data('Domain Details :(.*?)Customer Details', raw_data)
            customer_details = parse_bt_data('Customer Details :(.*?)Technical Details', raw_data)
            technical_details = parse_bt_data('Technical Details :(.*?)Billing Details :', raw_data)
            billing_details = parse_bt_data('Billing Details :(.*?)</div>', raw_data)
            
            if domain_details:
                domain_details = domain_details.replace('Registration Date :', 'Creation Date: ')
                domain_details = domain_details.replace('Expiration Date:', 'Registry Expiry Date: ')
                result.append(domain_details)
            if customer_details:
                result.append(customer_details)
            if technical_details:
                result.append(technical_details)
            if billing_details:
                result.append(billing_details)
    if result:
        result.append('Full WHOIS: https://nic.bt')
        final_result = {
            'status': True,
            'result': '\n'.join(result)
        }
    
    return final_result