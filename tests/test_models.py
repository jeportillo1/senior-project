"""
    Unit test file for models
"""

# from cgi import test
# from operator import truediv
from tkinter import TRUE
# from unicodedata import name
from django.test import TestCase
from app.forms import CustomUserCreationForm
# from pytz import timezone
from app.models import recent_new_user
# from app.forms import UserCreationForm
# from django.contrib.auth.models import User
from app.models import Item
# from app.models import person
from app.models import global_settings
from django.contrib.auth import get_user_model

User = get_user_model()
class RecentNewUserModelTest(TestCase):
    """
    Test Model class
    """
    @classmethod
    def setUpTestData(cls):
        """
        :return: None
        """
        # Setting up objects which can be use for all test methods

       
    def setUp(self):
        # user = User.objects.create_user(username='john',email='jlennon@beatles.com',
        #                          password='glass onion')
        #user.save();
        # setting up users
        new_user = User.objects.create(username='john', rank='Viewer', email='jlennon@beatles.com')
        new_user.set_password("glass onion")
        new_user.save()

        # self.newUser = User.objects.all()[:1].get()
        self.newUser = new_user.id
        recent_new_user.objects.create(user_id=self.newUser, descrption='This task includes all the development '
                                                                       'related activities for this project')


    def test_user_id_label(self):
        """
        :return: None
        """
        recentUser = recent_new_user.objects.get(user_id=self.newUser)
        field_label = recentUser._meta.get_field('user_id').verbose_name
        self.assertEqual(field_label, 'user')

    def test_description_label(self):
        """
        :return: None
        """
        recentUser = recent_new_user.objects.get(user_id=self.newUser)
        field_label = recentUser._meta.get_field('descrption').verbose_name
        self.assertEqual(field_label, 'descrption')

    def test_description_max_length(self):
        description = recent_new_user.objects.get(user_id=self.newUser)
        max_length = description._meta.get_field('descrption').max_length
        self.assertEqual(max_length, 250)

class AppItemModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        """
        :return: None
        """
        # Setting up objects which can be use for all test method
        Item.objects.create(title='test', image_path = 'testpath', stock = 0, threshold = 0, part_number="1")
    
    def testTitleLabel(self):
        title = Item.objects.get(pk = 1)
        field_label = title._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def testImageLabel(self):
        image = Item.objects.get(pk = 1)
        field_label = image._meta.get_field('image_path').verbose_name
        self.assertEqual(field_label, 'image path')

    def testStockLabel(self):
        stock = Item.objects.get(pk = 1)
        field_label = stock._meta.get_field('stock').verbose_name
        self.assertEqual(field_label, 'stock')

    def testThresholdLabel(self):
        stock = Item.objects.get(pk = 1)
        field_label = stock._meta.get_field('threshold').verbose_name
        self.assertEqual(field_label, 'threshold')

    def testPartNumberLabel(self):
        stock = Item.objects.get(pk = 1)
        field_label = stock._meta.get_field('part_number').verbose_name
        self.assertEqual(field_label, 'part number')

    def test_part_number_max_length(self):
        description = Item.objects.get(pk = 1)
        max_length = description._meta.get_field('part_number').max_length
        self.assertEqual(max_length, 15)

    def test_image_max_length(self):
        image = Item.objects.get(pk = 1)
        max_length = image._meta.get_field('image_path').max_length
        self.assertEqual(max_length, 500)
    
    def test_name_max_length(self):
        name = Item.objects.get(pk = 1)
        max_length = name._meta.get_field('title').max_length
        self.assertEqual(max_length, 50)
    

class PersonTestModel(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        """
        :return: None
        """
        # Setting up objects which can be use for all test method
    
    def setUp(self):
        # user = User.objects.create_user(username='john',email='jlennon@beatles.com',
        #                          password='glass onion')
        #user.save();
        # setting up users
        new_user = User.objects.create(username='john', rank='Viewer', email='jlennon@beatles.com')
        new_user.set_password("glass onion")
        new_user.save()

        # self.newUser = User.objects.all()[:1].get()
        self.newUser = new_user.id
    
    def testUsernameLabel(self):
        username = User.objects.get(id=self.newUser)
        field_label = username._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'username')
    
    def testFirstNameLabel(self):
        first_name = User.objects.get(id=self.newUser)
        field_label = first_name._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')
    
    def testLastNameLabel(self):
        last_name = User.objects.get(id=self.newUser)
        field_label = last_name._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def testEmailLabel(self):
        email = User.objects.get(id=self.newUser)
        field_label = email._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email address')
        
    def test_first_name_max_length(self):
        first_name = User.objects.get(id=self.newUser)
        max_length = first_name._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 150)
    
    def test_last_name_max_length(self):
        last_name = User.objects.get(id=self.newUser)
        max_length = last_name._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 150)
    
    def test_email_max_length(self):
        email = User.objects.get(id=self.newUser)
        max_length = email._meta.get_field('email').max_length
        self.assertEqual(max_length, 254)

    def test_username_max_length(self):
        username = User.objects.get(id=self.newUser)
        max_length = username._meta.get_field('username').max_length
        self.assertEqual(max_length, 150)

class AdminSettingTestModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        :return: None
        """
        # Setting up objects which can be use for all test method
        global_settings.objects.create()

    def test_allow_inventory_changes(self):
        allow_inventory_changes = global_settings.objects.get(id = 1)
        field_label = allow_inventory_changes._meta.get_field('allow_inventory_changes').verbose_name
        self.assertEqual(field_label, 'allow inventory changes')

    def test_allow_adding_new_users_label(self):
        allow_adding_new_users = global_settings.objects.get(id=1)
        field_label = allow_adding_new_users._meta.get_field('allow_adding_new_users').verbose_name
        self.assertEqual(field_label, 'allow adding new users')
    
    def test_allow_inventory_purchases_label(self):
        allow_inventory_purchases = global_settings.objects.get(id=1)
        field_label = allow_inventory_purchases._meta.get_field('allow_inventory_purchases').verbose_name
        self.assertEqual(field_label, 'allow inventory purchases')

    def test_allow_paring_data_label(self):
        allow_paring_data = global_settings.objects.get(id=1)
        field_label = allow_paring_data._meta.get_field('allow_paring_data').verbose_name
        self.assertEqual(field_label, 'allow paring data')

    