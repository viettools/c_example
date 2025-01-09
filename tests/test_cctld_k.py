# -*- coding: utf-8 -*-
# https://check.rs/

import unittest
from fastapi.testclient import TestClient
import sys, os, json

sys.path.append(os.path.dirname(os.path.normpath(os.path.dirname(os.path.abspath(__file__)))))

from main import app
client = TestClient(app)

class TestK(unittest.TestCase):
    def test_KE(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.ke"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .ke whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'Afriregister Limited')
        self.assertEqual(data['parse']['registrar_url'], 'null')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2018-01-10T11:43:08Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
        
    def test_KG(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.kg"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .kg whois server!')
            return

        self.assertEqual(data['parse']['registrar'], '')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], 'Tue Feb 10 09:42:42 2004')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
        
    def test_KI(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.ki"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .ki whois server!')
            return

        # whois_result = data.get('result', '')
        # self.assertEqual(whois_result.find('Domain: https://rdap.coccaregistry.org'), 0)
        
        self.assertEqual(data['parse']['registrar'], 'MarkMonitor')
        self.assertEqual(data['parse']['registrar_url'], 'http://www.markmonitor.com')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2006-05-15T12:00:00Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
    
    def test_KN(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.kn"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .kn whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'MarkMonitor Inc.')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2011-04-04T04:00:00Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
        
    def test_KR(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.kr"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .ac whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'Whois Corp.(http://whois.co.kr)')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2007. 03. 02.')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
        
    def test_KW(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.com.kw"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .kw whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'Solutions by STC')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2007-03-17T00:00:00.0Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
        
    def test_KY(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.ky"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .ky whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'Uniregistrar Corp')
        self.assertEqual(data['parse']['registrar_url'], 'uniregistrar.com')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2015-03-03T15:19:12.167Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
        
    def test_KZ(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.kz"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .kz whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'KAZNIC')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '1999-06-07 14:01:43')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertEqual(len(data['parse']['expiry_date']), 0)
        
    '''
        Test Reserved Domains
    '''
    
    def test_reserved_domain_ke(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "iana.ke"},
        )
        data = json.loads(response.content)
        
        if not data['status']:
            print('Please check .ke whois server - Reserved Domains!')
            return
        
        self.assertEqual(data['parse']['registrar'], '')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 1)
        self.assertEqual(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '')
        self.assertEqual(data['parse']['updated_date'], '')
        self.assertEqual(data['parse']['expiry_date'], '')
        
        self.assertEqual(data['parse']['domain_status'][0], 'Reserved Domain')
        
    def test_reserved_domain_ki(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "fuck.ki"},
        )
        data = json.loads(response.content)
        
        if not data['status']:
            print('Please check .ki whois server - Reserved Domains!')
            return
        
        self.assertEqual(data['parse']['registrar'], '')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 1)
        self.assertEqual(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '')
        self.assertEqual(data['parse']['updated_date'], '')
        self.assertEqual(data['parse']['expiry_date'], '')
        
        self.assertEqual(data['parse']['domain_status'][0], 'Reserved Domain')
        
    def test_reserved_domain_kn(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "fuck.kn"},
        )
        data = json.loads(response.content)
        
        if not data['status']:
            print('Please check .kn whois server - Reserved Domains!')
            return
        
        self.assertEqual(data['parse']['registrar'], '')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 1)
        self.assertEqual(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '')
        self.assertEqual(data['parse']['updated_date'], '')
        self.assertEqual(data['parse']['expiry_date'], '')
        
        self.assertEqual(data['parse']['domain_status'][0], 'Reserved Domain')
        
    def test_reserved_domain_kr(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "xxx.kr"},
        )
        data = json.loads(response.content)
        
        if not data['status']:
            print('Please check .kr whois server - Reserved Domains!')
            return
        
        self.assertEqual(data['parse']['registrar'], '')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 1)
        self.assertEqual(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '')
        self.assertEqual(data['parse']['updated_date'], '')
        self.assertEqual(data['parse']['expiry_date'], '')
        
        self.assertEqual(data['parse']['domain_status'][0], 'Reserved Domain')
        
    def test_reserved_domain_kw(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "xxx.kw"},
        )
        data = json.loads(response.content)
        
        if not data['status']:
            print('Please check .kw whois server - Reserved Domains!')
            return
        
        self.assertEqual(data['parse']['registrar'], '')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 1)
        self.assertEqual(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '')
        self.assertEqual(data['parse']['updated_date'], '')
        self.assertEqual(data['parse']['expiry_date'], '')
        
        self.assertEqual(data['parse']['domain_status'][0], 'Reserved Domain')
        
if __name__ == '__main__':
    unittest.main()