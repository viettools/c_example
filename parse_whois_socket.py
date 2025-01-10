# -*- coding: utf-8 -*-
# https://check.rs/

import re, html

class ParseWhoisSocket:
    
    def __init__(self, extension_name, regex_data, special_regex_data):
        self.extension_name = extension_name
        self.regex_data = regex_data
        self.special_regex_data = special_regex_data
    
    def _get_query_regex_option(self, item_option, regex_query, raw_data):
        if not item_option or not regex_query or not raw_data or not self:
            return False
        
        result = False
        regex_option = {}
        arr_regex_option = self.special_regex_data.get(self.extension_name, {})
        for item_regex_option in arr_regex_option:
            if item_regex_option.get('option', False) == item_option:
                regex_option = item_regex_option
                break
        
        if not regex_option or (regex_option and \
                                    not regex_option.get('dotall', False) and \
                                        not regex_option.get('ignore_case', False)):
            if regex_option.get('option', False) in ['domain_status', 'nameservers']:
                result = re.findall(regex_query, raw_data, re.IGNORECASE)
            else:
                result = re.findall(regex_query, raw_data, re.DOTALL | re.IGNORECASE)
        else:
            if regex_option.get('dotall', False) and not regex_option.get('ignore_case', False):
                result = re.findall(regex_query, raw_data, re.DOTALL)
            elif not regex_option.get('dotall', False) and regex_option.get('ignore_case', False):
                result = re.findall(regex_query, raw_data, re.IGNORECASE)
            else:
                result = re.findall(regex_query, raw_data, re.DOTALL | re.IGNORECASE)
            
        return result

    def _parse_data(self, raw_data):
        def spl_new_line(raw_regex_data):
            result = []
            for item in raw_regex_data:
                arr_spl = item.split('\n')
                if arr_spl:
                    result.extend(arr_spl)
            return result
        
        def remove_redundancy(raw_data):
            result = False
            if raw_data:
                result = raw_data.strip()
                result = re.sub('\n|\r', '', result)
            return result
        
        def filter_domain_status(arr_status):
            result = []
            if not arr_status:
                return result
            
            epp_status_codes = ['addPeriod', 'autoRenewPeriod', 'inactive', 'ok',
                                'pendingCreate', 'pendingDelete', 'pendingRenew',
                                'pendingRestore', 'pendingTransfer', 'pendingUpdate',
                                'redemptionPeriod', 'renewPeriod', 'serverDeleteProhibited',
                                'serverHold', 'serverRenewProhibited', 'serverTransferProhibited',
                                'serverUpdateProhibited', 'transferPeriod', 'clientDeleteProhibited',
                                'clientHold', 'clientRenewProhibited', 'clientTransferProhibited',
                                'clientUpdateProhibited']
            for item in arr_status:
                # .fr, .tf, .wf, .yt, .pm, .re or .mg
                if item == 'associated' or item.find('No Object Found') > -1:
                    continue
                
                # 'serverUpdateProhibited (Secured by CoCCA Premium Registry Lock)' --> serverUpdateProhibited
                check = [epp for epp in epp_status_codes if item.find(epp) > -1]
                if check:
                    result.append(check[0])
                else:
                    result.append(item)
            # Remove duplicate
            if result:
                result = list(set(result))
            return result
        
        def allow_c_array(c):
            if (ord(c) >= 97 and ord(c) <= 122) or \
                    (ord(c) >= 65 and ord(c) <= 90) or \
                        (ord(c) >= 48 and ord(c) <= 57) or \
                            ord(c) in [45, 46]:
                return c
            return False
        
        def filter_nserver(arr_nserver):
            result = []
            if not arr_nserver:
                return result
            for item in arr_nserver:
                arr_char = [c for c in item if allow_c_array(c)]
                if arr_char:
                    result.append(''.join(arr_char))
            return result
        
        def filter_nserver_opening_parenthesis(arr_nserver):
            result = []
            if not arr_nserver:
                return result
            for item in arr_nserver:
                if item.find('(') > -1:
                    result.append(item[:item.find('(')])
                else:
                    result.append(item)
            return result
        
        def check_reserved_domain(extension_name, whois_data):
            result = False
            if extension_name in ['ac', 'bm', 'bz'] and whois_data.find('This name is reserved by the Registry') > -1:
                result = True
            elif extension_name == 'rs' and whois_data.find('This domain is reserved') > -1:
                result = True
            elif extension_name == 'au' and (whois_data.find('Reserved by Registry') > -1 or whois_data.find('This domain name is on Priority Hold status') > -1):
                result = True
            elif extension_name in ['bj', 'cm', 'cx', 'cv', 'rw', 'ss', 'ng', 'nf', 'do', 'gy', 'hn',
                                    'ke', 'ki', 'kw', 'ms', 'ma', 'ly', 'kn', 'sb', 'tl'] and \
                    whois_data.find('Prohibited String - Domain Cannot Be Registered') > -1:
                result = True
            elif extension_name in ['mg', 'pe'] and whois_data.find('Prohibited String - Object Cannot Be Registered') > -1:
                result = True
            elif extension_name in ['ca', 'sg', 'nz'] and whois_data.find('The domain name requested has usage restrictions applied to it') > -1:
                result = True
            elif extension_name == 'cn' and whois_data.find('you apply can not be registered online') > -1:
                result = True
            elif extension_name == 'qa' and whois_data.find('The Domain Name is not Available') > -1:
                result = True
            elif extension_name == 'by' and whois_data.find('object is blocked') > -1:
                result = True
            elif extension_name == 'ae' and whois_data.find('has been reserved by aeDA Regulator') > -1:
                result = True
            elif extension_name == 'am' and whois_data.find('Reserved name: Temporarily reserved') > -1:
                result = True
            elif extension_name == 'be' and whois_data.find('Status:	NOT ALLOWED') > -1:
                result = True
            elif extension_name == 'bg' and whois_data.find('registration status: forbidden') > -1:
                result = True
            elif extension_name == 'bi' and whois_data.find('This string is on a restricted list, if registered, it will require approval') > -1:
                result = True
            elif extension_name == 'br' and whois_data.find('% reserved') > -1:
                result = True
            elif extension_name == 'om' and whois_data.find('Reserved Domain Name') > -1:
                result = True
            elif extension_name == 'dm' and whois_data.find('This domain is not available') > -1:
                result = True
            elif extension_name == 'kr' and whois_data.find('This request domain name is restricted') > -1:
                result = True
            elif extension_name == 'my' and whois_data.find('This name is not available for registration') > -1:
                result = True
            elif extension_name == 'tw' and whois_data.find('reserved name') > -1:
                result = True
            
            return result
        
        vals = {}
        if not raw_data:
            return vals
        
        arr = ['registrar', 'registrar_url', 'domain_status',
                'nameservers', 'creation_date', 'updated_date', 'expiry_date']
        
        for item in arr:
            # Reserved Domain
            if item == 'domain_status':
                is_reserved = check_reserved_domain(self.extension_name, raw_data)
                if is_reserved:
                    vals.update({'domain_status': 'Reserved Domain'})
                    continue
            # End 'Reserved Domain'
            
            dict_regex_query = self.regex_data.get(self.extension_name, {})
            if not dict_regex_query:
                dict_regex_query = self.regex_data['iana']
            
            regex_query = dict_regex_query.get(item, False)
            if regex_query:
                regex_data = self._get_query_regex_option(item, regex_query, raw_data)
                
                if regex_data:
                    # Special Case
                    if self.extension_name in ['am', 'aw',
                                            'be', 'bg', 'bn',
                                            'cz', 'eu', 'hk',
                                            'it', 'kg', 'ls',
                                            'mo', 'nl', 'pl',
                                            'sa', 'sg', 'sm',
                                            'tr', 'tw', 'uk',
                                            'uz', 'ac.uk', 'gov.uk',
                                            'co.uz', 'com.uz', 'net.uz', 'org.uz']:
                        if item == 'nameservers':
                            regex_data = spl_new_line(regex_data)
                            '''
                                .kg
                                    NS1.GOOGLE.COM 216.239.32.10
                                .co.uz
                                    Name Server: ns2.google.com. 216.239.34.10 
                                    Name Server: not defined. not defined. 
                            '''
                            if self.extension_name in ['kg', 'co.uz', 'com.uz', 'net.uz', 'org.uz']:
                                ns_ip_regex_data = []
                                for item_ns_ip in regex_data:
                                    item_ns_ip = item_ns_ip.strip()
                                    if item_ns_ip.find('not defined') > -1:
                                        continue
                                    
                                    spl_ns_ip = item_ns_ip.split(' ')
                                    if spl_ns_ip:
                                        ns_ip_regex_data.append(spl_ns_ip[0])
                                if ns_ip_regex_data:
                                    regex_data = list(ns_ip_regex_data)
                                    del ns_ip_regex_data
                                
                        # Special .bn
                        if regex_data and self.extension_name in ['bn', 'cz', 'ls']:
                            regex_data = filter_nserver_opening_parenthesis(regex_data)
                    if self.extension_name in ['as', 'gg', 'je', 'kz']:
                        if item in ['nameservers', 'domain_status']:
                            regex_data = spl_new_line(regex_data)
                    if self.extension_name == 'im' and item == 'nameservers':
                        # Filter 'ns1.google.com.' or 'ns1.google.com.\r' to 'ns1.google.com'
                        regex_data_im = []
                        for item_ns_im in regex_data:
                            if item_ns_im:
                                if item_ns_im.endswith('.\r'):
                                    item_ns_im = item_ns_im[:-2]
                                elif item_ns_im.endswith('.'):
                                    item_ns_im = item_ns_im[:-1]
                                
                                regex_data_im.append(item_ns_im)
                        if regex_data_im:
                            regex_data = list(regex_data_im)
                            del regex_data_im
                    # ['clientTransferProhibited, clientUpdateProhibited, clientDeleteProhibited']
                    if self.extension_name in ['am', 'bg', 'ru', 'sg', 'si',
                                            'sk', 'st', 'su', 'tw', 'md',
                                            'net.ru', 'org.ru', 'pp.ru'] \
                            and item == 'domain_status':
                        arr_status_one_line = []
                        for item_ds in regex_data:
                            if item_ds.find(',') > -1:
                                arr_status_one_line.extend(item_ds.split(','))
                            else:
                                arr_status_one_line.append(item_ds)
                        if arr_status_one_line:
                            regex_data = list(arr_status_one_line)
                            del arr_status_one_line
                    # Decode France Status
                    if self.extension_name == 'tg':
                        arr_status_one_line = []
                        for item_st in regex_data:
                            arr_status_one_line.append(html.unescape(item_st))
                        if arr_status_one_line:
                            regex_data = list(set(arr_status_one_line))
                    # Multi Regex
                    if self.extension_name == 'tn':
                        if item == 'nameservers':
                            raw_ns_tn_data = regex_data[0]
                            if raw_ns_tn_data:
                                raw_ns_tn_data += '\n'
                            
                            regex_ns_tn = re.findall("Name\.{2,}:(.*?)\n", raw_ns_tn_data, re.DOTALL | re.IGNORECASE)
                            arr_ns_data = []
                            for item_ns_tn in regex_ns_tn:
                                if item_ns_tn.endswith('.'):
                                    item_ns_tn = item_ns_tn[:-1]
                                item_ns_tn = item_ns_tn.replace(' ', '')
                                arr_ns_data.append(item_ns_tn)
                            if arr_ns_data:
                                regex_data = list(set(arr_ns_data))
                            del arr_ns_data
                        elif item in ['creation_date', 'updated_date', 'expiry_date']:
                            arr_dt_data = []
                            for item_dt_tn in regex_data:
                                item_dt_tn = item_dt_tn.strip() if item_dt_tn else False
                                if item_dt_tn and item_dt_tn.find('GMT') > -1:
                                    item_dt_tn = item_dt_tn[:item_dt_tn.find('GMT')]
                                    arr_dt_data.append(item_dt_tn)
                            if arr_dt_data:
                                regex_data = list(arr_dt_data)
                    
                    if self.extension_name == 'cl' and item in ['creation_date', 'updated_date', 'expiry_date']:
                        arr_rep = []
                        for item_date in regex_data:
                            item_date = item_date.replace('CLST', '')
                            arr_rep.append(item_date)
                        if arr_rep:
                            regex_data = list(arr_rep)
                            
                    if self.extension_name == 'se' and item == 'nameservers':
                        arr_rep = []
                        for item_ns_se in regex_data:
                            item_ns_se = item_ns_se.strip()
                            if item_ns_se.find(' ') > -1:
                                spl_item_ns_se = item_ns_se.split(' ')
                                if spl_item_ns_se:
                                    arr_rep.append(spl_item_ns_se[0])
                            else:
                                arr_rep.append(item_ns_se)
                        if arr_rep:
                            regex_data = list(arr_rep)
                    
                    if item in ['domain_status', 'nameservers']:
                        arr_ns = [remove_redundancy(rr_item) for rr_item in regex_data if rr_item and remove_redundancy(rr_item)]
                        if arr_ns:
                            if item == 'domain_status':
                                arr_ns = filter_domain_status(arr_ns)
                            else:
                                arr_ns = filter_nserver(arr_ns)
                                # 'ns1.google.com.' --> 'ns1.google.com'
                                arr_ns = [item[:-1] if item.endswith('.') else item for item in arr_ns]
                        vals.update({item: '\n'.join(arr_ns) if arr_ns else False})
                    else:
                        vals.update({item: remove_redundancy(regex_data[0])})
        
        return vals
    
    def parse_socket_data(self, raw_data):
        result = {
            'registrar': '',
            'registrar_url': '',
            'domain_status': [],
            'nameservers': [],
            'creation_date': '',
            'updated_date': '',
            'expiry_date': '',
        }
        if raw_data:
            pre_data = self._parse_data(raw_data)
            if pre_data.get('nameservers', False):
                nameservers = pre_data['nameservers'].split('\n')
                pre_data['nameservers'] = nameservers
            else:
                pre_data['nameservers'] = []
            
            if pre_data.get('domain_status', False):
                domain_status = pre_data['domain_status'].split('\n')
                pre_data['domain_status'] = domain_status
            else:
                pre_data['domain_status'] = []
            
            if pre_data:
                result.update(pre_data)
            # print(result) # Check Result
        return result