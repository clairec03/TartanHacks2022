from django.contrib import admin
from main.models import Profile, Identification, Moment, Tagged
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
      list_display    = ['user', 'id', 'avatar']

class IdentificationAdmin(admin.ModelAdmin):
      list_display    = ['profile',  'encoding']

class MomentAdmin(admin.ModelAdmin):
      list_display    = ['id', 'picture']

class TaggedAdmin(admin.ModelAdmin):
      list_display    = ['moment', 'picture']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Identification, IdentificationAdmin)
admin.site.register(Moment, MomentAdmin)
admin.site.register(Tagged, TaggedAdmin)