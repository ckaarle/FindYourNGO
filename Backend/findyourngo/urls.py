"""findyourngo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from findyourngo.restapi.controllers import views, ngo_controller, ngo_overview_item_controller

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('dataImport', views.dataImport, name='dataImport'),
    path('clearDatabase', views.clearDatabase, name='clearDatabase'),
    url(r'^ngos', ngo_controller.ngo_list),
    url(r'^ngos/(?P<pk>[0-9]+)$', ngo_controller.ngo_detail),
    url(r'^ngoOverviewItems', ngo_overview_item_controller.ngo_overview_item_list)
]

