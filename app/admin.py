from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import mock_inventory
from .models import * # noqa: F401
@admin.register(mock_inventory)
class UploadAdmin(ImportExportModelAdmin):
    pass