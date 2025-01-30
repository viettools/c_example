# -*- coding: utf-8 -*-
# https://check.rs/

from whois import Whois
from cctld import WhOISccTLD
from parse_whois_socket import ParseWhoisSocket
from verified.registrar import VerifiedRegistrar

from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from bs4 import BeautifulSoup
from tld import get_tld
import re, os, requests, json, time, pathlib, sys, configparser, csv

app = FastAPI(docs_url=None, redoc_url=None) # Remove 'docs_url=None, redoc_url=None' to check api

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])

current_path_dir = os.path.dirname(os.path.abspath(__file__))

app.mount('/static', StaticFiles(directory='{0}/static/src'.format(current_path_dir)), name='static')
templates = Jinja2Templates('{0}/templates'.format(current_path_dir))

#region Copy code from module 'domain_management' - Odoo17

def load_special_regex_data():
    result = {}
    path_csv = '{0}/data/domains.query.regex.csv'.format(current_path_dir)
    with open(path_csv) as csv_file:
        heading = next(csv_file)
        csv_obj = csv.reader(csv_file)
        for row in csv_obj:
            if row:
                domain_type = row[1]
                if not domain_type:
                    continue
                
                arr_replace = [['domain_management.domain_name_', ''], ['_whois', ''], ['_', '.']]
                for item_rep in arr_replace:
                    domain_type = domain_type.replace(item_rep[0], item_rep[1])
                
                dict_data = {
                    'option': row[2],
                    'dotall': False if row[3] == '0' else True,
                    'ignore_case': False if row[4] == '0' else True
                }
                if domain_type in result:
                    result[domain_type].append(dict_data)
                else:
                    result.update({domain_type: [dict_data]})
        
    return result

def load_regex_data():
    result = {}
    
    path_csv = '{0}/data/domains.query.csv'.format(current_path_dir)
    with open(path_csv) as csv_file:
        heading = next(csv_file)
        csv_obj = csv.reader(csv_file)
        for row in csv_obj:
            if row and row[2] == 'whois':
                domain_type = row[1]
                if not domain_type:
                    continue
                
                domain_type = domain_type.replace('domain_name_', '')
                domain_type = domain_type.replace('_', '.')
                
                whois_dict = {
                    'server': row[3],
                    'registrar': row[4] or False,
                    'registrar_url': row[5] or False,
                    'domain_status': row[6] or False,
                    'nameservers': row[7] or False,
                    'creation_date': row[8] or False,
                    'updated_date': row[9] or False,
                    'expiry_date': row[10] or False
                }
                result.update({domain_type: whois_dict})
    
    return result

regex_data = load_regex_data()
special_regex_data = load_special_regex_data()

#endregion

@app.get('/', response_class=HTMLResponse)
def main(request: Request):
    dict_config = {
        'flagcounter': {
            'enable': False
        },
        'tidio': {
            'enable': False
        },
        'alert': {
            'enable': False
        }
    }
    
    config_path = '{0}/config/checkdomain.ini'.format(current_path_dir)
    if pathlib.Path(config_path).exists():
        config = configparser.ConfigParser()
        config.read(config_path)
        
        dict_config['flagcounter'].update({
            'enable': config.getboolean('flagcounter', 'enable'),
            'url': config.get('flagcounter', 'url'),
            'img': config.get('flagcounter', 'img'),
        })
        
        dict_config['tidio'].update({
            'enable': config.getboolean('tidio', 'enable'),
            'url': config.get('tidio', 'url'),
        })
        
        dict_config['alert'].update({
            'enable': config.getboolean('alert', 'enable'),
        })
    
    header_template = templates.TemplateResponse('header.html', {'request': request})
    footer_template = templates.TemplateResponse('footer.html', {'request': request, 'dict_config': dict_config})
    main_template = templates.TemplateResponse('index.html', 
												{
													'request': request,
                                                    'dict_config': dict_config,
													'header_template': header_template.body.decode('utf-8'),
													'footer_template': footer_template.body.decode('utf-8'),
												})
    return main_template

@app.post('/api/v1/whois')
def whois_data(domain: str = Body(..., embed=True)):
    result = {'status': False, 'result': False}
    parse_data = {
        'registrar': '',
        'registrar_url': '',
        'domain_status': [],
        'nameservers': [],
        'creation_date': '',
        'updated_date': '',
        'expiry_date': '',
        'verified': False
    }
    result.update({'parse': parse_data})
    
    if not domain:
        return result
    domain = BeautifulSoup(domain, features='html.parser').get_text()
    
    # Special TLD
    arr_special_tld = ['br.com', 'cn.com', 'de.com', 'eu.com', 'gb.net',
                       'gr.com', 'in.net', 'ru.com', 'sa.com', 'se.net',
                       'uk.com', 'uk.net', 'us.com', 'za.com', 'jpn.com',
                       'it.com', 'priv.at', 'co.ca', 'co.pl', 'ac.ru', 'com.ru',
                       'msk.ru', 'net.ru', 'nov.ru', 'org.ru', 'pp.ru', 'spb.ru',
                       'ac.uk', 'gov.uk', 'co.uz', 'com.uz', 'net.uz', 'org.uz',
                       'ac.za', 'co.za', 'net.za', 'org.za', 'web.za', 'gov.za']
    # Web WHOIS
    arr_web_tld = ['ao', 'az',
                   'ba', 'bb', 'bd', 'bt',
                   'cu', 'cv', 'cy',
                   'dz', 'dj',
                   'es', 'eg', 'ec',
                   'gm', 'gr', 'gt', 'gw',
                   'hm', 'lk', 'tj', 'jo',
                   'sv', 'np', 'tt', 'pa',
                   'ph', 'vi', 'vn']
    
    #google.com -> tld_domain = 'com'
    tld_domain = False
    try:
        tld_domain = get_tld(domain, fix_protocol=True)
    except:
        spl = domain.split('.')
        if spl:
            tld_domain = spl[-1]
    
    if not tld_domain:
        return result
    
    final_tld_domain = tld_domain
    # sub domain ? 'com.ps' --> 'ps'
    if tld_domain not in arr_special_tld and tld_domain.find('.') > -1:
        spl_tld_domain = tld_domain.split('.')
        if spl_tld_domain:
            final_tld_domain = spl_tld_domain[-1]
    
    whois_result = {}
    wcc = WhOISccTLD()
    
    if wcc.get_whois_server(final_tld_domain):
        whois_server = wcc.get_whois_server(final_tld_domain)
        # Socket
        if whois_server:
            whois_data = Whois(domain, final_tld_domain)
            whois_data.set_hostname(whois_server)
            whois_result = whois_data.get_data()
    elif final_tld_domain in arr_web_tld:
        USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'
        dynamic_import = __import__('webwhois.{0}'.format(final_tld_domain))
        if hasattr(dynamic_import, '{0}'.format(final_tld_domain)):
            whois_result = getattr(dynamic_import, '{0}'.format(final_tld_domain)).whois_via_web(USER_AGENT, domain, tld_domain)
        else:
            whois_result = {
                'status': False,
                'result': False
            }
        # I want to limit query via web
        time.sleep(6)
    else:
        whois_iana_data = Whois(domain, final_tld_domain)
        result_iana = whois_iana_data.get_data()
        
        if result_iana['result']:
            check = re.findall('whois:\s+(.+)', result_iana['result'], re.IGNORECASE)
            # .AD no whois server --> [status:       ACTIVE]
            if check and check[0] and check[0].find('status') == -1:
                next_query = check[0].strip()
                
                whois_data = Whois(domain, final_tld_domain)
                whois_data.set_hostname(next_query)
                whois_result = whois_data.get_data()
            else:
                # Only whois data from whois.iana.org
                whois_result.update({'status': True, 'result': result_iana['result']})
    
    if whois_result:
        result.update(whois_result)
        
        if whois_result.get('result', False):
            parse_obj = ParseWhoisSocket(final_tld_domain, regex_data, special_regex_data)
            verified_obj = VerifiedRegistrar()
            
            parse_raw = parse_obj.parse_socket_data(whois_result['result'])
            verified_data = verified_obj.check_registrar(whois_result['result'])
            
            parse_raw.update({'verified': verified_data})
            result.update({'parse': parse_raw})
    
    return result

@app.get('/api/v1/proxy/rdap')
def query_rdap_proxy(domain: str | None = None):
    # Bypass: Response body is not available to scripts (Reason: CORS Missing Allow Origin)
    result = {}
    if not domain:
        return result
    
    domain = BeautifulSoup(domain, features='html.parser').get_text()
    rdap_url = False

    spl_domain = domain.split('.')
    if spl_domain:
        if spl_domain[-1] == 'de':
            rdap_url = 'https://rdap.denic.de'
        elif spl_domain[-1] == 've':
            rdap_url = 'https://rdap.nic.ve/rdap'
        elif spl_domain[-1] == 'tz':
            rdap_url = 'https://whois.tznic.or.tz/rdap'
        elif spl_domain[-1] == 'uz':
            rdap_url = 'https://rdap.cctld.uz'
        elif spl_domain[-1] == 'kg':
            rdap_url = 'https://rdap.cctld.kg'
        elif spl_domain[-1] == 'ml':
            rdap_url = 'https://rdap.nic.ml'
        elif spl_domain[-1] == 'si':
            rdap_url = 'https://rdap.register.si'
        elif spl_domain[-1] == 'ye':
            rdap_url = 'https://rdap.y.net.ye'
        elif spl_domain[-1] == 'ch':
            rdap_url = 'https://rdap.nic.ch'
        elif spl_domain[-1] == 'li':
            rdap_url = 'https://rdap.nic.li'
    
    if rdap_url:
        req = requests.Session()
        req_get = False
        try:
            req_get = req.get('{0}/domain/{1}'.format(rdap_url, domain))
        except:
            pass

        if req_get and req_get.status_code == 200:
            result = json.loads(req_get.text)
    
    return result

def is_docker():
    if pathlib.Path('/.dockerenv').exists():
        return True
    path = '/proc/self/cgroup'
    if not os.path.isfile(path): return False
    with open(path) as f:
        for line in f:
            if re.match('\d+:[\w=]+:/docker(-[ce]e)?/\w+', line):
                return True
    return False

if __name__ == '__main__':
    assert (sys.version_info.major, sys.version_info.minor) == (3, 11), 'Run Python 3.11 bro!!!'
    listen_host = '0.0.0.0'
    if not is_docker():
        listen_host= '127.0.0.1'
    uvicorn.run('main:app', host=listen_host, port=6996, proxy_headers=True, forwarded_allow_ips='*', reload=True)