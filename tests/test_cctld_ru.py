# -*- coding: utf-8 -*-
# https://check.rs/

import unittest
from fastapi.testclient import TestClient
import sys, os, json

sys.path.append(os.path.dirname(os.path.normpath(os.path.dirname(os.path.abspath(__file__)))))

from main import app
client = TestClient(app)

class TestRU(unittest.TestCase):
    def test_ac_ru(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "gpad.ac.ru"},
        )
        data = json.loads(response.content)
        
        if not data['status']:
            print('Please check .ac.ru whois server!')
            return
        
        self.assertEqual(data['parse']['registrar'], '')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], 'NO ACCESS')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertEqual(len(data['parse']['expiry_date']), 0)

    def test_com_ru(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.com.ru"},
        )
        data = json.loads(response.content)
        
        if not data['status']:
            print('Please check .com.ru whois server!')
            return
        
        self.assertEqual(data['parse']['registrar'], 'JSC "RU-CENTER"')
        self.assertEqual(data['parse']['registrar_url'], 'nic.ru')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '1999-06-28T15:19:49Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)

    def test_org_ru(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "mic.org.ru"},
        )
        data = json.loads(response.content)
        
        if not data['status']:
            print('Please check .org.ru whois server!')
            return
        
        self.assertEqual(data['parse']['registrar'], 'RU-CENTER-3LVL')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '2012-03-04T19:00:00Z')
        self.assertEqual(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
    
if __name__ == '__main__':
    unittest.main()