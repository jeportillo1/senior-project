"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import Group
# from django.contrib.auth.models import User

from app.models import global_settings, Item, Vendor
from app.apps import premissionPrep
from django.contrib.auth import get_user_model
User = get_user_model()

class ViewTest(TestCase):
    """Tests for the application views and permissions."""

    @classmethod
    def setUpTestData(cls):
        """
        :return: None
        """
        # Setting up objects which can be use for all test methods

        premissionPrep(None)
        # print("="*100)
        # for x in Group.objects.all():
        #     print(f"group: {x}")
        # print("="*100)

        # setting up an item in inventory and vendor
        itemA = Item(part_number= "PART", title = "item part", image_path = "", stock = 100, threshold = 1)
        itemA.save()
        vendorA = Vendor(name="Vendor A", path="www.amazon.com", itemfk=itemA)
        vendorA.save()

        # setting up users
        view_user = User.objects.create(username='view', rank='Viewer')
        # print(view_user)
        manager_user = User.objects.create(username='mngr', rank='Manager')
        admin_user = User.objects.create(username='admn', rank='Admin')

        view_user.set_password("password")
        manager_user.set_password("password")
        admin_user.set_password("password")

        view_user.save()
        manager_user.save()
        admin_user.save()
       
    def setUp(self):

        # # setting up main settings
        self.main_setting = global_settings.objects.get(id=1)

        # setting up an item in inventory and vendor
        self.itemA = Item.objects.get(title="item part")
        self.vendorA = Vendor.objects.get(itemfk=self.itemA)

        # setting up users
        self.view_user = User.objects.get(username='view')
        self.manager_user = User.objects.get(username='mngr')
        self.admin_user = User.objects.get(username='admn')


    
    def helper(self, name, template, account=None, general_allowed=False, account_allowed=False, is_reverse=True):
        """helper function"""
        # self.assertEqual(self.admin_user.get_user_permissions(), Group.objects.get(name="Admin").permissions.all())
        if is_reverse:
            url_path = reverse(name)
        else:
            url_path = name
        # test non-logged
        # if general allowed then no need to redirect otherwise requrie redirect
        if general_allowed:
            response = self.client.get(url_path)
            self.assertTemplateUsed(response, template)
            self.assertEqual(response.status_code, 200)
        else:
            # test non-logged in users to redirect
            response = self.client.get(url_path, follow=True)
            self.assertRedirects(response, f'/login/?next={url_path}')
            self.assertTemplateUsed(response, 'app/login.html')
            self.assertTemplateNotUsed(response, template)

        # logged in users get access
        if account is not None:
            self.client.login(username=account.username, password="password")
        response = self.client.get(url_path, follow=True)
        if general_allowed or account_allowed:
            self.assertTemplateUsed(response, template)
            self.assertEqual(response.status_code, 200)
        else:
            if account is not None:
                self.assertEqual(response.status_code, 403)
        
        if account is not None:
            # logout
            self.client.logout()


    def test_home(self):
        """Tests the home page."""
        self.helper(name="home", template="app/adminhomepage.html", general_allowed=False)
        self.helper(name="home", template="app/inventory/index.html", account=self.view_user, general_allowed=False, account_allowed=True)
        self.helper(name="home", template="app/inventory/index.html", account=self.manager_user, general_allowed=False, account_allowed=True)
        self.helper(name="home", template="app/adminhomepage.html", account=self.admin_user, general_allowed=False, account_allowed=True)


    def test_about(self):
        """Tests the about page."""
        self.helper(name="about", template="app/about.html", general_allowed=True)
        self.helper(name="about", template="app/about.html", account=self.view_user, general_allowed=True, account_allowed=True)
        self.helper(name="about", template="app/about.html", account=self.manager_user, general_allowed=True, account_allowed=True)
        self.helper(name="about", template="app/about.html", account=self.admin_user, general_allowed=True, account_allowed=True)

    
    def test_admin_settings(self):
        """Tests the home page."""
        self.helper(name="admin_settings", template="app/form_page.html", general_allowed=False)
        self.helper(name="admin_settings", template="app/form_page.html", account=self.view_user, general_allowed=False, account_allowed=False)
        self.helper(name="admin_settings", template="app/form_page.html", account=self.manager_user, general_allowed=False, account_allowed=False)
        self.helper(name="admin_settings", template="app/form_page.html", account=self.admin_user, general_allowed=False, account_allowed=True)


    def test_users(self):
        """Tests the home page."""
        self.helper(name="people_index", template="app/people/index.html", general_allowed=False)
        self.helper(name="people_index", template="app/people/index.html", account=self.view_user, general_allowed=False, account_allowed=False)
        self.helper(name="people_index", template="app/people/index.html", account=self.manager_user, general_allowed=False, account_allowed=False)
        self.helper(name="people_index", template="app/people/index.html", account=self.admin_user, general_allowed=False, account_allowed=True)


    def test_history(self):
        """Tests the home page."""
        self.helper(name="history", template="app/history.html", general_allowed=False)
        self.helper(name="history", template="app/history.html", account=self.view_user, general_allowed=False, account_allowed=True)
        self.helper(name="history", template="app/history.html", account=self.manager_user, general_allowed=False, account_allowed=True)
        self.helper(name="history", template="app/history.html", account=self.admin_user, general_allowed=False, account_allowed=True)


    def test_inventory(self):
        """Tests the inventory page."""
        self.helper(name="inventory_index", template="app/inventory/index.html", general_allowed=False)
        self.helper(name="inventory_index", template="app/inventory/index.html", account=self.view_user, general_allowed=False, account_allowed=True)
        self.helper(name="inventory_index", template="app/inventory/index.html", account=self.manager_user, general_allowed=False, account_allowed=True)
        self.helper(name="inventory_index", template="app/inventory/index.html", account=self.admin_user, general_allowed=False, account_allowed=True)

    def test_inventory_add_edit_disabled(self):
        """Tests the create button in inventory page."""
        # disallowed to change inventory
        # self.main_setting = global_settings(None, instance=self.main_setting)
        self.main_setting.allow_inventory_changes = False
        self.main_setting.save()
        
        self.helper(name="create_item", template="app/inventory/popups/create_item.html", general_allowed=False)
        self.helper(name="create_item", template="app/inventory/popups/create_item.html", account=self.view_user, general_allowed=False, account_allowed=False)
        self.helper(name="create_item", template="app/inventory/popups/create_item.html", account=self.manager_user, general_allowed=False, account_allowed=False)
        self.helper(name="create_item", template="app/inventory/popups/create_item.html", account=self.admin_user, general_allowed=False, account_allowed=False)


    def test_inventory_add_edit_enabled(self):
        """Tests the create button in inventory page."""
        # allowed to change inventory
        # self.main_setting = global_settings(None, instance=self.main_setting)
        self.main_setting.allow_inventory_changes = True
        self.main_setting.save()
        
        self.helper(name="create_item", template="app/inventory/popups/create_item.html", general_allowed=False)
        self.helper(name="create_item", template="app/inventory/popups/create_item.html", account=self.view_user, general_allowed=False, account_allowed=False)
        self.helper(name="create_item", template="app/inventory/popups/create_item.html", account=self.manager_user, general_allowed=False, account_allowed=True)
        self.helper(name="create_item", template="app/inventory/popups/create_item.html", account=self.admin_user, general_allowed=False, account_allowed=True)


    def test_inventory_update_edit_disabled(self):
        """Tests the update button in inventory page."""
        # disallowed to change inventory
        # self.main_setting = global_settings(None, instance=self.main_setting)
        self.main_setting.allow_inventory_changes = False
        self.main_setting.save()
        
        self.helper(name=reverse("update_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/update_item.html", general_allowed=False, is_reverse=False)
        self.helper(name=reverse("update_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/update_item.html", account=self.view_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("update_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/update_item.html", account=self.manager_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("update_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/update_item.html", account=self.admin_user, general_allowed=False, account_allowed=False, is_reverse=False)


    def test_inventory_update_edit_enabled(self):
        """Tests the update button in inventory page."""
        # allowed to change inventory
        # self.main_setting = global_settings(None, instance=self.main_setting)
        self.main_setting.allow_inventory_changes = True
        self.main_setting.save()
        
        # inventory/update_item/<int:pk>
        self.helper(name=reverse("update_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/update_item.html", general_allowed=False, is_reverse=False)
        self.helper(name=reverse("update_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/update_item.html", account=self.view_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("update_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/update_item.html", account=self.manager_user, general_allowed=False, account_allowed=True, is_reverse=False)
        self.helper(name=reverse("update_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/update_item.html", account=self.admin_user, general_allowed=False, account_allowed=True, is_reverse=False)


    def test_inventory_view_edit_disabled(self):
        """Tests the view button in inventory page."""
        # disallowed to change inventory
        # self.main_setting = global_settings(None, instance=self.main_setting)
        self.main_setting.allow_inventory_changes = False
        self.main_setting.save()
        
        self.helper(name=reverse("read_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/read_item.html", general_allowed=False, is_reverse=False)
        self.helper(name=reverse("read_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/read_item.html", account=self.view_user, general_allowed=False, account_allowed=True, is_reverse=False)
        self.helper(name=reverse("read_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/read_item.html", account=self.manager_user, general_allowed=False, account_allowed=True, is_reverse=False)
        self.helper(name=reverse("read_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/read_item.html", account=self.admin_user, general_allowed=False, account_allowed=True, is_reverse=False)


    def test_inventory_view_edit_enabled(self):
        """Tests the view button in inventory page."""
        # disallowed to change inventory
        # self.main_setting = global_settings(None, instance=self.main_setting)
        self.main_setting.allow_inventory_changes = True
        self.main_setting.save()
        
        # inventory/read_item/<int:pk>
        self.helper(name=reverse("read_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/read_item.html", general_allowed=False, is_reverse=False)
        self.helper(name=reverse("read_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/read_item.html", account=self.view_user, general_allowed=False, account_allowed=True, is_reverse=False)
        self.helper(name=reverse("read_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/read_item.html", account=self.manager_user, general_allowed=False, account_allowed=True, is_reverse=False)
        self.helper(name=reverse("read_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/read_item.html", account=self.admin_user, general_allowed=False, account_allowed=True, is_reverse=False)


    def test_inventory_remove_edit_disabled(self):
        """Tests the remove button in inventory page."""
        # allowed to change inventory
        # self.main_setting = global_settings(None, instance=self.main_setting)
        self.main_setting.allow_inventory_changes = False
        self.main_setting.save()
        
        self.helper(name=reverse("delete_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/delete_item.html", general_allowed=False, is_reverse=False)
        self.helper(name=reverse("delete_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/delete_item.html", account=self.view_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("delete_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/delete_item.html", account=self.manager_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("delete_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/delete_item.html", account=self.admin_user, general_allowed=False, account_allowed=False, is_reverse=False)


    def test_inventory_remove_edit_enabled(self):
        """Tests the remove button in inventory page."""
        # allowed to change inventory
        # self.main_setting = global_settings(None, instance=self.main_setting)
        self.main_setting.allow_inventory_changes = True
        self.main_setting.save()
        
        # inventory/delete_item/<int:pk>
        self.helper(name=reverse("delete_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/delete_item.html", general_allowed=False, is_reverse=False)
        self.helper(name=reverse("delete_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/delete_item.html", account=self.view_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("delete_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/delete_item.html", account=self.manager_user, general_allowed=False, account_allowed=True, is_reverse=False)
        self.helper(name=reverse("delete_item", kwargs={'pk': self.itemA.id}), template="app/inventory/popups/delete_item.html", account=self.admin_user, general_allowed=False, account_allowed=True, is_reverse=False)


    def test_inventory_vendor_purchase_disabled(self):
        """Tests the view button in inventory page."""
        # disallowed to purchase
        # self.main_setting = global_settings(None, instance=self.main_setting)
        self.main_setting.allow_inventory_purchases = False
        self.main_setting.save()
        
        self.helper(name=reverse("VendorList", kwargs={'item': self.itemA.id}), template="app/vendors/index.html", general_allowed=False, is_reverse=False)
        self.helper(name=reverse("VendorList", kwargs={'item': self.itemA.id}), template="app/vendors/index.html", account=self.view_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("VendorList", kwargs={'item': self.itemA.id}), template="app/vendors/index.html", account=self.manager_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("VendorList", kwargs={'item': self.itemA.id}), template="app/vendors/index.html", account=self.admin_user, general_allowed=False, account_allowed=False, is_reverse=False)


    def test_inventory_vendor_purchase_enabled(self):
        """Tests the view button in inventory page."""
        # allowed to purchase
        # self.main_setting = global_settings(None, instance=self.main_setting)
        self.main_setting.allow_inventory_purchases = True
        self.main_setting.save()
        
        # vendors/<int:item>/
        self.helper(name=reverse("VendorList", kwargs={'item': self.itemA.id}), template="app/vendors/index.html", general_allowed=False, is_reverse=False)
        self.helper(name=reverse("VendorList", kwargs={'item': self.itemA.id}), template="app/vendors/index.html", account=self.view_user, general_allowed=False, account_allowed=True, is_reverse=False)
        self.helper(name=reverse("VendorList", kwargs={'item': self.itemA.id}), template="app/vendors/index.html", account=self.manager_user, general_allowed=False, account_allowed=True, is_reverse=False)
        self.helper(name=reverse("VendorList", kwargs={'item': self.itemA.id}), template="app/vendors/index.html", account=self.admin_user, general_allowed=False, account_allowed=True, is_reverse=False)


    def test_inventory_vendor_add_changes_disabled(self):
        """Tests the add button in vendor page."""
        # disallowed to change
        # self.main_setting = global_settings(None, instance=self.main_setting)
        self.main_setting.allow_inventory_changes = False
        self.main_setting.save()
        
        self.helper(name=reverse("create_vendor", kwargs={'item': self.itemA.id}), template="app/vendors/popups/create_vendor.html", general_allowed=False, is_reverse=False)
        self.helper(name=reverse("create_vendor", kwargs={'item': self.itemA.id}), template="app/vendors/popups/create_vendor.html", account=self.view_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("create_vendor", kwargs={'item': self.itemA.id}), template="app/vendors/popups/create_vendor.html", account=self.manager_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("create_vendor", kwargs={'item': self.itemA.id}), template="app/vendors/popups/create_vendor.html", account=self.admin_user, general_allowed=False, account_allowed=False, is_reverse=False)


    def test_inventory_vendor_add_changes_enabled(self):
        """Tests the add button in vendor page."""
        # allowed to change
        # self.main_setting = global_settings(None, instance=self.main_setting)
        self.main_setting.allow_inventory_changes = True
        self.main_setting.save()
        
        # vendors/<int:item>/create_item/
        self.helper(name=reverse("create_vendor", kwargs={'item': self.itemA.id}), template="app/vendors/popups/create_vendor.html", general_allowed=False, is_reverse=False)
        self.helper(name=reverse("create_vendor", kwargs={'item': self.itemA.id}), template="app/vendors/popups/create_vendor.html", account=self.view_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("create_vendor", kwargs={'item': self.itemA.id}), template="app/vendors/popups/create_vendor.html", account=self.manager_user, general_allowed=False, account_allowed=True, is_reverse=False)
        self.helper(name=reverse("create_vendor", kwargs={'item': self.itemA.id}), template="app/vendors/popups/create_vendor.html", account=self.admin_user, general_allowed=False, account_allowed=True, is_reverse=False)


    def test_inventory_vendor_update_changes_disabled(self):
        """ Tests the update button in vendor page."""
        # disallowed to change
        # self.main_setting = global_settings(None, instance=self.main_setting)
        self.main_setting.allow_inventory_changes = False
        self.main_setting.save()
        
        self.helper(name=reverse("update_vendor", kwargs={'item': self.itemA.id, 'pk':self.vendorA.id}), template="app/vendors/popups/update_vendor.html", general_allowed=False, is_reverse=False)
        self.helper(name=reverse("update_vendor", kwargs={'item': self.itemA.id, 'pk':self.vendorA.id}), template="app/vendors/popups/update_vendor.html", account=self.view_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("update_vendor", kwargs={'item': self.itemA.id, 'pk':self.vendorA.id}), template="app/vendors/popups/update_vendor.html", account=self.manager_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("update_vendor", kwargs={'item': self.itemA.id, 'pk':self.vendorA.id}), template="app/vendors/popups/update_vendor.html", account=self.admin_user, general_allowed=False, account_allowed=False, is_reverse=False)


    def test_inventory_vendor_update_changes_enabled(self):
        """Tests the update button in vendor page."""
        # allowed to change
        # self.main_setting = global_settings(None, instance=self.main_setting)
        self.main_setting.allow_inventory_changes = True
        self.main_setting.save()
        
        # vendors/<int:item>/update_item/<int:pk>/
        self.helper(name=reverse("update_vendor", kwargs={'item': self.itemA.id, 'pk':self.vendorA.id}), template="app/vendors/popups/update_vendor.html", general_allowed=False, is_reverse=False)
        self.helper(name=reverse("update_vendor", kwargs={'item': self.itemA.id, 'pk':self.vendorA.id}), template="app/vendors/popups/update_vendor.html", account=self.view_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("update_vendor", kwargs={'item': self.itemA.id, 'pk':self.vendorA.id}), template="app/vendors/popups/update_vendor.html", account=self.manager_user, general_allowed=False, account_allowed=True, is_reverse=False)
        self.helper(name=reverse("update_vendor", kwargs={'item': self.itemA.id, 'pk':self.vendorA.id}), template="app/vendors/popups/update_vendor.html", account=self.admin_user, general_allowed=False, account_allowed=True, is_reverse=False)


    def test_inventory_vendor_delete_changes_disabled(self):
        """ Tests the delete button in vendor page."""
        # disallowed to change
        # self.main_setting = global_settings(None, instance=self.main_setting)
        self.main_setting.allow_inventory_changes = False
        self.main_setting.save()
        
        self.helper(name=reverse("delete_vendor", kwargs={'item': self.itemA.id, 'pk':self.vendorA.id}), template="app/vendors/popups/delete_vendor.html", general_allowed=False, is_reverse=False)
        self.helper(name=reverse("delete_vendor", kwargs={'item': self.itemA.id, 'pk':self.vendorA.id}), template="app/vendors/popups/delete_vendor.html", account=self.view_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("delete_vendor", kwargs={'item': self.itemA.id, 'pk':self.vendorA.id}), template="app/vendors/popups/delete_vendor.html", account=self.manager_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("delete_vendor", kwargs={'item': self.itemA.id, 'pk':self.vendorA.id}), template="app/vendors/popups/delete_vendor.html", account=self.admin_user, general_allowed=False, account_allowed=False, is_reverse=False)


    def test_inventory_vendor_delete_changes_enabled(self):
        """Tests the delete button in vendor page."""
        # allowed to change
        # self.main_setting = global_settings(None, instance=self.main_setting)
        self.main_setting.allow_inventory_changes = True
        self.main_setting.save()
        
        # vendors/<int:item>/delete_item/<int:pk>/
        self.helper(name=reverse("delete_vendor", kwargs={'item': self.itemA.id, 'pk':self.vendorA.id}), template="app/vendors/popups/delete_vendor.html", general_allowed=False, is_reverse=False)
        self.helper(name=reverse("delete_vendor", kwargs={'item': self.itemA.id, 'pk':self.vendorA.id}), template="app/vendors/popups/delete_vendor.html", account=self.view_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("delete_vendor", kwargs={'item': self.itemA.id, 'pk':self.vendorA.id}), template="app/vendors/popups/delete_vendor.html", account=self.manager_user, general_allowed=False, account_allowed=True, is_reverse=False)
        self.helper(name=reverse("delete_vendor", kwargs={'item': self.itemA.id, 'pk':self.vendorA.id}), template="app/vendors/popups/delete_vendor.html", account=self.admin_user, general_allowed=False, account_allowed=True, is_reverse=False)


    def test_profile(self):
        """Tests the profile page."""
        self.helper(name="profile", template="app/user/profile.html", general_allowed=False)
        self.helper(name="profile", template="app/user/profile.html", account=self.view_user, general_allowed=False, account_allowed=True)
        self.helper(name="profile", template="app/user/profile.html", account=self.manager_user, general_allowed=False, account_allowed=True)
        self.helper(name="profile", template="app/user/profile.html", account=self.admin_user, general_allowed=False, account_allowed=True)
        

    def test_change_password(self):
        """Tests the change password page."""
        self.helper(name="change_password", template="app/user/change_password.html", general_allowed=False)
        self.helper(name="change_password", template="app/user/change_password.html", account=self.view_user, general_allowed=False, account_allowed=True)
        self.helper(name="change_password", template="app/user/change_password.html", account=self.manager_user, general_allowed=False, account_allowed=True)
        self.helper(name="change_password", template="app/user/change_password.html", account=self.admin_user, general_allowed=False, account_allowed=True)
        
    
    def test_user_settings(self):
        """Tests the user settings page."""
        self.helper(name="user_settings", template="app/form_page.html", general_allowed=False)
        self.helper(name="user_settings", template="app/form_page.html", account=self.view_user, general_allowed=False, account_allowed=True)
        self.helper(name="user_settings", template="app/form_page.html", account=self.manager_user, general_allowed=False, account_allowed=True)
        self.helper(name="user_settings", template="app/form_page.html", account=self.admin_user, general_allowed=False, account_allowed=True)
        

    def test_people_index(self):
        """ Tests the users page."""
        self.helper(name="people_index", template="app/people/index.html", general_allowed=False)
        self.helper(name="people_index", template="app/people/index.html", account=self.view_user, general_allowed=False, account_allowed=False)
        self.helper(name="people_index", template="app/people/index.html", account=self.manager_user, general_allowed=False, account_allowed=False)
        self.helper(name="people_index", template="app/people/index.html", account=self.admin_user, general_allowed=False, account_allowed=True)
    
    def test_people_add_user_with_enabled(self):
        """ Tests the add button in users page."""
        # self.main_setting = global_settings(None, instance=self.main_setting)
        self.main_setting.allow_adding_new_users = True
        self.main_setting.save()

        self.helper(name=reverse("signup"), template="app/accounts/register.html", general_allowed=False, is_reverse=False)
        self.helper(name=reverse("signup"), template="app/accounts/register.html", account=self.view_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("signup"), template="app/accounts/register.html", account=self.manager_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("signup"), template="app/accounts/register.html", account=self.admin_user, general_allowed=False, account_allowed=True, is_reverse=False)

    def test_people_add_user_with_disabled(self):
        """ Tests the add button in users page."""
        # self.main_setting = global_settings(None, instance=self.main_setting)
        self.main_setting.allow_adding_new_users = False
        self.main_setting.save()

        self.helper(name=reverse("signup"), template="app/accounts/register.html", general_allowed=False, is_reverse=False)
        self.helper(name=reverse("signup"), template="app/accounts/register.html", account=self.view_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("signup"), template="app/accounts/register.html", account=self.manager_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("signup"), template="app/accounts/register.html", account=self.admin_user, general_allowed=False, account_allowed=False, is_reverse=False)

        # self.helper(name="accounts/register/", template="app/accounts/register.html", general_allowed=False, is_reverse=False)
        # self.helper(name="accounts/register/", template="app/accounts/register.html", account=self.view_user, general_allowed=False, account_allowed=False)
        # self.helper(name="accounts/register/", template="app/accounts/register.html", account=self.manager_user, general_allowed=False, account_allowed=False)
        # self.helper(name="accounts/register/", template="app/accounts/register.html", account=self.admin_user, general_allowed=False, account_allowed=False)

    def test_users_delete(self):
        """ Tests the delete button in users page."""
        # users/delete_user/<int:pk>
        self.helper(name=reverse("delete_user", kwargs={'pk':self.view_user.id}), template="app/people/popups/delete_user.html", general_allowed=False, is_reverse=False)
        self.helper(name=reverse("delete_user", kwargs={'pk':self.view_user.id}), template="app/people/popups/delete_user.html", account=self.view_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("delete_user", kwargs={'pk':self.view_user.id}), template="app/people/popups/delete_user.html", account=self.manager_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("delete_user", kwargs={'pk':self.view_user.id}), template="app/people/popups/delete_user.html", account=self.admin_user, general_allowed=False, account_allowed=True, is_reverse=False)

    def test_users_update(self):
        """ Tests the update button in users page."""
        # users/update_user/<int:pk>
        self.helper(name=reverse("update_user", kwargs={'pk':self.view_user.id}), template="app/people/popups/update_user.html", general_allowed=False, is_reverse=False)
        self.helper(name=reverse("update_user", kwargs={'pk':self.view_user.id}), template="app/people/popups/update_user.html", account=self.view_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("update_user", kwargs={'pk':self.view_user.id}), template="app/people/popups/update_user.html", account=self.manager_user, general_allowed=False, account_allowed=False, is_reverse=False)
        self.helper(name=reverse("update_user", kwargs={'pk':self.view_user.id}), template="app/people/popups/update_user.html", account=self.admin_user, general_allowed=False, account_allowed=True, is_reverse=False)
