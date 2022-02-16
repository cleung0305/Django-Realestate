from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from datetime import datetime, timedelta
from .models import Contact

# Create your views here.
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Check if user has inquired recently. (less than a day)
        if Contact.objects.filter(listing_id=listing_id, email=email, contact_date__gte=datetime.today()-timedelta(days=1)):
            messages.error(request, 'You have made an inquiry for this listing, please try again later')
            return redirect('listings:listing', listing_id=listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, user_id=user_id, name=name, 
                        email=email, phone=phone, massage=message)
        contact.save()

        # Send Email to User
        domain = get_current_site(request).domain
        mail_subject = f'BT Real Estate: Inquiry for {listing}'
        mail_message = render_to_string('contacts/inquiry_email.html', {
            'name': name,
            'listing_id': listing_id,
            'listing': listing,
            'domain': domain,
        })
        email = EmailMessage(mail_subject, mail_message, to=[email])
        email.content_subtype = 'html'
        email.send(fail_silently=False)

        # Send Email to realtor

        messages.success(request, 'Your inquiry has been submitted, a realtor will get back to you soon.')
        return redirect('listings:listing', listing_id=listing_id)