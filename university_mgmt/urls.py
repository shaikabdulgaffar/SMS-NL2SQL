from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('students.urls')),  # Now '' goes to students home
    path('admin/', admin.site.urls),
    path('students/', include('students.urls')),
    path('nl2sql/', include('nl2sql.urls')),
]