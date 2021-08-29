from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.forms import model_to_dict
import json
import random
import string

from cabinet.models import Cabinet, U
from core.additionals.functions import *
from core.additionals.generators import *


# Tests -----------------------------------------------------------------------


class CabinetApiCase(TestCase):
    """
    API tests for Cabinet
    """

    def setUp(self):
        self.model = Cabinet

        self.authenticated = APIClient()
        self.authenticated_2 = APIClient()
        self.unauthorized = APIClient()

        self.urls = self.APIurls()

        self.user = create_user(**user_payload_gen().__next__())
        self.user_2 = create_user(**user_payload_gen().__next__())

        self.token = create_token(self.user)
        self.token_2 = create_token(self.user_2)

        self.authenticated.force_authenticate(user=self.user, token=self.token)
        self.authenticated_2.force_authenticate(user=self.user_2, token=self.token_2)
        
        
        self.excluded_fields = ["u_count"] # <- These fields are being excluded from payloads during various tests

    def APIurls(self):
        """
        Returns API urls for model
        """

        prefix = "cabinet"
        app = "cabinet"

        urls = {
            "list": f"{app}:{prefix}_list",
            "retrieve": f"{app}:{prefix}_get",
            "retrieve_expanded": f"{app}:{prefix}_get_exp",
            "create": f"{app}:{prefix}_create",
            "detail": f"{app}:{prefix}_detail",
            "delete": f"{app}:{prefix}_delete",
        }

        return urls

    def model_obj_payload_gen(self):
        """
        Generates various model object payloads (this must to be customized)
        """

        while True:

            string_gen = custom_string_gen(
                big_letters=True, digits=True, gen_range=[5, 16]
            )
            int_gen = custom_number_gen(
                gen_range=[1,50]
            )
            payload = {
                "name": string_gen.__next__(),
                "description": string_gen.__next__(),
                "u_count": int_gen.__next__(),
                "owner": self.user,
            }

            yield payload

    # Authenticated user tests ------------------------------------------------
    def test_if_created_auth_success(self):
        """
        Tests if created api success providing minimal authenticated data
        """

        p_gen = self.model_obj_payload_gen()

        payload_0 = p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            data=convert_model_payload_no_instances(payload_0),
        )

        self.assertEqual(created.status_code, status.HTTP_201_CREATED)

    def test_if_updated_auth_success(self):
        """
        Tests if updated providing auth data
        """

        p_gen = self.model_obj_payload_gen()

        payload_0, payload_1 = p_gen.__next__(), p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        edited = self.authenticated.put(
            reverse(self.urls.get("detail"), kwargs={"pk": created.data.get("id")}),
            data=convert_model_payload_no_instances(payload_1),
        )

        payload_1["id"] = edited.data["id"]
        
        converted_payload_1 = convert_model_payload_no_instances(payload_1)
    
        exclude_fields(self.excluded_fields, payloads=[edited.data, converted_payload_1])
        
        
        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        self.assertEqual(edited.data, converted_payload_1)

    def test_if_updated_auth_queryset_success(self):
        """
        Tests if get_queryset() properly returns only owner records not foreign one
        """

        p_gen = self.model_obj_payload_gen()

        payload_0, payload_1 = p_gen.__next__(), p_gen.__next__()

        created_1 = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )
        created_2 = self.authenticated_2.post(
            reverse(self.urls.get("create")),
            data=convert_model_payload_no_instances(payload_1),
        )

        not_updated = self.authenticated_2.put(
            reverse(self.urls.get("detail"), kwargs={"pk": created_1.data.get("id")}),
            data=convert_model_payload_no_instances(payload_1),
        )

        get_2 = self.authenticated_2.get(reverse(self.urls.get("list")))

        self.assertEqual(created_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created_2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(not_updated.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(created_2.data, get_2.data)
        self.assertNotIn(created_1.data, get_2.data)

    def test_if_deleted_auth_success(self):
        """
        Tests if deleted using auth
        """

        p_gen = self.model_obj_payload_gen()

        payload_0, payload_1 = p_gen.__next__(), p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        deleted = self.authenticated.delete(
            reverse(self.urls.get("delete"), kwargs={"pk": created.data.get("id")})
        )

        self.assertEqual(deleted.status_code, status.HTTP_204_NO_CONTENT)

    def test_if_delete_auth_queryset_success(self):
        """
        Tests if get_queryset() filter properly instances of owner only not foreign one
        """

        p_gen = self.model_obj_payload_gen()

        payload_0, payload_1 = p_gen.__next__(), p_gen.__next__()

        post_1 = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        post_2 = self.authenticated_2.post(
            reverse(self.urls.get("create")),
            data=convert_model_payload_no_instances(payload_1),
        )

        del_1 = self.authenticated.delete(
            reverse(self.urls.get("delete"), kwargs={"pk": post_2.data.get("id")})
        )

        get_2 = self.authenticated_2.get(reverse(self.urls.get("list")))

        self.assertEqual(post_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post_2.status_code, status.HTTP_201_CREATED)

        self.assertEqual(del_1.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(post_2.data, get_2.data)
        
    def test_if_retrieve_auth_success(self):
        """
        Tests get providing auth
        """

        p_gen = self.model_obj_payload_gen()

        payload_0, payload_1 = p_gen.__next__(), p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        get = self.authenticated.get(
            reverse(self.urls.get("retrieve"), kwargs={"pk": created.data.get("id")})
        )

        payload_0["id"] = get.data.get("id")
        
        converted_payload = convert_model_payload_no_instances(payload_0)
    
        exclude_fields(self.excluded_fields, payloads=[payload_0, converted_payload])
        
        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get.status_code, status.HTTP_200_OK)
        self.assertEqual(get.data, converted_payload)

    def test_if_retrieve_auth_success_expanded(self):
        """
        Tests if retrieved expanded serializer providing auth data
        """

        p_gen = self.model_obj_payload_gen()

        payload_0 = p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        get = self.authenticated.get(
            reverse(
                self.urls.get("retrieve_expanded"), kwargs={"pk": created.data["id"]}
            )
        )

        self.assertEqual(created.status_code, status.HTTP_201_CREATED)

    def test_if_retrieve_auth_queryset_success_expanded(self):
        """
        Tests if get_queryset() returns only owner records
        """

        p_gen = self.model_obj_payload_gen()

        payload_0 = p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        not_retrived = self.authenticated_2.get(
            reverse(
                self.urls.get("retrieve_expanded"), kwargs={"pk": created.data["id"]}
            )
        )

        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        self.assertEqual(not_retrived.status_code, status.HTTP_404_NOT_FOUND)

    def test_if_retrieve_auth_queryset_success(self):
        """
        Tests if get_queryset() returns only owner records not foreign one
        """

        p_gen = self.model_obj_payload_gen()

        payload_0 = p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        not_retrived = self.authenticated_2.get(
            reverse(self.urls.get("retrieve"), kwargs={"pk": created.data["id"]})
        )

        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        self.assertEqual(not_retrived.status_code, status.HTTP_404_NOT_FOUND)

    def test_if_list_auth_success(self):
        """
        Tests if list is available for auth user
        """

        p_gen = self.model_obj_payload_gen()

        payload_0, payload_1 = p_gen.__next__(), p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        res = self.authenticated.get(reverse(self.urls.get("list")))

        self.assertTrue(res.data)
        self.assertIn(created.data, res.data)

    def test_if_list_auth_queryset_success(self):
        """
        Tests if get_queryset() properly lists instances of owner only not foreign one
        """

        p_gen = self.model_obj_payload_gen()

        cabinet_payload_fk_0, cabinet_payload_fk_1 = p_gen.__next__(), p_gen.__next__()

        created_1 = self.authenticated.post(
            reverse(self.urls.get("create")), data=cabinet_payload_fk_0
        )
        created_2 = self.authenticated_2.post(
            reverse(self.urls.get("create")), data=cabinet_payload_fk_1
        )

        get_1 = self.authenticated.get(reverse(self.urls.get("list")))
        get_2 = self.authenticated_2.get(reverse(self.urls.get("list")))

        self.assertIn(created_1.data, get_1.data)
        self.assertNotIn(created_1.data, get_2.data)

    # NotAuthenticated user tests ---------------------------------------------
    def test_if_created_unauth_failed(self):
        """
        Tests if failed creating new object by unauthorized user
        """

        p_gen = self.model_obj_payload_gen()

        payload_0 = p_gen.__next__()

        not_created = self.unauthorized.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        self.assertEqual(not_created.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_if_updated_unauth_failed(self):
        """
        Tests if failed during update by unauthorized user
        """

        p_gen = self.model_obj_payload_gen()

        payload_0, payload_1 = p_gen.__next__(), p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        not_updated = self.unauthorized.put(
            reverse(self.urls.get("detail"), kwargs={"pk": created.data["id"]}),
            data=convert_model_payload_no_instances(payload_1),
        )

        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        self.assertEqual(not_updated.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_if_deleted_unauth_failed(self):
        """
        Tests if failed deleting object by unathorized user
        """

        p_gen = self.model_obj_payload_gen()

        payload_0 = p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        not_deleted = self.unauthorized.delete(
            reverse(self.urls.get("delete"), kwargs={"pk": created.data["id"]})
        )

        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        self.assertEqual(not_deleted.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_if_retrieve_unauth_failed(self):
        """
        Tests if failed during retrive by unauth user
        """

        p_gen = self.model_obj_payload_gen()

        payload_0 = p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        not_retrieved = self.unauthorized.get(
            reverse(self.urls.get("retrieve"), kwargs={"pk": created.data["id"]})
        )

        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        self.assertEqual(not_retrieved.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_if_list_unauth_failed(self):
        """
        Tests if list is not available for unauthorized user
        """

        p_gen = self.model_obj_payload_gen()

        payload_0 = p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        not_listed = self.unauthorized.get(reverse(self.urls.get("list")))

        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        self.assertEqual(not_listed.status_code, status.HTTP_401_UNAUTHORIZED)


class UApiCase(TestCase):
    """
    API tests for Cabinet

    """

    def setUp(self):
        self.model = U

        self.authenticated = APIClient()
        self.authenticated_2 = APIClient()
        self.unauthorized = APIClient()

        self.urls = self.APIurls()

        self.user = create_user(**user_payload_gen().__next__())
        self.user_2 = create_user(**user_payload_gen().__next__())

        self.token = create_token(self.user)
        self.token_2 = create_token(self.user_2)

        self.authenticated.force_authenticate(user=self.user, token=self.token)
        self.authenticated_2.force_authenticate(user=self.user_2, token=self.token_2)
        
        self.excluded_fields = [] # <- These fields are being excluded from payloads during various tests
        
    def custom_obj_gen(self, objclass):
        """
        Executes pre phases in order to prepare additional objects to work with in futher steps
        """
        
        self.objClass = objclass
        
        while True:
            p_gen = self.objClass.model_obj_payload_gen(self)
        
            payload_0 = p_gen.__next__()

            cabinet_created = self.authenticated.post(
                reverse(self.objClass.APIurls(self).get("create")),
                data=convert_model_payload_no_instances(payload_0),
            )
            
            yield cabinet_created

    def APIurls(self):
        """
        Returns API urls for model
        """

        prefix = "u"
        app = "cabinet"

        urls = {
            "list": f"{app}:{prefix}_list",
            "retrieve": f"{app}:{prefix}_get",
            "retrieve_expanded": f"{app}:{prefix}_get_exp",
            "create": f"{app}:{prefix}_create",
            "detail": f"{app}:{prefix}_detail",
            "delete": f"{app}:{prefix}_delete",
        }

        return urls

    def model_obj_payload_gen(self):
        """
        Generates various model object payloads (this must to be customized)
        """

        while True:

            string_gen = custom_string_gen(
                big_letters=True, digits=True, gen_range=[5, 16]
                )

            number_gen = custom_number_gen(
                gen_range=[1, 100]
                )
            
            obj_gen = self.custom_obj_gen(
                objclass=CabinetApiCase
                )

            payload = {
                "position": number_gen.__next__(),
                "cabinet": obj_gen.__next__().data.get("id")
                }
            
            
            yield payload

    # Authenticated user tests ------------------------------------------------
    def test_if_created_auth_success(self):
        """
        Tests if created api success providing minimal authenticated data
        """

        p_gen = self.model_obj_payload_gen()

        payload_0 = p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            data=convert_model_payload_no_instances(payload_0),
        )

        self.assertEqual(created.status_code, status.HTTP_201_CREATED)

    def test_if_updated_auth_success(self):
        """
        Tests if updated providing auth data
        """

        p_gen = self.model_obj_payload_gen()

        payload_0, payload_1 = p_gen.__next__(), p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        edited = self.authenticated.put(
            reverse(self.urls.get("detail"), kwargs={"pk": created.data.get("id")}),
            data=convert_model_payload_no_instances(payload_1),
        )

        payload_1["id"] = edited.data["id"]
        
        converted_payload_1 = convert_model_payload_no_instances(payload_1)
    
        exclude_fields(self.excluded_fields, payloads=[edited.data, converted_payload_1])

        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        self.assertEqual(edited.data, converted_payload_1)

    def test_if_updated_auth_queryset_success(self):
        """
        Tests if get_queryset() properly returns only owner records not foreign one
        """

        p_gen = self.model_obj_payload_gen()

        payload_0, payload_1 = p_gen.__next__(), p_gen.__next__()

        created_1 = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )
        created_2 = self.authenticated_2.post(
            reverse(self.urls.get("create")),
            data=convert_model_payload_no_instances(payload_1),
        )

        not_updated = self.authenticated_2.put(
            reverse(self.urls.get("detail"), kwargs={"pk": created_1.data.get("id")}),
            data=convert_model_payload_no_instances(payload_1),
        )

        get_2 = self.authenticated_2.get(
            reverse(self.urls.get("list"))
            )
        

        self.assertEqual(created_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created_2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(not_updated.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotIn(created_1.data, get_2.data)
        # self.assertIn(created_2.data, get_2.data)

    def test_if_deleted_auth_success(self):
        """
        Tests if deleted using auth
        """

        p_gen = self.model_obj_payload_gen()

        payload_0, payload_1 = p_gen.__next__(), p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        deleted = self.authenticated.delete(
            reverse(self.urls.get("delete"), kwargs={"pk": created.data.get("id")})
        )

        self.assertEqual(deleted.status_code, status.HTTP_204_NO_CONTENT)

    def test_if_delete_auth_queryset_success(self):
        """
        Tests if get_queryset() filter properly instances of owner only not foreign one
        """

        p_gen = self.model_obj_payload_gen()

        payload_0, payload_1 = p_gen.__next__(), p_gen.__next__()

        post_1 = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        post_2 = self.authenticated_2.post(
            reverse(self.urls.get("create")),
            data=convert_model_payload_no_instances(payload_1),
        )

        del_1 = self.authenticated.delete(
            reverse(self.urls.get("delete"), kwargs={"pk": post_2.data.get("id")})
        )

        get_2 = self.authenticated_2.get(reverse(self.urls.get("list")))

        self.assertEqual(post_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post_2.status_code, status.HTTP_201_CREATED)

        self.assertEqual(del_1.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(post_2.data, get_2.data)

    def test_if_retrieve_auth_success(self):
        """
        Tests get providing auth
        """

        p_gen = self.model_obj_payload_gen()

        payload_0, payload_1 = p_gen.__next__(), p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        get = self.authenticated.get(
            reverse(self.urls.get("retrieve"), kwargs={"pk": created.data.get("id")})
        )

        payload_0["id"] = get.data.get("id")


        converted_payload_0 = convert_model_payload_no_instances(payload_0)
    
        exclude_fields(self.excluded_fields, payloads=[get.data, converted_payload_0])

        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get.status_code, status.HTTP_200_OK)
        self.assertEqual(get.data, converted_payload_0)

    def test_if_retrieve_auth_queryset_success(self):
        """
        Tests if get_queryset() returns only owner records not foreign one
        """

        p_gen = self.model_obj_payload_gen()

        payload_0 = p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        not_retrived = self.authenticated_2.get(
            reverse(self.urls.get("retrieve"), kwargs={"pk": created.data["id"]})
        )

        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        self.assertEqual(not_retrived.status_code, status.HTTP_404_NOT_FOUND)

    def test_if_list_auth_success(self):
        """
        Tests if list is available for auth user
        """

        p_gen = self.model_obj_payload_gen()

        payload_0, payload_1 = p_gen.__next__(), p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        res = self.authenticated.get(reverse(self.urls.get("list")))

        self.assertTrue(res.data)
        self.assertIn(created.data, res.data)

    def test_if_list_auth_queryset_success(self):
        """
        Tests if get_queryset() properly lists instances of owner only not foreign one
        """

        p_gen = self.model_obj_payload_gen()

        cabinet_payload_fk_0, cabinet_payload_fk_1 = p_gen.__next__(), p_gen.__next__()

        created_1 = self.authenticated.post(
            reverse(self.urls.get("create")), data=cabinet_payload_fk_0
        )
        created_2 = self.authenticated_2.post(
            reverse(self.urls.get("create")), data=cabinet_payload_fk_1
        )

        get_1 = self.authenticated.get(reverse(self.urls.get("list")))
        get_2 = self.authenticated_2.get(reverse(self.urls.get("list")))

        self.assertIn(created_1.data, get_1.data)
        self.assertNotIn(created_1.data, get_2.data)
        
    # # NotAuthenticated user tests ---------------------------------------------
    def test_if_created_unauth_failed(self):
        """
        Tests if failed creating new object by unauthorized user
        """

        p_gen = self.model_obj_payload_gen()

        payload_0 = p_gen.__next__()

        not_created = self.unauthorized.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        self.assertEqual(not_created.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_if_updated_unauth_failed(self):
        """
        Tests if failed during update by unauthorized user
        """

        p_gen = self.model_obj_payload_gen()

        payload_0, payload_1 = p_gen.__next__(), p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        not_updated = self.unauthorized.put(
            reverse(self.urls.get("detail"), kwargs={"pk": created.data["id"]}),
            data=convert_model_payload_no_instances(payload_1),
        )

        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        self.assertEqual(not_updated.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_if_deleted_unauth_failed(self):
        """
        Tests if failed deleting object by unathorized user
        """

        p_gen = self.model_obj_payload_gen()

        payload_0 = p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        not_deleted = self.unauthorized.delete(
            reverse(self.urls.get("delete"), kwargs={"pk": created.data["id"]})
        )

        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        self.assertEqual(not_deleted.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_if_retrieve_unauth_failed(self):
        """
        Tests if failed during retrive by unauth user
        """

        p_gen = self.model_obj_payload_gen()

        payload_0 = p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        not_retrieved = self.unauthorized.get(
            reverse(self.urls.get("retrieve"), kwargs={"pk": created.data["id"]})
        )

        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        self.assertEqual(not_retrieved.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_if_list_unauth_failed(self):
        """
        Tests if list is not available for unauthorized user
        """

        p_gen = self.model_obj_payload_gen()

        payload_0 = p_gen.__next__()

        created = self.authenticated.post(
            reverse(self.urls.get("create")),
            convert_model_payload_no_instances(payload_0),
        )

        not_listed = self.unauthorized.get(reverse(self.urls.get("list")))

        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        self.assertEqual(not_listed.status_code, status.HTTP_401_UNAUTHORIZED)

