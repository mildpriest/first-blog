from django.conf.urls import include, url
from django.contrib import admin

# 개발 media 폴더 접근을 위한 세팅
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'', include('blog.urls')),
    url(r'', include('search.urls')),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # 개발 media 폴더 접근을 위한 세팅
