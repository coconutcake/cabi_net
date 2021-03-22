import datetime
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


# funkcje pomocnicze
def get_current_time():
    return datetime.datetime.now()

def get_yesterday_date():
    yesterday = get_current_time()-datetime.timedelta(days=1)
    return yesterday.date()

def get_created_yesterdays(model):
    return model.objects.filter(created__date=get_yesterday_date())

def get_updated_yesterdays(model):
    return model.objects.filter(updated__date=get_yesterday_date())

def create_user(**params):
    return get_user_model().objects.create_user(**params)

def get_user(**params):
    return get_user_model().objects.get(**params)

def get_pks_list(objects):
    return [x.pk for x in objects]

def get_token(user_instance):
    instance = get_user_model().objects.get(pk=user_instance.pk)
    return Token.objects.get(user=instance)

def create_token(user_instance):
    instance = get_user_model().objects.get(pk=user_instance.pk)
    return Token.objects.create(user=instance)