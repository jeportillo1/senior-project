"""
Definition of views.

This holds methods that returns how a page is supposed to look like
"""
import warnings
warnings.filterwarnings(action="ignore", message=".*DeleteView*.")

from datetime import datetime
# from http.client import FORBIDDEN
# from urllib import request
# from aiohttp import request
# from django.db import connection
# from django.db.models import Q, ExpressionWrapper, BooleanField
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
# from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.admin.views.decorators import staff_member_required # noqa: F401
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm # noqa: F401
# from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from tablib import Dataset

# from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .resources import UploadResource
# import urllib.parse
from app.static.utils.queries import ItemQuery 

from .forms import (
    CustomUserCreationForm,
    UserSettingsForm, 
    GlobalSettingsForm, 
    # InventoryForm,
    # PersonForm,
    profileForm,
    UserForm,
    ItemForm,
    VendorForm
)

from .models import ( 
    # People,
    # admin_settings as admin_settings_model, 
    inventory_changes, purchase_history,
    # user_settings as user_settings_model,
    recent_alerts as recent_alerts_model,
    recent_new_user as recent_new_user_model,
    # inventory as inventory_model,
    # person as person_model,
    personal_user_settings as personal_user_settings_model,
    global_settings as global_settings_model,
    recent_new_item as recent_new_item_model,
    history as history_model,
    Item,
    Vendor
)

from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)

from django.contrib.auth import get_user_model

User = get_user_model()

# from DjangoWebProject1.DjangoWebProject1.settings import DATABASES

# handles custom error pages
# note: needs (request, exception) for newer versions of django
# currently running older version so using (request) only
def error_handler_404(request):
    return render(request, "app/errors/404.html", {})
def error_handler_500(request):
    return render(request, "app/errors/500.html", {})

@login_required(login_url='login')
@permission_required('app.add_customuser', raise_exception=True)
def register_view(request):
    if not global_settings_model.objects.get(pk=1).allow_adding_new_users:
        raise PermissionDenied
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse_lazy('people_index'))
    context = {"form": form, 'year':datetime.now().year}
    return render(request, "app/accounts/register.html", context)


# this is admin home
# login required
# TODO: possibly separate admin homepage from regular homepage
@login_required(login_url='login')
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    if not request.user.has_perm("app.view_history"):
        return redirect('inventory_index')
    # File Upload - WIP
    if request.method == 'POST':
        up_resource = UploadResource()
        dataset = Dataset()
        new_uploads = request.FILES['myfile']

        imported_data = dataset.load(new_uploads.read())
        result = up_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            up_resource.import_data(dataset, dry_run=False)  # Actually import now
    return render(
        request,
        'app/adminhomepage.html',
        {
            'newitem' : recent_new_item_model.objects.all(),
            'usersettings' : personal_user_settings_model.objects.all().filter(user_id=request.user.id),
            # 'newuser' : recent_new_user_model.objects.all(),
            'history' : recent_new_user_model.objects.all().order_by("-created_date"),
            'title':'Admin Home Page', # this passes in info and html page can use {{ title }}
            'year':datetime.now().year,
        }
    )


# this is page to view history of events
# TODO : make functional
# login required
@login_required(login_url='login')
def history(request):
    """Renders the history page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/history.html',
        {
            # 'purchases' : purchase_history.objects.all(), Inactive, need to create db in Heroku.
            # 'inventory' : inventory_changes.objects.all(), Inactive, need to create db in Heroku.
            # 'newuser' : recent_new_user_model.objects.all(),
            'history': recent_new_user_model.objects.all().order_by("-created_date"),
            'title':'History',
            'year':datetime.now().year,
        }
    )

# this is page to view all the people
# TODO : make functional
# login required
@login_required(login_url='login')
def people(request):
    """Renders the people page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/people.html',
        {
            'title':'People',
            'year':datetime.now().year,
        }
    )


# this is page to change settings
# login required
@login_required(login_url='login')
def user_settings(request):
    """Renders the settings page for user"""

    # get form for the user requesting page
    # current_user_settings_isinstance = personal_user_settings_model.objects.get(user_id=request.user.id)
    current_user_settings_isinstance = request.user.user_profile
    user_form = UserSettingsForm(request.POST or None, instance=current_user_settings_isinstance)

    # if form is submitted
    if request.method == "POST":
        if request.POST.get("revert"):
            # if revert button pressed creates a new form (which prefils with default values)
            user_form = UserSettingsForm(None)

            # ties default form to user id
            # user_form then gets only displayed to user with default values
            user_form.user = request.user.id
        else:
            # saves info on what happened
            a = recent_new_user_model(user_id = request.user.id, descrption = request.user.username + " changed settings") 
            a.save()    

            if user_form.is_valid():
                user_form.save()
    
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/form_page.html',
        {
            'title': 'User Settings',
            'form' : user_form,
            'year': datetime.now().year,
        }
    )

# this is page to change settings
# login required
@login_required(login_url='login')
@permission_required('app.change_global_settings', raise_exception=True)
def admin_settings(request):
    """Renders the settings page."""
    # current global settings are in row with id=1
    admin_settings_form = GlobalSettingsForm(request.POST or None, instance=global_settings_model.objects.get(id=1))

    # if form is submitted
    if request.method == "POST":
        a = recent_new_user_model(user_id = request.user.id, descrption = request.user.username + " has changed admin settings") 
        a.save()
        if admin_settings_form.is_valid():
            admin_settings_form.save()
            admin_settings_form = GlobalSettingsForm(request.POST, instance=global_settings_model.objects.get(id=1))

    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/form_page.html',
        {
            'title': 'Admin Settings',
            'form' : admin_settings_form,
            'year': datetime.now().year,
        }
    )

# This is a page to view an page about the company (can include stuff like mission statement)
# left it as login not required
# TODO : add real info into the html file for about
def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'This is an inventory management page for ACR Solar',
            'year':datetime.now().year,
        }
    )

@login_required(login_url='login')
def new_user(request):
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        a = recent_new_user_model(user_id = request.user.id, descrption = request.user.username + " new user") 
        a.save()


    return render(
        request,
        'app/adminhomepage.html',{
            'history': recent_new_user_model.objects.all(),
            'year':datetime.now().year,
        }
    )

@login_required(login_url="login")
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        a = recent_new_user_model(user_id = request.user.id, descrption = request.user.username + " change password") 
        a.save()
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('change_password')

    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'app/user/change_password.html', {
        'form': form,
        'title': 'Change Password',
        'year':datetime.now().year,
    })


@login_required(login_url="login")
def profile(request):
    if request.method == "POST": 
        form = profileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('profile')
    else:
        form = profileForm(instance=request.user)

    return render(request, 'app/user/profile.html', {'form': form, 'title':'User Profile', 'year':datetime.now().year,})

class InventoryIndex(generic.ListView):
    """ This is the 'main' view """
    model = Item
    template_name = 'app/inventory/index.html'
    context_object_name = 'items'

    def get_queryset(self):
        self.paginate_by = self.request.user.user_profile.paging_by
        searched = self.request.GET.get('searched')
        searchby = self.request.GET.get('searchby')
        return ItemQuery(searched, searchby, Item)
        

    @method_decorator(login_required(login_url='login'))
    @method_decorator(permission_required('app.view_item', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """ pass in extra context data here """
        context = super().get_context_data(**kwargs)
        context['global_settings'] = global_settings_model.objects.get(pk=1)
        searched = self.request.GET.get('searched')
        searchby = self.request.GET.get('searchby')
        if searched is None or searched == "":
            searched = ""
            searchby = "all" # change to default
            extra = ""
        else:
            extra = f"&searchby={searchby}&searched={searched}"
        context['title'] = "Inventory"
        context['searched'] = searched
        context['searchby'] = searchby
        context['extra'] = extra
        context['year'] = datetime.now().year
        return context




class ItemCreateView(BSModalCreateView):
    """ Create/Add popup """
    template_name = 'app/inventory/popups/create_item.html'
    form_class = ItemForm
    success_message = 'Success: Item was created.'
    success_url = reverse_lazy('inventory_index')
    # def get_success_url(self):
    #     return reverse_lazy("inventory_index", args = (self.kwargs["page"],self.kwargs["searched"],self.kwargs["searchby"]))
    
    @method_decorator(login_required(login_url='login'))
    @method_decorator(permission_required('app.add_item', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        if not global_settings_model.objects.get(pk=1).allow_inventory_changes:
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)


class ItemUpdateView(BSModalUpdateView):
    """ Update popup """
    model = Item
    template_name = 'app/inventory/popups/update_item.html'
    form_class = ItemForm
    success_message = 'Success: Item was updated.'
    success_url = reverse_lazy('inventory_index')

    @method_decorator(login_required(login_url='login'))
    @method_decorator(permission_required('app.change_item', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        if not global_settings_model.objects.get(pk=1).allow_inventory_changes:
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)



class ItemReadView(BSModalReadView):
    """ View/Read popup """
    model = Item
    template_name = 'app/inventory/popups/read_item.html'
    form_class = ItemForm
    success_url = reverse_lazy('inventory_index')

    @method_decorator(login_required(login_url='login'))
    @method_decorator(permission_required('app.view_item', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ItemDeleteView(BSModalDeleteView):
    """ Delete popup """
    model = Item
    template_name = 'app/inventory/popups/delete_item.html'
    success_message = 'Success: Item was deleted.'
    success_url = reverse_lazy('inventory_index')

    @method_decorator(login_required(login_url='login'))
    @method_decorator(permission_required('app.delete_item', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        if not global_settings_model.objects.get(pk=1).allow_inventory_changes:
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)
        

class PeopleIndex(generic.ListView):
    """ This is the 'main' view """
    model = User
    paginate_by = 0 # how many items per page
    template_name = 'app/people/index.html'
    context_object_name = 'persons'
    queryset = User.objects.all().order_by('rank', 'last_name')
    #Person.objects.all()

    @method_decorator(login_required(login_url='login'))
    @method_decorator(permission_required('app.view_customuser', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """ pass in extra context data here """
        context = super().get_context_data(**kwargs)
        context['global_settings'] = global_settings_model.objects.get(pk=1)
        searched = self.request.GET.get('searched')
        searchby = self.request.GET.get('searchby')
        extra = f"&searchby={searchby}&searched={searched}"

        if searched is None or searched == "":
            searched = ""
            searchby = "all" # change to default
            extra = ""
        context['title'] = "Users"
        context['username'] = "People"
        context['searched'] = searched
        context['searchby'] = searchby
        context['extra'] = extra
        context['year'] = datetime.now().year
        return context

class UserUpdateView(BSModalUpdateView):
    """ Update popup """
    model = User
    template_name = 'app/people/popups/update_user.html'
    form_class = UserForm
    success_message = 'Success: User was updated.'
    success_url = reverse_lazy('people_index')

    @method_decorator(login_required(login_url='login'))
    @method_decorator(permission_required('app.change_customuser', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class UserDeleteView(BSModalDeleteView):
    """ Delete popup """
    model = User
    template_name = 'app/people/popups/delete_user.html'
    success_message = 'Success: User was deleted.'
    success_url = reverse_lazy('people_index')

    @method_decorator(login_required(login_url='login'))
    @method_decorator(permission_required('app.delete_customuser', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """ pass in extra context data here """
        context = super().get_context_data(**kwargs)
        user_in_question = User.objects.get(pk=self.kwargs['pk'])
        context['person'] = user_in_question
        return context



@login_required(login_url='login')
@permission_required('app.view_items', raise_exception=True)
def items(request, page=1, searched="", searchby=""):
    data = dict()
    if request.method == 'GET':
        a = recent_new_user_model(user_id = request.user.id, descrption = request.user.username + " acessed inventory") 
        a.save()

        queryset = ItemQuery(searched, searchby, Item)
        
        paginator = Paginator(queryset, request.user.user_profile.paging_by)
        # page = utils.get_page_number_from_request(request)
        page_obj = paginator.get_page(page)
        data['table'] = render_to_string(
            'app/inventory/table.html',
            {
                'items'     : page_obj,
                'global_settings' : global_settings_model.objects.get(pk=1),
                'page' : page,
                'searched' : searched,
                'searchby' : searchby,
            },
            request=request
        )
        return JsonResponse(data)


@login_required(login_url='login')
@permission_required('app.view_customuser', raise_exception=True)
def users_list(request):
    data = dict()
    if request.method == 'GET':
        users_list = User.objects.all().order_by('rank', 'last_name')
        data['table'] = render_to_string(
            'app/people/table.html',
            {'persons': users_list,},
            request=request
        )
        return JsonResponse(data)
         
class ReadVendor(BSModalReadView):
    """ View/Read popup """
    template_name = 'app/inventory/popups/read_vendor.html'
    model = Item
    success_url = reverse_lazy('inventory_index')

    def get_context_data(self, **kwargs):
        """ pass in extra context data here """
        context = super().get_context_data(**kwargs)
        context['Vendors'] = Vendor.objects.filter(itemfk=self.kwargs["pk"])
        context['global_settings'] = global_settings_model.objects.get(pk=1)
        return context

    @method_decorator(login_required(login_url='login'))
    @method_decorator(permission_required('app.view_vendor', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        if not global_settings_model.objects.get(pk=1).allow_inventory_purchases:
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)

class VendorIndex(generic.ListView):
    """ This is the 'main' view """
    model = Vendor
    template_name = 'app/vendors/index.html'
    context_object_name = 'vendors'

    def get_queryset(self):
        return Vendor.objects.filter(itemfk=self.kwargs["item"])
    
    def form_valid(self, form):
        form.instance.itemfk = self.kwargs["item"]
        return super().form_valid(form)
        

    @method_decorator(login_required(login_url='login'))
    @method_decorator(permission_required('app.view_vendor', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        if not global_settings_model.objects.get(pk=1).allow_inventory_purchases:
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """ pass in extra context data here """
        context = super().get_context_data(**kwargs)
        context['itemfk'] = self.kwargs["item"]
        context['global_settings'] = global_settings_model.objects.get(pk=1)
        context['title'] = "Vendor"
        context['year'] = datetime.now().year
        return context

class VendorCreateView(BSModalCreateView):
    """ Create/Add popup """
    template_name = 'app/vendors/popups/create_vendor.html'
    form_class = VendorForm
    success_message = 'Success: Vendor was created.'

    def get_success_url(self):
        return reverse_lazy("VendorList", args = (self.kwargs["item"],))

    @method_decorator(login_required(login_url='login'))
    @method_decorator(permission_required('app.add_vendor', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        if not global_settings_model.objects.get(pk=1).allow_inventory_changes:
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.itemfk = Item.objects.get(pk = self.kwargs["item"])
        return super().form_valid(form)


class VendorUpdateView(BSModalUpdateView):
    """ Update popup """
    model = Vendor
    template_name = 'app/vendors/popups/update_vendor.html'
    form_class = VendorForm
    success_message = 'Success: Vendor was updated.'
    success_url = reverse_lazy('VendorList')

    def get_success_url(self):
        return reverse_lazy("VendorList", args = (self.kwargs["item"],))

    @method_decorator(login_required(login_url='login'))
    @method_decorator(permission_required('app.change_vendor', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        if not global_settings_model.objects.get(pk=1).allow_inventory_changes:
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)

class VendorDeleteView(BSModalDeleteView):
    """ Delete popup """
    model = Vendor
    template_name = 'app/vendors/popups/delete_vendor.html'
    success_message = 'Success: Vendor was deleted.'
    success_url = reverse_lazy('VendorList')

    def get_success_url(self):
        return reverse_lazy("VendorList", args = (self.kwargs["item"],))

    @method_decorator(login_required(login_url='login'))
    @method_decorator(permission_required('app.delete_vendor', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        if not global_settings_model.objects.get(pk=1).allow_inventory_changes:
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)


@login_required(login_url='login')
@permission_required('app.view_vendor', raise_exception=True)
def vendors(request, itemfk):
    if not global_settings_model.objects.get(pk=1).allow_inventory_purchases:
        raise PermissionDenied
    data = dict()
    if request.method == 'GET':

        data['table'] = render_to_string(
            'app/vendors/table.html',
            {
                'vendors'     : Vendor.objects.filter(itemfk = itemfk),
                'itemfk' : itemfk,
                'global_settings' : global_settings_model.objects.get(pk=1),
            },
            request=request
        )
        return JsonResponse(data)