"""
Definition of forms.
"""

# from email.policy import default
from django import forms
from django.contrib.auth.forms import AuthenticationForm
try:
    from django.utils.translation import ugettext_lazy as _
except Exception:
    from django.utils.translation import gettext_lazy as _
# from django.utils.safestring import mark_safe
from .models import (
    # People,
    Vendor,
    personal_user_settings,
    global_settings,
    # inventory as inventory_form,
    # person as person_form,
    Item,
    mock_inventory
)
# from django.contrib.auth.models import User
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm # noqa: F401
from django.contrib.auth.forms import UserCreationForm
# from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin

from django.contrib.auth import get_user_model

User = get_user_model()

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = personal_user_settings
        fields = ["font_type", "paging_by"]
        labels = {
            "font_type" : "Font type",
            "paging_by" : "Items per page",
        }

        
class GlobalSettingsForm(forms.ModelForm):
    class Meta:
        model = global_settings
        fields = ["allow_inventory_changes",  "allow_inventory_purchases", "allow_adding_new_users", "allow_paring_data",]
        labels = {
            "allow_inventory_changes" : "enable inventory changes",
            "allow_inventory_purchases" : "enable inventory purchases",
            "allow_adding_new_users" : "enable registering new users",
            "allow_paring_data" : "enable parsing from google doc",
        }


class profileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username' , 'first_name', 'last_name', 'email']

class UserForm(BSModalModelForm):
    class Meta:
        model = User
        fields = ['username' , 'first_name', 'last_name', 'email', 'rank']

class ItemForm(BSModalModelForm):
    class Meta: 
        model = Item
        fields = ["part_number", "title", "image_path", "stock", "threshold"]
        exclude = ["alert"]

        labels = {
            "part_number" : "Part #",
            "title" : "Name",
            "image_path" : "Image URL",
            "stock" :"Stock",
            "threshold" : "Threshold",
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['rank', 'username', 'password1', 'password2', 'first_name', 'last_name', 'email']

class VendorForm(BSModalModelForm):

    class Meta:
        model = Vendor
        fields = ["name", "path"]

        labels = {
            "name" : "Vendor Name",
            "path" : "Vendor URL",
        }

class Mock_InventoryForm(BSModalModelForm):
    class Meta:
        model = mock_inventory # Replace with regular inventory when ready.
        fields = ["item", "alert", "name", "image", "amount", "description"] 
        labels = {
            "item" : "Item",
            "alert" : "Alert",
            "name" : "Name ",
            "image" : "Image",
            "amount" : "Amount", 
            "description" : "Description", 
        }    