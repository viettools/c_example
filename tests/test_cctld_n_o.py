# -*- coding: utf-8 -*-
# https://check.rs/

import unittest
from fastapi.testclient import TestClient
import sys, os, json

sys.path.append(os.path.dirname(os.path.normpath(os.path.dirname(os.path.abspath(__file__)))))

from main import app
client = TestClient(app)

class TestNO(unittest.TestCase):
    def test_NA(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.na"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .na whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'MarkMonitor Inc.')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2007-03-27T22:00:00.0Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
    
    def test_NC(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "whois.nc"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .nc whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'NONE')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2007-07-05T08:46:31.000Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
    
    def test_NF(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.nf"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .nf whois server!')
            return
        
        # whois_result = data.get('result', '')
        # self.assertEqual(whois_result.find('Domain: https://rdap.coccaregistry.org'), 0)

        self.assertEqual(data['parse']['registrar'], 'MarkMonitor')
        self.assertEqual(data['parse']['registrar_url'], 'http://www.markmonitor.com')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2005-11-27T11:00:00Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
    
    def test_NG(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.ng"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .ng whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'markmonitor')
        self.assertEqual(data['parse']['registrar_url'], 'http://www.markmonitor.com')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2011-01-19T13:24:01Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
        
    def test_NL(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.nl"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .nl whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'MarkMonitor Inc.')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '1999-05-27')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertEqual(len(data['parse']['expiry_date']), 0)

    def test_NO(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.no"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .no whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'REG466-NORID')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 0)
        self.assertEqual(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2001-02-26')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertEqual(len(data['parse']['expiry_date']), 0)

    def test_NU(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.nu"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .nu whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'MarkMonitor Inc')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '1999-06-07')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)

    def test_NZ(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "apple.nz"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .nz whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'Nom-IQ Ltd, dba Com Laude')
        self.assertEqual(data['parse']['registrar_url'], 'www.comlaude.com')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2017-10-31T11:37:27Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertEqual(len(data['parse']['expiry_date']), 0)

    def test_OM(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "apple.om"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .om whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'Abu Ghazaleh Intellectual Property (AGIP)')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '')
        self.assertEqual(len(data['parse']['updated_date']), 0)
        self.assertEqual(len(data['parse']['expiry_date']), 0)
    
    '''
        Test Reserved Domains
    '''
    
    def test_reserved_domain_nf(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "fuck.nf"},
        )
        data = json.loads(response.content)
        
        if not data['status']:
            print('Please check .nf whois server - Reserved Domains!')
            return
        
        self.assertEqual(data['parse']['registrar'], '')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 1)
        self.assertEqual(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '')
        self.assertEqual(data['parse']['updated_date'], '')
        self.assertEqual(data['parse']['expiry_date'], '')
        
        self.assertEqual(data['parse']['domain_status'][0], 'Reserved Domain')
        
    def test_reserved_domain_ng(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "xxx.ng"},
        )
        data = json.loads(response.content)
        
        if not data['status']:
            print('Please check .ng whois server - Reserved Domains!')
            return
        
        self.assertEqual(data['parse']['registrar'], '')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 1)
        self.assertEqual(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '')
        self.assertEqual(data['parse']['updated_date'], '')
        self.assertEqual(data['parse']['expiry_date'], '')
        
        self.assertEqual(data['parse']['domain_status'][0], 'Reserved Domain')
        
    def test_reserved_domain_nz(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "fuck.nz"},
        )
        data = json.loads(response.content)
        
        if not data['status']:
            print('Please check .nz whois server - Reserved Domains!')
            return
        
        self.assertEqual(data['parse']['registrar'], '')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 1)
        self.assertEqual(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '')
        self.assertEqual(data['parse']['updated_date'], '')
        self.assertEqual(data['parse']['expiry_date'], '')
        
        self.assertEqual(data['parse']['domain_status'][0], 'Reserved Domain')
        
    def test_reserved_domain_om(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "xxx.om"},
        )
        data = json.loads(response.content)
        
        if not data['status']:
            print('Please check .om whois server - Reserved Domains!')
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