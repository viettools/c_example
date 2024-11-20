# -*- coding: utf-8 -*-
# https://check.rs/

import unittest
from fastapi.testclient import TestClient
import sys, os, json

sys.path.append(os.path.dirname(os.path.normpath(os.path.dirname(os.path.abspath(__file__)))))

from main import app
client = TestClient(app)

class TestPQ(unittest.TestCase):

    def test_PE(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.pe"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .pe whois server!')
            return

        self.assertEqual(data['parse']['registrar'],'MarkMonitor Inc.')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '')
        self.assertEqual(len(data['parse']['updated_date']), 0)
        self.assertEqual(len(data['parse']['expiry_date']), 0)

    def test_PK(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.pk"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .pk whois server!')
            return

        self.assertEqual(data['parse']['registrar'], '')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2005-12-01')
        self.assertEqual(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
    
    def test_PL(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.pl"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .pl whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'Markmonitor, Inc.')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2002.09.19 13:00:00')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertEqual(len(data['parse']['expiry_date']), 0)

    def test_PM(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.pm"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .pm whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'MARKMONITOR Inc.')
        self.assertEqual(data['parse']['registrar_url'], 'http://www.markmonitor.com')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2011-12-06T09:12:15Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
    
    def test_PR(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.pr"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .pr whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'MarkMonitor Inc.')
        self.assertEqual(data['parse']['registrar_url'], 'http://www.markmonitor.com')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2005-09-15T16:10:10Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
        
    def test_PS(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.ps"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .ps whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'MarkMonitor Inc.')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2004-05-18T22:00:00.0Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
        
    def test_PT(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.pt"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .pt whois server!')
            return

        self.assertEqual(data['parse']['registrar'], '')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '09/01/2003 00:00:00')
        self.assertEqual(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
        
    def test_PW(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.pw"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .pw whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'MarkMonitor, Inc.')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertEqual(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '2012-10-12T10:19:46.0Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
    
    def test_QA(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.qa"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .qa whois server!')
            return

        self.assertEqual(data['parse']['registrar'], 'ROUTEDGE')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)

        self.assertEqual(data['parse']['creation_date'], '')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertEqual(len(data['parse']['expiry_date']), 0)
    
if __name__ == '__main__':
    unittest.main()