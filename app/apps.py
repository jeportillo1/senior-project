# configure for app
# https://docs.djangoproject.com/en/4.0/ref/applications/

from django.apps import AppConfig
from django.db.models.signals import post_migrate

def createGlobal(sender, **kwargs):
    """ create global settings if there isn't one"""
    from app.models import global_settings

    if not global_settings.objects.exists():
        admin_settings_form = global_settings(None)
        admin_settings_form.save()


def premissionPrep(sender, **kwargs):
    """ adds permissions to groups """
    from django.contrib.auth.models import Group, Permission
    if not Permission.objects.exists():
        return
    Agroup, Acreated = Group.objects.get_or_create(name='Admin')
    Mgroup, Mcreated = Group.objects.get_or_create(name='Manager')
    Vgroup, Vcreated = Group.objects.get_or_create(name='Viewer')

    app_user_can_add_user = Permission.objects.get(codename='add_customuser')
    app_user_can_change_user = Permission.objects.get(codename='change_customuser')
    app_user_can_delete_user = Permission.objects.get(codename='delete_customuser')
    app_user_can_view_user = Permission.objects.get(codename='view_customuser')

    app_user_can_view_history = Permission.objects.get(codename='view_history')
    app_user_can_add_history = Permission.objects.get(codename='add_history')
    app_user_can_delete_history = Permission.objects.get(codename='delete_history')
    app_user_can_change_history = Permission.objects.get(codename='change_history')

    app_global_settings_can_change_global_settings = Permission.objects.get(name='Can change global_settings')
    app_global_settings_can_view_global_settings = Permission.objects.get(name='Can view global_settings')

    app_item_can_add_item = Permission.objects.get(name='Can add item')
    app_item_can_change_item = Permission.objects.get(name='Can change item')
    app_item_can_delete_item = Permission.objects.get(name='Can delete item')
    app_item_can_view_item = Permission.objects.get(name='Can view item')

    app_vendor_can_add_vendor = Permission.objects.get(name='Can add vendor')
    app_vendor_can_change_vendor = Permission.objects.get(name='Can change vendor')
    app_vendor_can_delete_vendor = Permission.objects.get(name='Can delete vendor')
    app_vendor_can_view_vendor = Permission.objects.get(name='Can view vendor')

    AdminPermissions = [
        app_user_can_view_history, app_user_can_add_history, app_user_can_delete_history, app_user_can_change_history,
        app_user_can_add_user, app_user_can_change_user, app_user_can_delete_user, app_user_can_view_user,
        app_global_settings_can_change_global_settings, app_global_settings_can_view_global_settings,
        app_item_can_add_item, app_item_can_delete_item, app_item_can_view_item, app_item_can_change_item,
        app_vendor_can_add_vendor, app_vendor_can_change_vendor, app_vendor_can_delete_vendor, app_vendor_can_view_vendor
    ]

    ManagerPermissions = [
        app_item_can_add_item, app_item_can_delete_item, app_item_can_view_item, app_item_can_change_item,
        app_vendor_can_add_vendor, app_vendor_can_change_vendor, app_vendor_can_delete_vendor, app_vendor_can_view_vendor
    ]

    ViewerPermissions = [
        app_item_can_view_item,
        app_vendor_can_view_vendor
    ]

    if Acreated:
        for p in AdminPermissions:
            Agroup.permissions.add(p)

    if Mcreated:
        for p in ManagerPermissions:
            Mgroup.permissions.add(p)

    if Vcreated:
        for p in ViewerPermissions:
            Vgroup.permissions.add(p)

class MyAppConfig(AppConfig):
    """config for app"""
    name = 'app'
    verbose_name = "My Application"

    def ready(self):
        post_migrate.connect(createGlobal, sender=self)
        post_migrate.connect(premissionPrep, sender=self)
        