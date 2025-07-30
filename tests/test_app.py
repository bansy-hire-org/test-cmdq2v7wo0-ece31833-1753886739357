import unittest
import json
from src.app import app
import os
from unittest.mock import patch

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.credly_api_key = os.environ.get('CREDLY_API_KEY', 'dummy_key')

    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'status': 'OK'})

    def test_receive_workday_data_valid(self):
        mock_credly_response = unittest.mock.Mock()
        mock_credly_response.status_code = 200

        with patch('src.app.requests.post') as mock_post:
            mock_post.return_value = mock_credly_response
            data = {
                'employee_id': '123',
                'badge_name': 'Python Certification'
            }
            response = self.app.post('/workday', json=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.data), {'message': 'Badge issuance initiated'})

    def test_receive_workday_data_invalid(self):
        response = self.app.post('/workday', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {'error': 'Invalid Workday data'})

    def test_receive_workday_data_credly_api_error(self):
        with patch('src.app.requests.post') as mock_post:
             mock_post.side_effect = Exception('API Error')
             data = {
                 'employee_id': '123',
                 'badge_name': 'Python Certification'
             }
             response = self.app.post('/workday', json=data)
             self.assertEqual(response.status_code, 500)
             self.assertEqual(json.loads(response.data), {'error': 'Internal server error'})

    def test_transform_workday_to_credly(self):
      from src.app import transform_workday_to_credly
      workday_data = {
          'employee_id': '456',
          'badge_name': 'Java Expert'
      }
      credly_data = transform_workday_to_credly(workday_data)
      self.assertEqual(credly_data['recipient_email'], 'employee456@example.com')
      self.assertEqual(credly_data['badge_name'], 'Java Expert')

if __name__ == '__main__':
    unittest.main()
