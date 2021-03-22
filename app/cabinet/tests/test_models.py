

from django.test import TestCase
from django.forms.models import model_to_dict
from django.db import IntegrityError

from cabinet.models import Cabinet
from core.additionals.functions import *



class CabinetCase(TestCase):
    """
    Testing model Cabinet
    """
    
    def setUp(self):
        self.model = Cabinet
        user = {
            "email": "sample@email.com",
            "password": "asdafdgsdgrtv"
        }

        self.user = create_user(**user)
   
        
    def test_if_created_success(self):
        """
        Tests if model is created providing minimal proper data
        """
        
        params = {
            "name": "szafa1",
            "description": "opis",
            "owner": self.user,
        }
        
        params_fk = params.copy()
        params_fk['owner'] = self.user.id
        
        created = self.model.objects.create(**params)
        
        self.assertTrue(created)
        self.assertEqual(
            model_to_dict(created, fields = params.keys()),
            params_fk)


    def test_if_updated_success(self):
        """ 
        Tests if object is updated 
        """
        
        params_0 = {
            "name": "szafa1",
            "description": "opis",
            "owner": self.user,
            }
        
        params_0_fk = params_0.copy()
        params_0_fk['owner'] = self.user.id
        
        params_1 = {
            "name": "szafa2",
            "description": "opis2",
            "owner": self.user,
        }
        
        params_1_fk = params_1.copy()
        params_1_fk['owner'] = self.user.id
        
        
        created = self.model.objects.create(**params_0)
        self.model.objects.filter(pk=created.pk).update(**params_1)
        updated = self.model.objects.get(pk=created.pk)
        
        self.assertEqual(
            model_to_dict(updated, fields=params_1.keys()),params_1_fk)

    
    def test_if_deleted_success(self):
        """
        Tests if deleted
        """
        
        params_0 = {
            "name": "szafa1",
            "description": "opis",
            "owner": self.user,
            }
        
        params_0_fk = params_0.copy()
        params_0_fk['owner'] = self.user.id
        
        created = self.model.objects.create(**params_0)
        
        self.assertTrue(created)
        self.assertEqual(
            model_to_dict(created, fields = params_0.keys()),
            params_0_fk)
        
        self.model.objects.filter(pk=created.id).delete()
        
        self.assertFalse(self.model.objects.filter(pk=created.pk).exists())
        
        
        
        
        