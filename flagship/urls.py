"""flagship URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include

"""!!!!THESE 2 from's ARE NECESSARY FOR DEVELOPMENT SERVER!!!!"""
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('gallery/', include('gallery.urls')),
]

urlpatterns += [
    path('forums/', include('forums.urls')),
]

urlpatterns += [
    path('api/', include('api.urls')),
]

"""!!!!THIS IS NECESSARY TO RENDER MEDIA FILES FROM DEVELOPMENT SERVER!!!"""
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)