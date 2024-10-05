import random
from datetime import datetime,timedelta
from faker import Faker
from django.core.management.base import BaseCommand
from Event.models import Event,Venue,Genre
from Authentication.models import User
from django.utils import timezone
import datetime

class Command(BaseCommand):
    help='Generate random data for Event and Venue models'

    def handle(self,*args,**options):
        fake=Faker('en_IN')
        #Specify no of fake users you want to create
        number_of_users=40
        for u in range(number_of_users):
            user=User.objects.create_user(
            username=fake.user_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            middle_name=fake.first_name() if random.choice([True, False]) else '',  # Optional middle name
            email=fake.email(),
            password='password123',
            role='USER',
            status='ACTIVE'
             )
            user.save()
          # Print the created user's details
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.username} - {user.email}'))
        genres=['Comedy','Musical','Drama','Action','Horror']
        for genre in genres:
             Genre.objects.get_or_create(name=genre)

    #Created sample venues
        for v in range(30):
             venue=Venue.objects.create(
             name = fake.catch_phrase(),
             location=fake.address().replace('\n', ', '),  # Replace newlines with commas for address
             no_of_seats=random.randint(100, 1000), 
             status='ACTIVE',
        )
    
        self.stdout.write(f'Created Venue: {venue}')

        # Create some sample events
        for i in range(30):  
            event_date = datetime.now().date() + timedelta(days=random.randint(1, 30))
            start_time = timezone.make_aware(datetime.datetime.now() + datetime.timedelta(days=1))  # Start time tomorrow
            end_time = start_time + datetime.timedelta(hours=3) 

            event = Event.objects.create(
                name=fake.catch_phrase(),  # Random event name
                date=event_date,
                details=fake.paragraph(nb_sentences=8),  # Random event details
                start_time=start_time,
                end_time=end_time,
                posted_by=User.objects.order_by('?').first(),  # Random user from existing users
                venue_id=Venue.objects.order_by('?').first(),  # Random venue
                status=random.choice(Event.STATUS_CHOICES)[0],
                price=round(random.uniform(100, 1000), 2)  # Random price between 100 and 1000
            )
            #Assign random genres
            event.genres.set(random.sample(list(Genre.objects.all()),  k=random.randint(1, len(Genre.objects.all())))) #assign random genres

            self.stdout.write(f'Created Event: {event}')

