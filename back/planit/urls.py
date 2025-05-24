from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/home/', include('home.urls')),
    path('api/report/', include('report.urls')),
    path('api/helper/', include('helper.urls')),
    path('api/setting/', include('setting.urls')),
]