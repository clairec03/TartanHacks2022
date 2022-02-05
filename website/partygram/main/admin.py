from django.contrib import admin
from main.models import Profile
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
      list_display    = ['user', 'id', 'pfp']

admin.site.register(Profile, ProfileAdmin)
