# -*- coding: utf-8 -*-
# https://check.rs/

import requests
import re, json
from bs4 import BeautifulSoup

def parse_sv_data(regex_input, raw_data):
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
        result = result.replace('\n', '')
        result = result.replace('\xa0\xa0', '\n')
    return result

def get_hidden_value(req, headers, domain):
    req_get = False
    try:
        req_get = req.get('https://svnet.sv', headers=headers, verify=False)
    except:
        pass
    
    result = {}
    if req_get and req_get.status_code == 200 and req_get.text:
        raw_data = req_get.text
        if raw_data:
            find_data_post_id = re.findall('<input type="hidden" id="ID" name="ID" value="(.*?)">', req_get.text, re.DOTALL|re.M)
            var_id = '1'
            if find_data_post_id:
                var_id = find_data_post_id[0]
            
            result = {
                'key': 'Buscar',
                'ID': find_data_post_id[0],
                'nombre': domain
            }
    return result

def get_dominios_registrados(req, headers, domain, domain_type, payload):
    req_post = False
    result = False
    try:
        req_post = req.post('https://svnet.sv/accion/procesos.php', data=payload, headers=headers)
    except:
        pass
    if req_post and req_post.status_code == 200 and req_post.text:
        raw_data = req_post.text
        if raw_data:
            registered_area = re.findall('Dominios Registrados(.*?)</div></div></div>', raw_data, re.DOTALL|re.M)
            if registered_area:
                registered_domain = re.findall('<div class="col-12">(.*?)</i>', registered_area[0], re.DOTALL|re.M)
                for item in registered_domain:
                    item_domain = BeautifulSoup(item, features='html.parser').get_text()
                    if item_domain:
                        item_domain = item_domain.strip()
                        if item_domain.find('{0}.{1}'.format(domain, domain_type)) == 0:
                            item_whois = re.search('onClick="Whois\((.*?)\)', item, re.DOTALL|re.M)
                            if item_whois:
                                result = item_whois.group(1)
                                break
    return result

def whois_via_web(USER_AGENT, domain, domain_type):
    if domain and domain_type:
        domain = domain.replace('.{0}'.format(domain_type), '')
    headers = {
        'User-Agent': USER_AGENT
    }
    
    final_result = {
        'status': False,
        'result': False
    }
    
    req = requests.Session()
    hidden_value = get_hidden_value(req, headers, domain)
    whois_id = False
    if hidden_value:
        whois_id = get_dominios_registrados(req, headers, domain, domain_type, hidden_value)
    
    if whois_id:
        req_post = False
        try:
            req_post = req.post('https://svnet.sv/accion/procesos.php', data={'key': 'Whois', 'ID': whois_id}, headers=headers)
        except:
            pass
    
        result = []
        if req_post and req_post.status_code == 200 and req_post.text:
            raw_data = req_post.text
            if raw_data:
                domain_status_details = parse_sv_data('Estado:(.*?)Contacto Administrativo:', raw_data)
                admin_name_details = parse_sv_data('Contacto Administrativo:(.*?)Correo Electrónico:', raw_data)
                email_details = parse_sv_data('Correo Electrónico:(.*?)Teléfono:', raw_data)
                phone_details = parse_sv_data('Teléfono:(.*?)Fecha Registro:', raw_data)
                creation_date_details = parse_sv_data('Fecha Registro:(.*?)Fecha de vencimiento:', raw_data)
                expiry_date_details = parse_sv_data('Fecha de Baja:(.*?)</table>', raw_data)
                if domain_status_details:
                    result.append('Domain Status: {0} https://icann.org/epp'.format(domain_status_details))
                if admin_name_details:
                    result.append('Admin Name: {0}'.format(admin_name_details))
                if email_details:
                    result.append('Admin Email: {0}'.format(email_details))
                if phone_details:
                    result.append('Admin Phone: {0}'.format(phone_details))
                if creation_date_details:
                    result.append('Creation Date: {0}'.format(creation_date_details))
                if expiry_date_details:
                    result.append('Registry Expiry Date: {0}'.format(expiry_date_details))
    if result:
        result.append('Full WHOIS: https://svnet.sv')
        final_result = {
            'status': True,
            'result': '\n'.join(result)
        }
    
    return final_result