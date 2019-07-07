from django.contrib import admin
from .models import Tutorial, TutorialCategory, TutorialSeries
from django.db import models
from tinymce.widgets import TinyMCE
# Register your models here.

class TutorialAdmin(admin.ModelAdmin):
    # to change the order of the items in admin panel
    '''
    fields = ["title",
              "published",
              "content"]
    '''
    # to group the items
    fieldsets = [("Title/date", {"fields": ["title","published"]}),
                 ("URL", {"fields": ["slug"]}),
                 ("Series", {"fields": ["series"]}),
                 ("Content", {"fields": ["content"]})]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }

admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(TutorialCategory)
admin.site.register(TutorialSeries)