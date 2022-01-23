from django.contrib import admin

from .models import Listing, PhotoAlbum, Photo

admin.site.register(Listing)
admin.site.register(PhotoAlbum)
admin.site.register(Photo)

