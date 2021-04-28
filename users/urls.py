from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserViewSet, generate_jwttoken, send_email

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')

auth_urls = [
    path('token/', generate_jwttoken,
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('email/', send_email, name='send_email'),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_urls)),
]
