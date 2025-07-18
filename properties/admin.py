from django.contrib import admin
from .models import Property

# Register your models here.
admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'location', 'created_at')
    search_fields = ('title', 'description', 'location')
    list_filter = ('location', 'created_at')
    ordering = ('-created_at',)
