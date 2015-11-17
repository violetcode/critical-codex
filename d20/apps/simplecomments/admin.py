from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Comment

# Register your models here.
class CommentsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None,
           {'fields': ('content_type', 'object_pk')}
        ),
        (_('Content'),
           {'fields': ('user', 'comment')}
        ),
        (_('Hierarchy'),
           {'fields': ('parent')}
        ),
        (_('Metadata'),
           {'fields': ('submit_date')}
        ),
    )

    list_display = ('name','content_type', 'object_pk', 'parent', 'submit_date')
    search_fields = ('comment', 'user__username')
    raw_id_fields = ("parent",)
    date_hierarchy = 'submit_date'
    ordering = ('-submit_date',)

admin.site.register(Comment, CommentsAdmin)