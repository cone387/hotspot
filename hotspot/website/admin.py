from django.contrib import admin
from .models import SourceItem, HotSpot, Collection, CrawlLog, History
# Register your models here.


class SourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'site_name', 'name', 'fetch_interval', 'status', 'last_runtime', 'warn_msg')
    # list_editable = ('category', 'name', 'fetch_interval', 'status', 'fetch_time')
    list_filter = ('name', 'status', 'warn_msg')


class HotSpotAdmin(admin.ModelAdmin):
    list_display = ('source', 'title', 'url',)


class CrawlLogAdmin(admin.ModelAdmin):
    list_display = ('source_id', 'hot_num', 'upload_num', 'start_time')


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'source', 'title', 'create_time')


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'source', 'title', 'create_time')


admin.site.register(SourceItem, SourceAdmin)
admin.site.register(HotSpot, HotSpotAdmin)
admin.site.register(CrawlLog, CrawlLogAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(Collection, CollectionAdmin)
