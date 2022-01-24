from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Listing, PhotoAlbum, Photo

def linkify(field_name):
    """
    Converts a foreign key value into clickable links.
    
    If field_name is 'parent', link text will be str(obj.parent)
    Link will be admin url for the admin url for obj.parent.id:change
    """
    def _linkify(obj):
        linked_obj = getattr(obj, field_name)
        if linked_obj is None:
            return '-'
        app_label = linked_obj._meta.app_label
        model_name = linked_obj._meta.model_name
        view_name = f'admin:{app_label}_{model_name}_change'
        link_url = reverse(view_name, args=[linked_obj.pk])
        return format_html('<a href="{}">{}</a>', link_url, linked_obj)

    _linkify.short_description = field_name  # Sets column name
    return _linkify

class PhotoAlbumAdmin(admin.ModelAdmin):
    model = PhotoAlbum
    list_display = ['title', 'get_main_link', 'get_photo_link']

    @admin.display(description='Main Photo')
    def get_main_link(self, obj):
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


admin.site.register(Listing)
admin.site.register(PhotoAlbum, PhotoAlbumAdmin)
admin.site.register(Photo)

