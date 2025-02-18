from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('orders.urls')),
    path('', TemplateView.as_view(template_name='main.html'), name='main'),
    path('total-list/',
         TemplateView.as_view(template_name='list.html'),
         name='list'),
    path('custom/',
         TemplateView.as_view(template_name='order_list.html'),
         name='order_list'),
    path('total-revenue/',
         TemplateView.as_view(template_name='total_revenue.html'),
         name='total_revenue'),
]
