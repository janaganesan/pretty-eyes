"""prettyeyes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('prettyeyes/', views.prettyeyes, name='prettyeyes'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='report_html'),
    path('orders/<int:pk>/reportjson/', views.report_detail, name='report_json'),
    path('report/<int:pk>/', views.report_table, name='report_table'),
    path('filters/', views.filters, name='filters'),
    path('diffreport/', views.diffreport, name='diffreport'),
]
