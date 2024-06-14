"""
Definition of models.
"""

# from xmlrpc.client import DateTime
# from django import db
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser # , User
# from django_boost.models.fields import AutoOneToOneField
from django.utils.timezone import now
from annoying.fields import AutoOneToOneField
from django.contrib.auth.models import Group

# Create your models here.
# created a table for admin settings
# print(now())

RANK_CHOICES = (
    ('Admin', 'Admin'),
    ('Manager', 'Manager'),
    ('Viewer', 'Viewer'),
)
RANK_GROUPS = ["Admin", "Manager", "Viewer"]
class CustomUser(AbstractUser):
    rank = models.CharField(max_length=10,choices=RANK_CHOICES,default="Viewer")

    def save(self, *args, **kwargs):
        # remove user from rank groups
        query_set = Group.objects.filter(user = self.pk)
        for g in query_set:
            if g.name in RANK_GROUPS:
                g.user_set.remove(self)
                # self.user.groups.remove(group)

        # assign user to new rank group
        if self.rank == "Admin":
            group, created = Group.objects.get_or_create(name='Admin')
        elif self.rank == "Manager":
            group, created = Group.objects.get_or_create(name='Manager')
        elif self.rank == "Viewer":
            group, created = Group.objects.get_or_create(name='Viewer')
        group.user_set.add(self.pk)
        super(CustomUser, self).save(*args, **kwargs)



User = get_user_model()

class recent_alerts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=45)
    
    class Meta:

        db_table="recent_alerts"

#new history page
class recent_new_user(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    descrption = models.CharField(max_length=250)
    created_date = models.DateTimeField(default=now, editable=False)

    class Meta:
        
        db_table="recent_new_user"

class recent_new_item(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    description = models.CharField(max_length=45)
    newItem = models.CharField(max_length=45)

    class Meta:

        db_table = "recent_new_item"

# Mockup purchase history db. Inactive, need to create db in Heroku. -Thomas
class purchase_history(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    descrption = models.CharField(max_length=45)
    # add time attribute to this and other audit logs?

    class Meta:

        db_table="purchase_history"

# Mockup inventory changes db. Inactive, need to create db in Heroku. -Thomas
class inventory_changes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    descrption = models.CharField(max_length=45)
    # add time attribute to this and other audit logs?

    class Meta:

        db_table="inventory_changes"

class history(models.Model):
    id = models.IntegerField(primary_key= True)
    description = models.CharField(max_length=100)
    time = models.DateField()

    class Meta:
        db_table = "history"
       

# for settings, left is value right is appearance
FONT_CHOICES = (
    ('Arial', 'Arial'),
    ('Courier New', 'Courier'),
    ('Times New Roman', 'Times New Roman'),
    ('Verdana', 'Verdana'),
)
PAGINATE_BY_CHOICES = (
    (5, '5'),
    (10, '10'),
    (15, '15'),
    (25, '25'),
    (50, '50'),
    (100, '100'),
    (0, 'All')
)
class personal_user_settings(models.Model):
    user = AutoOneToOneField(to=User, on_delete=models.CASCADE, primary_key=True, related_name="user_profile")
    font_type = models.CharField(max_length=20, choices=FONT_CHOICES, default='Arial')
    paging_by = models.PositiveSmallIntegerField(choices=PAGINATE_BY_CHOICES, default=10)

    class Meta:
        db_table = "personal_user_settings"

class global_settings(models.Model):

    allow_inventory_changes = models.BooleanField(default=False)
    allow_adding_new_users = models.BooleanField(default=False)
    allow_inventory_purchases = models.BooleanField(default=False)
    allow_paring_data = models.BooleanField(default=False)

    class Meta:
        db_table = "global_settings"

class Item(models.Model):

    title = models.CharField(max_length=50)
    alert = models.BooleanField(default = True)
    image_path = models.CharField(max_length = 500, blank=True)
    stock = models.PositiveIntegerField(default=0)
    threshold = models.PositiveIntegerField(default=1)
    part_number = models.CharField(max_length = 15, blank=True)

    def save(self, *args, **kwargs):
        if self.stock > self.threshold:
            self.alert = False
        else:
            self.alert = True
        super(Item, self).save(*args, **kwargs)


class Vendor(models.Model):
    path = models.URLField(max_length=500)   
    name = models.CharField(max_length=100)
    itemfk = models.ForeignKey(Item, unique=False, on_delete=models.CASCADE)
    
# Temporary, deprecates when File Upload is ready.
class mock_inventory(models.Model):
    item = models.IntegerField(primary_key = True)
    alert = models.BooleanField(default = True)
    name = models.CharField(max_length = 100)
    image = models.CharField(max_length = 500)
    amount = models.IntegerField()
    description = models.CharField(max_length = 500)

    class Meta:
        db_table = "mock_inventory"