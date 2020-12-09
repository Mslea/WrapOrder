"""project3 URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from process_order import views
from webcam import views as wbviews
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('order_detail/<str:ordercode>/',views.order_detail,name='cart'),
    path('order_list/',views.order_list,name='order_list'),
    path('wrap/',wbviews.wrap,name = 'wrap'),
    path('video_feed/', wbviews.video_feed, name="video-feed"),
    path('login/',views.user_login,name = 'login'),
    path('logout/', views.user_logout,name = 'logout'),
    path('validate_login/',views.validate_login,name = 'validate_login'),
    path('wrap/orderwrap/',wbviews.getorderwrap,name = 'getorderwrap')
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)