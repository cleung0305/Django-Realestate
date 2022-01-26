from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Listing, PhotoAlbum, Photo

# Create your views here.
def listings(request):
    listings = Listing.objects.all()
    paginator = Paginator(listings, 3)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    # paged_listings = paginator.get_elided_page_range(page, on_each_side=1, on_ends=1)
    context = {
        'listings': paged_listings
    }
    return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    listing = Listing.objects.filter(id=listing_id).first()
    context = {
        'listing': listing
    }
    return render(request, 'listings/listing.html', context)

def search(request):
    return render(request, 'listings/search.html')