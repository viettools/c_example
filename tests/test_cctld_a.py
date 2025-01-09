# -*- coding: utf-8 -*-
# https://check.rs/

import unittest
from fastapi.testclient import TestClient
import sys, os, json

sys.path.append(os.path.dirname(os.path.normpath(os.path.dirname(os.path.abspath(__file__)))))

from main import app
client = TestClient(app)

class TestA(unittest.TestCase):
    def test_google_ac(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.ac"},
        )
        data = json.loads(response.content)
        
        if not data['status']:
            print('Please check .ac whois server!')
            return
        
        self.assertEqual(data['parse']['registrar'], 'MarkMonitor Inc.')
        self.assertEqual(data['parse']['registrar_url'], 'http://www.markmonitor.com')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '2006-04-03T13:38:02Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
        
    def test_google_ad(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.ad"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .ad whois server!')
            return
        
        self.assertEqual(data['parse']['registrar'], 'SAPIM, SLU')
        self.assertEqual(data['parse']['registrar_url'], 'https://www.sapim.com/')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '2006-12-06T12:00:00.0Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
        
    def test_google_ae(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.ae"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .ae whois server!')
            return
        
        self.assertEqual(data['parse']['registrar'], 'MarkMonitor')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '')
        self.assertEqual(len(data['parse']['updated_date']), 0)
        self.assertEqual(len(data['parse']['expiry_date']), 0)
        
    def test_google_af(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.af"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('[+] -----> .AF: Please check .af whois server!')
            return
        
        # whois_result = data.get('result', '')
        # self.assertEqual(whois_result.find('Domain: https://rdap.coccaregistry.org'), 0)

        self.assertEqual(data['parse']['registrar'], 'MarkMonitor')
        self.assertEqual(data['parse']['registrar_url'], 'http://www.markmonitor.com')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '2009-10-05T03:51:17Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
    
    def test_google_ag(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.ag"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .ag whois server!')
            return
        
        self.assertEqual(data['parse']['registrar'], 'MarkMonitor Inc.')
        self.assertEqual(data['parse']['registrar_url'], 'http://www.markmonitor.com')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '2003-01-05T14:06:59Z')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
    
    def test_google_ai(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.ai"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('[+] -----> .AI: Please check .ai whois server!')
            return
        
        self.assertEqual(data['parse']['registrar'], 'Markmonitor')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '')
        self.assertEqual(len(data['parse']['updated_date']), 0)
        self.assertEqual(len(data['parse']['expiry_date']), 0)
        
    def test_google_am(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.am"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .am whois server!')
            return
        
        self.assertEqual(data['parse']['registrar'], 'abcdomain (ABCDomain LLC)')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '1999-06-05')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
        
    def test_google_ar(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.ar"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .ar whois server!')
            return
        
        self.assertEqual(data['parse']['registrar'], 'nicar')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '2019-11-01 12:21:37.677445')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
        
    def test_google_as(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.as"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .as whois server!')
            return
        
        self.assertEqual(data['parse']['registrar'], 'MarkMonitor Inc. (http://www.markmonitor.com)')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '02nd August 2000 at 00:00:00.000')
        self.assertEqual(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
        
    def test_google_at(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.at"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .at whois server!')
            return
        
        self.assertEqual(data['parse']['registrar'], 'MarkMonitor Inc. ( https://nic.at/registrar/434 )')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertEqual(len(data['parse']['expiry_date']), 0)
        
    def test_google_au(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.au"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .au whois server!')
            return
        
        self.assertEqual(data['parse']['registrar'], 'MarkMonitor Corporate Services Inc')
        self.assertEqual(data['parse']['registrar_url'], 'https://whois-webform.markmonitor.com/whois/')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertEqual(len(data['parse']['expiry_date']), 0)
        
    def test_google_aw(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "google.aw"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .aw whois server!')
            return
        
        self.assertEqual(data['parse']['registrar'], 'SETAR N.V.')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '2017-09-13')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertEqual(len(data['parse']['expiry_date']), 0)
    
    def test_whois_ax(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "whois.ax"},
        )
        data = json.loads(response.content)
        if not data['status']:
            print('Please check .ax whois server!')
            return
        
        self.assertEqual(data['parse']['registrar'], 'Ålands landskapsregering')
        self.assertEqual(data['parse']['registrar_url'], 'https://regeringen.ax')
        self.assertGreater(len(data['parse']['domain_status']), 0)
        self.assertGreater(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '02.02.2012')
        self.assertGreater(len(data['parse']['updated_date']), 0)
        self.assertGreater(len(data['parse']['expiry_date']), 0)
        
    '''
        Test Reserved Domains
    '''
    
    def test_reserved_domain_ac(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "xxx.ac"},
        )
        data = json.loads(response.content)
        
        if not data['status']:
            print('Please check .ac whois server - Reserved Domains!')
            return
        
        self.assertEqual(data['parse']['registrar'], '')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 1)
        self.assertEqual(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '')
        self.assertEqual(data['parse']['updated_date'], '')
        self.assertEqual(data['parse']['expiry_date'], '')
        
        self.assertEqual(data['parse']['domain_status'][0], 'Reserved Domain')
        
    def test_reserved_domain_ae(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "xxx.ae"},
        )
        data = json.loads(response.content)
        
        if not data['status']:
            print('Please check .ae whois server - Reserved Domains!')
            return
        
        self.assertEqual(data['parse']['registrar'], '')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 1)
        self.assertEqual(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '')
        self.assertEqual(data['parse']['updated_date'], '')
        self.assertEqual(data['parse']['expiry_date'], '')
        
        self.assertEqual(data['parse']['domain_status'][0], 'Reserved Domain')
        
    def test_reserved_domain_am(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "fuck.am"},
        )
        data = json.loads(response.content)
        
        if not data['status']:
            print('Please check .am whois server - Reserved Domains!')
            return
        
        self.assertEqual(data['parse']['registrar'], '')
        self.assertEqual(data['parse']['registrar_url'], '')
        self.assertEqual(len(data['parse']['domain_status']), 1)
        self.assertEqual(len(data['parse']['nameservers']), 0)
        
        self.assertEqual(data['parse']['creation_date'], '')
        self.assertEqual(data['parse']['updated_date'], '')
        self.assertEqual(data['parse']['expiry_date'], '')
        
        self.assertEqual(data['parse']['domain_status'][0], 'Reserved Domain')
        
    def test_reserved_domain_au(self):
        response = client.post(
            '/api/v1/whois',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            json={"domain": "mail.au"},
        )
        data = json.loads(response.content)
        
        if not data['status']:
            print('Please check .au whois server - Reserved Domains!')
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