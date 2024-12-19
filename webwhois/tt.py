# -*- coding: utf-8 -*-
# https://check.rs/

import requests
import re, json
from bs4 import BeautifulSoup

def pre_raw_data(regex_group, extend_header_html=None, extend_footer_html=None):
    result = False
    if regex_group:
        result = regex_group.group(1)
        result = result.replace('\xa0', '')
        if extend_header_html:
            result = extend_header_html + result
        if extend_footer_html:
            result = result + extend_footer_html
    return result

def parse_tt_data(regex_group, extend_header_html=None, extend_footer_html=None):
    result = False
    pre_clean_data = pre_raw_data(regex_group, extend_header_html, extend_footer_html)
    if pre_clean_data:
        clean_data = BeautifulSoup(pre_clean_data, features='html.parser').get_text()
        if clean_data:
            result = clean_data.strip()
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
    post_data = {
        'name': (None, domain), 
        'Search': (None, 'Search')
    }
    
    req_cookie = req.cookies.get_dict()
    headers.update({
        'Referer': 'https://www.nic.tt/cgi-bin/search.pl',
        'Origin': 'https://www.nic.tt'
    })

    req_post = False
    try:
        req_post = requests.post('https://nic.tt/cgi-bin/search.pl', files=post_data, headers=headers, cookies=req_cookie, verify=False)
    except:
        pass
    
    result = []
    if req_post and req_post.status_code == 200 and req_post.text:
        raw_data = req_post.text
        if raw_data:
            creation_date_details = parse_tt_data(re.search('Registration Date(.*?)Expiration Date', raw_data, re.DOTALL|re.M))
            expiration_date_details = parse_tt_data(re.search('Expiration Date(.*?)<font', raw_data, re.DOTALL|re.M))
            ns_details = parse_tt_data(re.search('DNS Hostnames(.*?)DNS IP Addresses', raw_data, re.DOTALL|re.M))
            status_details = parse_tt_data(re.search('<font color=(.+)>(.*?)Administrative Contact', raw_data, re.DOTALL|re.M), '<font color=', '>')

            if creation_date_details:
                result.append('Creation Date: {0}'.format(creation_date_details))
            if expiration_date_details:
                result.append('Registry Expiry Date: {0}'.format(expiration_date_details))
            if status_details:
                result.append('Domain Status: {0} https://icann.org/epp'.format(status_details))
            if ns_details:
                spl_ns = ns_details.split(',')
                for ns in spl_ns:
                    result.append('Name Server: {0}'.format(ns.strip()))
    if result:
        result.append('Full WHOIS: https://nic.tt/cgi-bin/search.pl')
        final_result = {
            'status': True,
            'result': '\n'.join(result)
        }
    
    return final_result