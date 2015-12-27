__author__ = 'hamdiahmadi'

from django.conf.urls import url,patterns,include
from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^graph/$',views.makeGraph,name='makeGraph'),
    url(r'^form/$',views.form,name='form')
]