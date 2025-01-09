# -*- coding: utf-8 -*-
# https://check.rs/

import unittest
from fastapi.testclient import TestClient
import sys, os, json

sys.path.append(os.path.dirname(os.path.normpath(os.path.dirname(os.path.abspath(__file__)))))

from main import app
client = TestClient(app)

class TestR(unittest.TestCase):
    def test_RE(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.re"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .re whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'MARKMONITOR Inc.')
        self.assertEqual(data['parse']['registrar_url'], 'http://www.markmonitor.com')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2008-11-19T09:40:52Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)

    def test_RO(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.ro"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .ro whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'MarkMonitor Inc.')
        self.assertEqual(data['parse']['registrar_url'], 'www.markmonitor.com')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2000-07-17')
        self.assertEqual(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
        
    def test_RS(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.rs"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .rs whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'Webglobe d.o.o.')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '10.03.2008 12:31:19')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)

    def test_RU(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.ru"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .ru whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'RU-CENTER-RU')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2004-03-03T21:00:00Z')
        self.assertEqual(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)

    def test_RW(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.rw"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .rw whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'MarkMonitor Inc.')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '1999-05-22T22:00:00Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
    
    '''
        Test Reserved Domains
    '''
    
    def test_reserved_domain_rs(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "iana.rs"},
        )
        data = json.loads(response.content)
        
        if not data['status']:
            print('Please check .rs whois server - Reserved Domains!')
            return
        
        self.assertEqual(data['parse']['registrar'], '')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 1)
        self.assertEqual(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '')
        self.assertEqual(data['parse']['updated_date'], '')
        self.assertEqual(data['parse']['expiry_date'], '')
        
        self.assertEqual(data['parse']['domain_status'][0], 'Reserved Domain')
        
    def test_reserved_domain_rw(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "fuck.rw"},
        )
        data = json.loads(response.content)
        
        if not data['status']:
            print('Please check .rw whois server - Reserved Domains!')
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