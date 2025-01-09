# -*- coding: utf-8 -*-
# https://check.rs/

import unittest
from fastapi.testclient import TestClient
import sys, os, json

sys.path.append(os.path.dirname(os.path.normpath(os.path.dirname(os.path.abspath(__file__)))))

from main import app
client = TestClient(app)

class TestG(unittest.TestCase):
    def test_GA(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.ga"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .ga whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'MARKMONITOR Inc.')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2023-06-06T19:15:12.718385Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)

    def test_GD(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.gd"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .gd whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'MarkMonitor, Inc.')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2006-12-11T00:00:00.0Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)

    def test_GE(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.ge"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .ge whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'proservice ltd')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2006-07-28')
        self.assertEqual(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)

    def test_GF(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.gf"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .gf whois server!')
            return

        self.assertEqual(data['parse']['registrar'], '')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertEqual(len(data['parse']['expiry_date']), 0)

    def test_GG(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.gg"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .gg whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'MarkMonitor Inc. (http://www.markmonitor.com)')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '30th April 2003 at 00:00:00.000')
        self.assertEqual(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)

    def test_GH(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.com.gh"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .gh whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'Ghana Dot Com')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2007-01-08T05:00:00.000Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)

    def test_GI(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "apple.gi"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .gi whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'GibNet Registrar')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2009-10-19T13:55:20Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)

    def test_GL(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.gl"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .gl whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'MarkMonitor, Inc.')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2003-03-11T03:00:00.0Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)

    def test_GN(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "ande.gov.gn"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .gn whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'Internal Registrars')
        self.assertEqual(data['parse']['registrar_url'], 'https://ande.gov.gn/dns-gn/')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2023-08-02T14:29:11Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)

    def test_GS(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.gs"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .gs whois server!')
            return
        
        # whois_result = data.get('result', '')
        # self.assertEqual(whois_result.find('Domain: https://rdap.coccaregistry.org'), 0)

        self.assertEqual(data['parse']['registrar'], 'MarkMonitor')
        self.assertEqual(data['parse']['registrar_url'], 'http://www.markmonitor.com')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2004-07-08T12:00:00Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)

    def test_GY(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.gy"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .gy whois server!')
            return
        
        # whois_result = data.get('result', '')
        # self.assertEqual(whois_result.find('Domain: https://rdap.coccaregistry.org'), 0)

        self.assertEqual(data['parse']['registrar'], 'MarkMonitor')
        self.assertEqual(data['parse']['registrar_url'], 'http://www.markmonitor.com')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2008-05-12T17:56:23Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
        
    '''
        Test Reserved Domains
    '''
    
    def test_reserved_domain_gy(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "whois.gy"},
        )
        data = json.loads(response.content)
        
        if not data['status']:
            print('Please check .gy whois server - Reserved Domains!')
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