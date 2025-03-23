from django.contrib import admin
from main.models import Contact,Profile,UserLocation


class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','subject','added_on','is_approved']


admin.site.register(Contact, ContactAdmin)
admin.site.register(Profile)

admin.site.register(UserLocation)