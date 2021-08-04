from django.urls import path,re_path,include
from .import views
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import views as auth_views



urlpatterns=[
re_path('^', include('django.contrib.auth.urls')),
path('',views.home,name='home'),
path('about_us/',views.aboutus,name='about_us'),
path('eligibility/',views.eligibility,name='eligibility'),
path('donor/',views.donor,name='donor'),
path('t_c/',views.tandc,name='t_c'),
re_path(r'^login/$',LoginView.as_view(template_name='login.html',redirect_field_name='next'),name='login'),
re_path(r'^logout/$',LogoutView.as_view(template_name='index.html',next_page="home"),name='logout'),
path('profile/',views.profile,name='profile'),
path('profile/favourite/',views.favourite,name='favourite'),
path('seek/',views.requests,name='seek'),
path('update/',views.update,name="update"),
path('delete/',views.delete,name="delete"),
path('profile/edit',views.update_profile,name='profile_edit'),
path('password/',views.change_password,name='change_password'),
path('contact/',views.contact_us,name='contact'),
re_path(r'^profile/(?P<pk>[0-9]+)$',views.detail,name='detail'),
re_path(r'^donor/(?P<pk>[0-9]+)$',views.detail,name='detail'),
path('signup/', views.signup_view, name="signup"),
path('sent/', views.activation_sent_view, name="activation_sent"),
path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),

]

