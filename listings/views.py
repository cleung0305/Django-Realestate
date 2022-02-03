from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Listing, PhotoAlbum, Photo
from .choices import bedroom_choices, price_choices, state_choices

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
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': listing
    }
    return render(request, 'listings/listing.html', context)

def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    #keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    #City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    #State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    #bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    #price
    if 'price_lower' in request.GET and 'price_upper' in request.GET:
        price_lower = request.GET['price_lower']
        price_upper = request.GET['price_upper']
        if price_lower and price_upper:
            if price_lower < price_upper:
                queryset_list = queryset_list.filter(price__gte=price_lower, price__lte=price_upper)
        elif not price_lower and price_upper:
            queryset_list = queryset_list.filter(price__lte=price_upper)
        elif not price_upper and price_lower:
            queryset_list = queryset_list.filter(price__gte=price_lower)

    context = {
        'listings': queryset_list,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'state_choices': state_choices,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)