from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def login_required_custom(view_func):
    return login_required(view_func, login_url='/')
