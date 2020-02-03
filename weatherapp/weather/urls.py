from django.urls import path
from .views import home,add,delete

urlpatterns = [
    path('', home, name='home'),
    path('<slug:units>',home, name='home'),
    path('add/',add, name='add' ),
    path('delete/<int:pk>/',delete,name='delete')
]
