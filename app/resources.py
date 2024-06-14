from import_export import resources
from .models import mock_inventory

class UploadResource(resources.ModelResource):
    class Meta:
        model = mock_inventory