from django.urls import path
from .views import (WelcomePageView, HomePageView, IhaCreateView, iha_delete_view, 
                    IhaUpdateView, RentalRecordCreateView, RentRecordListView, RentRecordUpdateView, rent_delete_view, UserRentRecordView, 
                    RentRecordApiV,RegisterView,LoginView,LogoutView)

urlpatterns = [
    path("", WelcomePageView.as_view(), name = "layout"),
    path("home/", HomePageView.as_view(), name = "home-page"),
    path("register/", RegisterView.as_view(), name = "register"),
    path("login/", LoginView.as_view(), name = "login"),
    path("logout/", LogoutView.as_view(), name = "logout"),
    path('create/', IhaCreateView.as_view(), name='iha_create'),
    path('<int:id>/delete/', iha_delete_view, name='iha-delete'),
    path('<int:pk>/update/', IhaUpdateView.as_view(), name='iha-update'),
    path('rent/', RentalRecordCreateView.as_view(), name='iha-rent'),
    path('rent-list/', RentRecordListView.as_view(), name='rent-list'),
    path('<int:pk>/rent-update/', RentRecordUpdateView.as_view(), name='rent-update'),
    path('user-rent/', UserRentRecordView.as_view(), name='user-rent'),
    path('<int:id>/rent-delete/', rent_delete_view, name='rent-delete'),
    path("rent-record-list/", RentRecordApiV.as_view(), name="rent-record-list")
]