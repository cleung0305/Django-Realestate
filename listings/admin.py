from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Listing, PhotoAlbum, Photo

class ListingAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'list_date', 'is_published', 'realtor']
    list_display_links = ['id', 'title']
    list_filter = ['realtor',]
    list_editable = ['is_published']
    search_fields = ['title', 'street_address', 'city', 'state', 'zip', 'price']
    list_per_page = 25

class PhotoAlbumAdmin(admin.ModelAdmin):
    model = PhotoAlbum
    list_display = ['title', 'get_main_link', 'get_photo_link']

    @admin.display(description='Main Photo')
    def get_main_link(self, obj):
        if obj.photos.filter(default=True):
            link_url = reverse('admin:listings_photo_change', args=[obj.default().id])
            return format_html('<a href="{}">{}</a>', link_url, obj.default().name)

    @admin.display(description='Photos')
    def get_photo_link(self, obj):
        urllist = ''
        for x in list(obj.photos.filter(default=False)):
            link_url = reverse('admin:listings_photo_change', args=[x.id])
            html = f'<a href="{link_url}">{x.name}&nbsp;&nbsp;&nbsp;&nbsp;</a>'
            urllist += html
        return format_html(urllist)

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['name', 'album', 'default']

admin.site.register(Listing, ListingAdmin)
admin.site.register(PhotoAlbum, PhotoAlbumAdmin)
admin.site.register(Photo, PhotoAdmin)

