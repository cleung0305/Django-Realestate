from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Listing, PhotoAlbum, Photo

# Create your views here.
def listings(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 12)
    page = request.GET.get('page', 1)
    paged_listings = paginator.get_page(page)
    page_range = paginator.get_elided_page_range(number=page, on_each_side=1, on_ends=1)
    context = {
        'listings': paged_listings,
        'page_range': page_range
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