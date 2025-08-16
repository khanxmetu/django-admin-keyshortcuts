from django.contrib import admin

from .models import Language
from .models import Paper


class LanguageAdmin(admin.ModelAdmin):
    list_display = ["iso", "shortlist", "english_name", "name"]
    list_editable = ["shortlist"]
    search_fields = ["iso"]


site = admin.AdminSite(name="test_admin_keyboard_shortcuts")
site.register(Language, LanguageAdmin)
site.register(Paper)
