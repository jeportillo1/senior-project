"""
Definition of urls for setup.
This mostly ties urls to methods in views.py
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


# variables inherited from django, replaced string value
# handler404 = 'app.views.error_handler_404'
# handler500 = 'app.views.error_handler_500'

# set the urls to views & gives them a name
# example : path('about/', views.about, name='about')
#  1st part (ex: "about/") is url part
#  2nd part (ex: views.about) is method that controls how page looks like the page looks
#  name part allows references to it (ex: name="about" allows href="{% url 'about' %}")
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('admin_settings/', views.admin_settings, name="admin_settings"),
    path('history/', views.history, name="history"),
    path('people/', views.people, name="people"),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('accounts/register/', views.register_view, name="signup"),

    path('user/password/', views.change_password, name='change_password'),
    path('user/profile/', views.profile, name ="profile"),
    path('user/settings/', views.user_settings, name="user_settings"),


    path('inventory/', views.InventoryIndex.as_view(), name='inventory_index'),
    path('inventory/<slug:search>', views.InventoryIndex.as_view(), name='inventory_index_searched'),
    path('inventory/items/<int:page>', views.items, name='items'),
    path('inventory/items/<int:page>/<slug:searchby>/<slug:searched>', views.items, name='items_searched'),
    path('inventory/create_item/', views.ItemCreateView.as_view(), name='create_item'),
    path('inventory/update_item/<int:pk>', views.ItemUpdateView.as_view(), name='update_item'),
    path('inventory/read_item/<int:pk>', views.ItemReadView.as_view(), name='read_item'),
    path('inventory/delete_item/<int:pk>', views.ItemDeleteView.as_view(), name='delete_item'),
    path('inventory/read_vendor/<int:pk>/', views.ReadVendor.as_view(), name='ReadVendor'),

    path('vendors/<int:item>/', views.VendorIndex.as_view(), name='VendorList'),
    path('vendors/<int:item>/delete_item/<int:pk>/', views.VendorDeleteView.as_view(), name='delete_vendor'),
    path('vendors/<int:item>/create_item/', views.VendorCreateView.as_view(), name='create_vendor'),
    path('vendors/<int:item>/update_item/<int:pk>/', views.VendorUpdateView.as_view(), name='update_vendor'),
    path('vendors/<int:itemfk>', views.vendors, name='vendorslist'),

    path('users/', views.PeopleIndex.as_view(), name="people_index"),
    path('users/<slug:search>', views.PeopleIndex.as_view(), name='people_index_searched'),
    path('users/update_user/<int:pk>', views.UserUpdateView.as_view(), name='update_user'),
    path('users/delete_user/<int:pk>', views.UserDeleteView.as_view(), name='delete_user'),
    path('users/people/', views.users_list, name="user_list"),

]
