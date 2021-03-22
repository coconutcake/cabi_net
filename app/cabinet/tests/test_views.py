from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.forms import model_to_dict
import json

from cabinet.models import Cabinet
from core.additionals.functions import *


# URLS
CREATE_CABINET_URL = "cabinet:cabinet_create"
DETAIL_CABINET_URL = "cabinet:cabinet_detail"
DELETE_CABINET_URL = "cabinet:cabinet_delete"


class CabinetApiCase(TestCase):
    """
    API tests for Cabinet
    """
    
    def setUp(self):
        self.authenticated = APIClient()
        self.unauthorized = APIClient()
        self.model = Cabinet
        user_payload = {
            "email": "sample@email.com",
            "password": "asdafdgsdgrtv"
        }

        self.user = create_user(**user_payload)
        self.token = create_token(self.user)
        self.authenticated.force_authenticate(user=self.user, token=self.token)
        
    
    def test_if_created_success(self):
        """
        Tests if created api success providing minimal authenticated data
        """
        
        cabinet_payload = {
            "name": "szafa1",
            "description": "opis",
            "owner": self.user
        }
        
        cabinet_payload_fk = cabinet_payload.copy()
        cabinet_payload_fk['owner'] = self.user.id
                
        
        res = self.authenticated.post(
            reverse(CREATE_CABINET_URL), data=cabinet_payload_fk)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        