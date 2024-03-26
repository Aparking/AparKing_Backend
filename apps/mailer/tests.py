from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

class MailerViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_mailer_view(self):
        response = self.client.get('/mailer/send_email/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mailer/email_form_page.html')

    def test_send_mail(self):
        data = {'subject': 'subjetc',
                'message': 'message',
                'mailTo': 'sergiosantiago0403@gmail.com'}
        response = self.client.post('/mailer/send_email/', data)
    
        self.assertEqual(response.status_code, 302)

    def test_send_mail_fail(self):
        data = {'message': 'message',
                'mailTo': 'mail@gmail.com'}

        response = self.client.post('/mailer/send_email/', data)
        
        self.assertEqual(response.request['PATH_INFO'], '/mailer/send_email/')
        self.assertEqual(response.status_code, 200)
