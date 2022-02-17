from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from email.mime.image import MIMEImage

from datetime import datetime, timedelta
from .models import Contact
from listings.models import Listing
from realtors.models import Realtor

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

        listing_model = Listing.objects.get(id=listing_id)

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
        html_body = render_to_string('contacts/inquiry_email.html', {
            'name': name,
            'listing_id': listing_id,
            'listing_model': listing_model,
            'domain': domain,
        })
        img_data = listing_model.album.default().photo.read()
        img = MIMEImage(img_data)
        img.add_header('Content-ID', '<listing_img>')
        img.add_header('Content-Disposition', 'inline', filename="listing_img")
        
        email = EmailMultiAlternatives(mail_subject, None, to=[email])
        email.attach_alternative(html_body, "text/html")
        email.mixed_subtype = 'related'
        email.attach(img)

        email.send(fail_silently=False)

        # Send Email to realtor
        realtor = Realtor.objects.get(email=realtor_email)
        realtor_mail_subject = f'You\'ve Got An Inquiry for {listing}'
        realtor_mail_message = render_to_string('contacts/inquiry_realtor_email.html', {
            'realtor': realtor,
            'name': name,
            'listing_id': listing_id,
            'listing': listing,
            'domain': domain,
        })
        realtor_email = EmailMessage(realtor_mail_subject, realtor_mail_message, to=[])
        realtor_email.content_subtype = 'html'
        realtor_email.send(fail_silently=False)

        messages.success(request, 'Your inquiry has been submitted, a realtor will get back to you soon.')
        return redirect('listings:listing', listing_id=listing_id)