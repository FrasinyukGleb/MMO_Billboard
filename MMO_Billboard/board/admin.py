from django.contrib import admin


from board.models import *

from django_summernote.admin import SummernoteModelAdmin
from board.models import *


# Apply summernote to all TextField in model.
class PostAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ['content']
    exclude = ('author',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Post, PostAdmin)

