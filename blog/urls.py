from. import views
from django.urls import path
urlpatterns = [
    path('',views.index,name='bloghome'),
    path('home/',views.index,name='home')
]