"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
import re

from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path, re_path
from django.views.static import serve
from rest_framework import routers

import mask.views as mask_views


router = routers.DefaultRouter()
router.register('masks', mask_views.MaskViewSet, base_name='mask')
router.register('defectpositions', mask_views.DefectPositionViewSet, base_name='defectposition')
router.register('defectpositionimages', mask_views.DefectPositionImageViewSet, base_name='defectpositionimage')
router.register('defects', mask_views.DefectViewSet, base_name='defect')

urlpatterns = [
  re_path('^', include(router.urls)),

  path('admin/', admin.site.urls),
  # we always serve static since even in production they should only be used when manually accessing the endpoints
  re_path(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')),
          serve,
          kwargs={'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
