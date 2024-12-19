# -*- coding: utf-8 -*-
# https://check.rs/

import requests
import re
from bs4 import BeautifulSoup

def get_cy_id(req, headers, domain, domain_type):
    query_domain = ''
    if domain and domain_type:
        query_domain = domain.replace('.{0}'.format(domain_type), '')
    payload = {
        'domainEndingName': domain_type,
        'domainName': query_domain
    }
    
    result = {
    }
    req_post = False
    try:
        req_post = req.post('https://registry.nic.cy/api/domains/_search', json=payload, headers=headers, verify=False)
    except:
        pass
    
    if req_post and req_post.status_code == 200 and req_post.json():
        arr_json_data = req_post.json()
        if arr_json_data:
            json_data = arr_json_data[0]
            if json_data.get('id', False):
                result.update({
                    'domain_id': json_data.get('id')
                })
            if json_data.get('status', False):
                result.update({
                    'domain_status': json_data.get('status')
                })
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
    
    cy_id_data = get_cy_id(req, headers, domain, domain_type)
    if cy_id_data:
        req_get = False
        try:
            req_get = req.get('https://www.nic.cy/api/whoIs/{0}'.format(cy_id_data['domain_id']), headers=headers, verify=False)
        except:
            pass
        
        result = []
        if req_get and req_get.status_code == 200 and req_get.text:
            json_data = req_get.json()
            if json_data:
                if json_data.get('domainWhoIs', False):
                    if json_data['domainWhoIs'].get('domainFullname', False):
                        result.append('Domain Name: {0}'.format(json_data['domainWhoIs']['domainFullname']))
                    if json_data['domainWhoIs'].get('domainExpirationDate', False):
                        result.append('Registry Expiry Date: {0}'.format(json_data['domainWhoIs']['domainExpirationDate']))
                    for ns_server in json_data['domainWhoIs'].get('domainServers', []):
                        if ns_server.get('name', False):
                            result.append('Name Server: {0}'.format(ns_server.get('name')))
                    
                    if cy_id_data.get('domain_status', False):
                        result.append('Domain Status: {0} {1}'.format(cy_id_data.get('domain_status'), 'https://icann.org/epp'))
        
        if result:
            result.append('\nFull WHOIS: https://www.nic.cy')
            final_result = {
                'status': True,
                'result': '\n'.join(result)
            }
    
    return final_result