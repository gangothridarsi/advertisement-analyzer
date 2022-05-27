from django.contrib import admin
from advapp import models

# Register your models here.
admin.site.register(models.Advertisement)
admin.site.register(models.User)
admin.site.register(models.UserResults)