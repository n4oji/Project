from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.core.paginator import Paginator
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm, EventForm
import io
#imports for print files , cvs and pdf
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator


#homapage
def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	name = "Naoji"
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	cal = HTMLCalendar().formatmonth(year, month_number)

	now = datetime.now()
	current_year = now.year

	time = now.strftime('%H:%M')

	return render(request, 'events/home.html', {
		"name" : name,
		"year" : year,
		"month" : month,
		"month_number" : month_number,
		"cal" : cal,
		"current_year" : current_year,
		"time" : time,
	})

#events list
def all_events(request):
	event_list = Event.objects.all().order_by('event_date')

	return render(request, 'events/events_list.html', {'event_list': event_list})

#adding a venue
def add_venue(request):
	submitted = False
	if request.method == "POST":
		form = VenueForm(request.POST)
		if form.is_valid():
			form.save()

			return HttpResponseRedirect('/add_venue?submitted=True')
	else:
		form = VenueForm
		if 'submitted' in request.GET:
			submitted = True

	return render(request, 'events/add_venue.html', {'form': form, 'submitted': submitted})

#venues list
def list_venues(request):
	# venue_list = Venue.objects.all().order_by('name')
	venue_list = Venue.objects.all()

	#set up pagination
	p = Paginator(Venue.objects.all(), 5)
	page = request.GET.get('page')
	venues = p.get_page(page)
	nums = "a" * venues.paginator.num_pages

	return render(request, 'events/venue.html', {
		'venue_list': venue_list,
		'venues': venues,
		'nums': nums
		})

#show specified venue
def show_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)

	return render(request, 'events/show_venue.html', {'venue': venue})

#search bar for venues
def search_venues(request):
	if request.method=="POST":
		searched = request.POST['searched']
		venues = Venue.objects.filter(name__contains=searched)

		return render(request, 'events/search_venues.html', 
			{'searched': searched,
			'venues': venues})
	else:
		return render(request, 'events/search_venues.html', {})

#updating a venue
def update_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	form = VenueForm(request.POST or None, instance=venue)
	if form.is_valid():
		form.save()
		
		return redirect('list-venues')

	return render(request, 'events/update_venue.html', {'venue': venue, 'form': form})

#adding event
def add_event(request):
	submitted = False
	if request.method == "POST":
		form = EventForm(request.POST)
		if form.is_valid():
			form.save()

			return HttpResponseRedirect('/add_event?submitted=True')
	else:
		form = EventForm
		if 'submitted' in request.GET:
			submitted = True

	return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})

#update event
def update_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	form = EventForm(request.POST or None, instance=event)
	if form.is_valid():
		form.save()
		
		return redirect('list-events')

	return render(request, 'events/update_event.html', {'event': event, 'form': form})

#delete event
def delete_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	event.delete()

	return redirect('list-events')

#delete venue
def delete_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	venue.delete()

	return redirect('list-venues')

#generate a file with all venues
def venue_text(request):
	response = HttpResponse(content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=venues.txt'

	venues = Venue.objects.all()

	lines = []
	for venue in venues:
		lines.append(f"{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.website}\n{venue.email_address}\n\n")

	#escrever em txt
	response.writelines(lines)
	return response

#create csv file with venues
def venue_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=venues.csv'

	#create csv writer
	writer = csv.writer(response)

	venues = Venue.objects.all()

	#add column headings to csv file
	writer.writerow(['Venue Name', 'Address', 'Zip-Code', 'Phone', 'Website', 'Email'])

	for venue in venues:
		writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.website, venue.email_address])

	return response

#create a pdf with venues
def venue_pdf(request):
	#create bytestream
	buf = io.BytesIO()
	#create canvas
	c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
	#create text object
	textobj = c.beginText()
	textobj.setTextOrigin(inch, inch)
	textobj.setFont("Helvetica", 16)

	venues = Venue.objects.all()

	lines = []

	for venue in venues:
		lines.append(venue.name)
		lines.append(venue.address)
		lines.append(venue.zip_code)
		lines.append(venue.phone)
		lines.append(venue.website)
		lines.append(venue.email_address)
		lines.append(" ")

	for line in lines:
		textobj.textLine(line)

	c.drawText(textobj)
	c.showPage()
	c.save()
	buf.seek(0)

	return FileResponse(buf, as_attachment=True, filename='venue.pdf')

