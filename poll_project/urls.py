
from django.contrib import admin
from django.urls import path

from poll import views as poll_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", poll_views.uhome, name='uhome'),
    path("poll/uhome", poll_views.uhome, name='uhome'),
    path('poll/home', poll_views.home, name='home'),
    path('create', poll_views.create, name='create'),
    path('vote/<poll_id>/', poll_views.vote, name='vote'),
    path('results/<poll_id>/', poll_views.results, name='results'),
    path("usignup",poll_views.usignup,name="usignup"),
    path("poll/uwelcome",poll_views.uwelcome,name="uwelcome"),
    path("ulogout",poll_views.ulogout,name="ulogout"),
    path("ucp",poll_views.ucp,name="ucp"),
    path("delete/<poll_id>/",poll_views.delete,name="delete"),

]
