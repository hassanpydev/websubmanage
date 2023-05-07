from django.contrib import admin
from .models import Subdomain, Domain, Keyword

# Register your models here.
admin.site.site_title = "SubManage"  # Custom site title
admin.site.site_header = "Subdomain Manager"  # Custom site header
admin.site.index_title = "Subdomain Manager"  # Custom index title


class KeywordAdmin(admin.ModelAdmin):
    list_display = ['word', 'subdomain', 'follow_releated_search', 'follow_ppl_also_ask', 'max_results', 'created_at',
                    'updated_at']
    list_filter = ['subdomain', 'follow_releated_search', 'follow_ppl_also_ask']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Keyword Information', {'fields': ['word', 'subdomain']}),
        ('Settings', {'fields': ['follow_releated_search', 'follow_ppl_also_ask', 'max_results']}),
        ('Timestamps', {'fields': ['created_at', 'updated_at']}),
    ]
    search_fields = ['word']

class PostAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Post Information', {
            'fields': ('post_title', 'post_content', 'post_excerpt'),
        }),
        ('Status', {
            'fields': ('post_status', 'comment_status', 'ping_status'),
        }),
        ('Date Information', {
            'fields': ('post_date', 'post_modified'),
        }),
    )

    actions = ['make_published']

    def make_published(self, request, queryset):
        queryset.update(post_status='publish')
    make_published.short_description = 'Mark selected posts as published'


admin.site.register(Keyword, KeywordAdmin)

admin.site.register(Subdomain)
admin.site.register(Domain)
