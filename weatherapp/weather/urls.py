from django.urls import path
from django.conf.urls import handler404
from .views import home,add,delete,error_404

urlpatterns = [
    path('', home, name='home'),
    path('<slug:units>',home, name='home'),
    path('add/',add, name='add' ),
    path('delete/<int:pk>/',delete,name='delete')
]

handler404 = error_404
