import json

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Templates


class TemplatesTestCase(APITestCase):
    
    def GetTemplateTestCase(self):
        customer_id="999"
        response=self.client.get("/te/customer/"+customer_id+"/templates")
        print(response)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def PostTemplateTestCase(self):
        customer_id="999"
        response=self.client.post("/te/customer/"+customer_id+"/templates")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        