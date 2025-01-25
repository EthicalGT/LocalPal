from django.contrib import admin
from django.urls import path
from localpal import views
#pass: Vaish@2003

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage),
    path('home',views.homepage),
    path('explore',views.explore),
    path('feedback',views.feedback),
    path('adminlogin',views.adminlogin),
    path('admindashboard',views.admindashboard),
    path('addlocalgems',views.addlocalgems),
    path('deletelocalgems',views.deletelocalgems),
    path('feedbackinfo',views.feedbackinfo),
]
