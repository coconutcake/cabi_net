from django.test import TestCase
from django.forms.models import model_to_dict
from django.db import IntegrityError

from cabinet.models import Cabinet, U
from core.additionals.functions import *
from core.additionals.generators import *


class CabinetCase(TestCase):
    """
    Testing model Cabinet
    """

    def setUp(self):
        self.model = Cabinet
        self.user = create_user(**user_payload_gen().__next__())
        self.instances_fields = get_model_payload_instances_fields(
            self.model_obj_payload_gen().__next__()
        )

    def model_obj_payload_gen(self):
        """
        Generates various model object payloads (must to be customized)
        """

        while True:

            string_gen = custom_string_gen(
                big_letters=True, digits=True, gen_range=[5, 16]
            )

            payload = {
                "name": string_gen.__next__(),
                "description": string_gen.__next__(),
                "owner": self.user,
            }

            yield payload

    def test_if_created_success(self):
        """
        Tests if model is created providing minimal proper data
        """

        p_gen = self.model_obj_payload_gen()

        payload_0 = p_gen.__next__()

        created = self.model.objects.create(**payload_0)

        created_with_instances = model_to_dict_with_instances(
            instance=created, fields=payload_0, instance_fields=self.instances_fields
        )

        self.assertTrue(created)
        self.assertEqual(created_with_instances, payload_0)

    def test_if_updated_success(self):
        """ 
        Tests if object is updated 
        """

        p_gen = self.model_obj_payload_gen()

        payload_0 = p_gen.__next__()
        payload_1 = p_gen.__next__()

        created = self.model.objects.create(**payload_0)

        self.model.objects.filter(pk=created.pk).update(**payload_1)

        updated = self.model.objects.get(pk=created.pk)

        updated_with_instances = model_to_dict_with_instances(
            instance=updated, fields=payload_0, instance_fields=self.instances_fields
        )

        self.assertEqual(updated_with_instances, payload_1)

    def test_if_deleted_success(self):
        """
        Tests if deleted
        """

        p_gen = self.model_obj_payload_gen()

        payload_0 = p_gen.__next__()

        created = self.model.objects.create(**payload_0)

        created_with_instances = model_to_dict_with_instances(
            instance=created, fields=payload_0, instance_fields=self.instances_fields
        )

        self.assertTrue(created)
        self.assertEqual(created_with_instances, payload_0)

        self.model.objects.filter(pk=created.id).delete()

        self.assertFalse(self.model.objects.filter(pk=created.pk).exists())


class UCase(TestCase):
    """
    Testing model Cabinet
    """

    def setUp(self):
        self.model = U
        self.user = create_user(**user_payload_gen().__next__())
        self.instances_fields = get_model_payload_instances_fields(
            self.model_obj_payload_gen().__next__()
        )

    def model_obj_payload_gen(self):
        """
        Generates various model object payloads (must to be customized)
        """

        while True:

            string_gen = custom_string_gen(
                big_letters=True, digits=True, gen_range=[5, 16]
            )
            number_gen = custom_number_gen(gen_range=[1, 100])

            payload = {
                "position": number_gen.__next__(),
            }

            yield payload

    def test_if_created_success(self):
        """
        Tests if model is created providing minimal proper data
        """

        p_gen = self.model_obj_payload_gen()

        payload_0 = p_gen.__next__()

        created = self.model.objects.create(**payload_0)

        created_with_instances = model_to_dict_with_instances(
            instance=created, fields=payload_0, instance_fields=self.instances_fields
        )

        self.assertTrue(created)
        self.assertEqual(created_with_instances, payload_0)

    def test_if_updated_success(self):
        """ 
        Tests if object is updated 
        """

        p_gen = self.model_obj_payload_gen()

        payload_0 = p_gen.__next__()
        payload_1 = p_gen.__next__()

        created = self.model.objects.create(**payload_0)

        self.model.objects.filter(pk=created.pk).update(**payload_1)

        updated = self.model.objects.get(pk=created.pk)

        updated_with_instances = model_to_dict_with_instances(
            instance=updated, fields=payload_0, instance_fields=self.instances_fields
        )

        self.assertEqual(updated_with_instances, payload_1)

    def test_if_deleted_success(self):
        """
        Tests if deleted
        """

        p_gen = self.model_obj_payload_gen()

        payload_0 = p_gen.__next__()

        created = self.model.objects.create(**payload_0)

        created_with_instances = model_to_dict_with_instances(
            instance=created, fields=payload_0, instance_fields=self.instances_fields
        )

        self.assertTrue(created)
        self.assertEqual(created_with_instances, payload_0)

        self.model.objects.filter(pk=created.id).delete()

        self.assertFalse(self.model.objects.filter(pk=created.pk).exists())

