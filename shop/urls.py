from. import views
from django.urls import path
urlpatterns = [
    path('',views.index,name='shopHome'),
    path('about/',views.about,name='AboutUs'),
    path('contact/',views.contact,name='ContactUs'),
    path('tracker/',views.tracker,name='TrackingStatus'),
    path('search/',views.search,name='Search'),
    path('productview/<str:pk>',views.prodView,name='prodview'),
    path('checkout/',views.checkout,name='Checkout'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('signup/',views.signup,name='signup'),
    path('postComent/',views.postCommet,name='postComment')
]