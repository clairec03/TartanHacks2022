from django.contrib import admin
from main.models import Profile, Identification, Moment
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
      list_display    = ['user', 'id', 'avatar']

class IdentificationAdmin(admin.ModelAdmin):
      list_display    = ['profile',  'encoding']

class MomentAdmin(admin.ModelAdmin):
      list_display    = ['picture']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Identification, IdentificationAdmin)
admin.site.register(Moment, MomentAdmin)