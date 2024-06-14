"""
Package for the application.
"""
default_app_config = 'app.apps.MyAppConfig'
import pymysql

pymysql.install_as_MySQLdb()