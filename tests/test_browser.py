"""
    Unit Test file for views
"""
from django.test import TestCase

from selenium import webdriver

from setup.settings.development_settings import SITE_URL


class TaskListViewTest(TestCase):
    """
    Test View class
    """
    # # Browser Integration testing with Selenium
    def test_chrome_site_homepage(self):
        browser = webdriver.Chrome()
        browser.get(SITE_URL)
        self.assertIn('Semaphore', browser.title)
        browser.close()