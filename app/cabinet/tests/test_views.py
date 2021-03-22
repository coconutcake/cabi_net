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
LIST_CABINET_URL = "cabinet:cabinet_list"
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
        self.authenticated_2 = APIClient()
        self.unauthorized = APIClient()
        self.model = Cabinet
        user_payload = {
            "email": "sample@email.com",
            "password": "asdafdgsdgrtv"
        }
        user_payload_2 = {
            "email": "asda@easdl.net",
            "password": "adasddgsdgrtv"
        }

        self.user = create_user(**user_payload)
        self.user_2 = create_user(**user_payload_2)

        self.token = create_token(self.user)
        self.token_2 = create_token(self.user_2)

        self.authenticated.force_authenticate(user=self.user, token=self.token)
        self.authenticated_2.force_authenticate(user=self.user_2, token=self.token_2)
    
    
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
    

    def test_if_delete_auth_queryset_works(self):
        """
        Tests if get_queryset() filter properly instances of owner only
        """

        cabinet_payload_0 = {
            "name": "szafa1",
            "description": "opis",
            "owner": self.user
        }
        
        cabinet_payload_fk_0= cabinet_payload_0.copy()
        cabinet_payload_fk_0['owner'] = self.user.id

        cabinet_payload_1 = {
            "name": "sasdaa2",
            "description": "23",
            "owner": self.user
        }
        
        cabinet_payload_fk_1 = cabinet_payload_1.copy()
        cabinet_payload_fk_1['owner'] = self.user.id

        res_1 = self.authenticated.post(
            reverse(CREATE_CABINET_URL), data=cabinet_payload_fk_0
        )
        res_2 = self.authenticated_2.post(
            reverse(CREATE_CABINET_URL), data=cabinet_payload_fk_1
        )


        del_1 = self.authenticated.delete(
            reverse(DELETE_CABINET_URL, kwargs={'pk': res_2.data.get("id")})
        )
        get_2 = self.authenticated_2.get(
            reverse(LIST_CABINET_URL)
        )


        self.assertEqual(res_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_2.status_code, status.HTTP_201_CREATED)

        self.assertEqual(del_1.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(res_2.data, get_2.data)
    
    
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
    
    
    def test_if_list_auth_success(self):
        """
        Tests if list is available for auth user
        """
        cabinet_payload = {
            "name": "szafa1",
            "description": "opis",
            "owner": self.user
        }
        
        cabinet_payload_fk = cabinet_payload.copy()
        cabinet_payload_fk['owner'] = self.user.id

        created = self.authenticated.post(
            reverse(CREATE_CABINET_URL), data=cabinet_payload_fk)

        res = self.authenticated.get(
            reverse(LIST_CABINET_URL))
        
        self.assertTrue(res.data)
        self.assertIn(created.data, res.data)

    
    def test_if_list_auth_queryset_works(self):
        """
        Tests if get_queryset() properly lists instances of owner only
        """
        cabinet_payload_0 = {
            "name": "szafa1",
            "description": "opis",
            "owner": self.user
        }
        
        cabinet_payload_fk_0= cabinet_payload_0.copy()
        cabinet_payload_fk_0['owner'] = self.user.id

        cabinet_payload_1 = {
            "name": "sasdaa2",
            "description": "23",
            "owner": self.user
        }
        
        cabinet_payload_fk_1 = cabinet_payload_1.copy()
        cabinet_payload_fk_1['owner'] = self.user.id

        res_1 = self.authenticated.post(
            reverse(CREATE_CABINET_URL), data=cabinet_payload_fk_0
        )
        res_2 = self.authenticated_2.post(
            reverse(CREATE_CABINET_URL), data=cabinet_payload_fk_1
        )

        get_1 = self.authenticated.get(reverse(LIST_CABINET_URL))
        get_2 = self.authenticated_2.get(reverse(LIST_CABINET_URL))

        self.assertIn(res_1.data, get_1.data)
        self.assertIn(res_2.data, get_2.data)

        self.assertNotIn(res_1.data, get_2.data)
    
    
    
    
    
    # Anouthorized tests