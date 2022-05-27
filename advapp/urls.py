from django.urls import path
from . import views

app_name = 'advapp'

urlpatterns = [
    path('main/<int:id>/<str:customer>', views.Main, name =  'main'),
    
    # Display All Ads
    path('display/<str:uname>', views.displayAds, name = 'display'),
    
    # When user clicks an ad, get the details of perticular ad
    path('detail/<str:uid>/<str:adid>', views.getAdDetails, name = 'detail'),
    
    # Manage You own ads
    path('manage/<int:id>', views.manageAds, name = 'manage'),
    path('create/<int:id>', views.AdCreate, name = 'create'),
]
