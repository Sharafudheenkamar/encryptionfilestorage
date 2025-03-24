from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(LoginTable)
admin.site.register(usertable)
admin.site.register(FileTable)
admin.site.register(SecureFile)
admin.site.register(Rating)