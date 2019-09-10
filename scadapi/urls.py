"""scadapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from mainapp import views
from mainapp import api

urlpatterns = [
    url(r'^$', views.main_page),

    url(r'^api/provision/$', api.provision_view),

    url(r'^api/experiment/$', api.experiment_view),
    url(r'^api/experiment/(\d+)/delete/$', api.experiment_deletion_view),

    url(r'^api/temperature/$', api.temperature_view),

    url(r'^api/automation/$', api.automation_view),
    url(r'^api/automation/(\w+)/$', api.automation_view),

    url(r'^api/thermistor/$', api.thermistor_view),
    url(r'^api/thermistor/(\d+)/$', api.thermistor_view),

    url(r'^api/(\w+)/$', api.multiple_generic_device_state_view),
    url(r'^api/(\w+)/(\d+)/$', api.single_generic_device_state_view),

    url(r'^api/(\w+)/(\d+)/(\w+)/$', api.single_generic_device_actuation_view),

	url(r'^api/$', api.all_devices_state_list_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
