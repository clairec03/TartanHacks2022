from django.contrib import admin
from main.models import Profile, Encoding
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
      list_display    = ['user', 'id', 'pfp']

class EncodingAdmin(admin.ModelAdmin):
      list_display    = ['user',  'serialized_encoding']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Encoding, EncodingAdmin)