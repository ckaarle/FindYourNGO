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
from django.contrib import admin
from rest_framework import routers
from findyourngo.restapi.controllers import views, ngo_controller, ngo_overview_item_controller, ngo_filter_controller
from findyourngo.restapi.controllers.ngo_filter_controller import NgoFilterView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('google/', views.GoogleView.as_view(), name='google'),
    path('facebook/', views.FacebookView.as_view(), name='facebook'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('dataImport', views.dataImport, name='dataImport'),
    path('clearDatabase', views.clearDatabase, name='clearDatabase'),
    url(r'^ngos$', ngo_controller.ngo_list),
    url(r'^ngoDetailItem', ngo_controller.ngo_detail),
    url(r'^ngos/filteroptions/$', ngo_filter_controller.ngo_filter_options),
    url(r'^ngos/filter/$', NgoFilterView.as_view()),
    path('recalculateTW', views.recalculateTW, name='recalculateTW'),
    url(r'countries', views.country_list),
    url(r'topics', views.topic_list),
    url(r'^ngoOverviewItems', ngo_overview_item_controller.NgoOverviewItemList.as_view()),
]

