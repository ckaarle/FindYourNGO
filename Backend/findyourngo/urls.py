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
from findyourngo.restapi.controllers import views, ngo_controller, ngo_overview_controller, ngo_filter_controller, rating_controller
from findyourngo.restapi.tasks.background_tasks import start_background_tasks

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/login/', views.LoginView.as_view(), name='email'),
    path('users/register/', views.RegisterView.as_view(), name='email'),
    path('google/', views.GoogleView.as_view(), name='google'),
    path('facebook/', views.FacebookView.as_view(), name='facebook'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('dataImport', views.dataImport, name='dataImport'),
    path('clearDatabase', views.clearDatabase, name='clearDatabase'),
    path('clearBackgroundTasks', views.clearBackgroundTasks, name="clearBackgroundTasks"),
    url(r'^ngos$', ngo_controller.ngo_list),
    url(r'^ngoDetailItem', ngo_controller.ngo_detail),
    url(r'^ngos/filteroptions/$', ngo_filter_controller.ngo_filter_options),
    url(r'^ngos/filter/$', ngo_filter_controller.filter_options),
    url(r'^ngoOverviewItems', ngo_overview_controller.NgoOverviewItemList.as_view()),
    url(r'^twRating', rating_controller.tw_rating),
    url(r'^userReviewsForNgo', rating_controller.userReviews),
    url(r'^review', rating_controller.review),
    path('twUpdate', views.twUpdate),
    url(r'names', views.name_list),
    url('test/', views.TestView.as_view(), name='test'),
    url(r'^userReviewPresent', rating_controller.user_review_present)
]


start_background_tasks()