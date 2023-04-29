from django.contrib import admin
from .models import Subdomain, Domain

# Register your models here.
admin.site.site_title = "SubManage"  # Custom site title
admin.site.site_header = "Subdomain Manager"  # Custom site header
admin.site.index_title = "Subdomain Manager"  # Custom index title

admin.site.register(Subdomain)
admin.site.register(Domain)
