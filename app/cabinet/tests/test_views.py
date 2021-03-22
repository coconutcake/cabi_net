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
RETRIEVE_CABINET_URL = "cabinet:cabinet_get"
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
        
        
    # Authenticated tests
    def test_if_created_auth_success(self):
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
    
    
    def test_if_updated_auth_success(self):
        """
        Tests if updated providing auth data
        """
        
        cabinet_payload_0 = {
            "name": "szafa1",
            "description": "opis",
            "owner": self.user
        }
        
        cabinet_payload_0_fk = cabinet_payload_0.copy()
        cabinet_payload_0_fk['owner'] = self.user.id
        
        cabinet_payload_1 = {
            "name": "szafa3",
            "description": "opi3s",
            "owner": self.user
        }
        
        
        cabinet_payload_1_fk = cabinet_payload_1.copy()
        cabinet_payload_1_fk['owner'] = self.user.id
        
        
        res = self.authenticated.post(
            reverse(CREATE_CABINET_URL), data=cabinet_payload_0_fk)
        
        edited = self.authenticated.put(\
            reverse(DETAIL_CABINET_URL,kwargs={'pk': res.data.get("id")}),
            data=cabinet_payload_1_fk
            )
        
        cabinet_payload_1_fk['id'] = edited.data['id']
              
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(edited.data, cabinet_payload_1_fk)
        
    
    def test_if_deleted_auth_success(self):
        """
        Tests if deleted using auth
        """
        
        cabinet_payload_0 = {
            "name": "szafa1",
            "description": "opis",
            "owner": self.user
        }
        
        cabinet_payload_0_fk = cabinet_payload_0.copy()
        cabinet_payload_0_fk['owner'] = self.user.id
        
        created = self.authenticated.post(
            reverse(CREATE_CABINET_URL), data=cabinet_payload_0_fk)
        
        deleted = self.authenticated.delete(
            reverse(DELETE_CABINET_URL, kwargs={'pk': created.data.get("id")}))
            
        self.assertEqual(deleted.status_code, status.HTTP_204_NO_CONTENT)
        
    
    def test_if_retrieve_auth_success(self):
        """
        Tests get providing auth
        """
        cabinet_payload_0 = {
            "name": "szafa1",
            "description": "opis",
            "owner": self.user
        }
        
        cabinet_payload_0_fk = cabinet_payload_0.copy()
        cabinet_payload_0_fk['owner'] = self.user.id
        
        created = self.authenticated.post(
            reverse(CREATE_CABINET_URL), data=cabinet_payload_0_fk)
        
        get = self.authenticated.get(
            reverse(RETRIEVE_CABINET_URL, kwargs={'pk': created.data.get("id")}))
        
        cabinet_payload_0_fk['id'] = get.data.get("id")
        
        self.assertEqual(get.status_code, status.HTTP_200_OK)
        self.assertEqual(get.data, cabinet_payload_0_fk)
        
        
        
    # Unouthorized tests