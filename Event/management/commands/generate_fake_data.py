import random
from datetime import datetime,timedelta
from faker import Faker
from django.core.management.base import BaseCommand
from Event.models import Event,Venue,Genre,EventMedia
from Authentication.models import User
from django.utils import timezone
import datetime
import requests
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

class Command(BaseCommand):
    help='Generate random data for Event and Venue models'

    def handle(self,*args,**options):
        fake=Faker('en_IN')

        #Specify no of fake users you want to create
        self.stdout.write(self.style.SUCCESS("Seeding User......."))
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
        self.stdout.write(self.style.SUCCESS("Successfully Seeded Users!"))
        

        # Seeding Genre Data
        self.stdout.write(self.style.SUCCESS("Seeding Genres......."))
        genres=['Comedy','Musical','Drama','Action','Horror']
        for genre in genres:
             Genre.objects.get_or_create(name=genre)
        self.stdout.write(self.style.SUCCESS("Successfully Seeded Genres!"))

        # Creating Meaningful Venue names
        def generate_venue_names():
            venue_types = ["Stadium", "Theater", "Arena", "Hall", "Auditorium", "Convention Center", "Gallery"]
            venue_name = fake.company()
            venue_type = random.choice(venue_types)
            return f"{venue_name} {venue_type}"

        #Created sample venues
        self.stdout.write(self.style.SUCCESS("Seeding Venues......."))
        for v in range(30):
            venue=Venue.objects.create(
                name = generate_venue_names(),
                location= fake.address().replace('\n', ', '),  # Replace newlines with commas for address
                no_of_seats= random.randint(100, 1000), 
                status='ACTIVE',
            )
            
            self.stdout.write(f'Created Venue: {venue}')
        self.stdout.write(self.style.SUCCESS("Successfully Seeded Venues!"))


        # Meaningful event names
        event_names = [
            "Rock 'n' Roll Night", "Jazz Under the Stars", "Pop Music Festival",
            "Tech Innovators Conference", "AI and Machine Learning Summit", "Startup Growth Expo",
            "Shakespeare in the Park", "Broadway Classics", "A Midsummer Night's Dream",
            "Football Championship Finals", "Marathon for Charity", "National Soccer League - Finals",
            "Photography 101", "Yoga for Beginners", "Art & Craft Workshop",
            "Annual Science Fair", "Business Leaders Symposium", "Food and Wine Festival",
            "Music on the Lake", "Gourmet Dinner & Wine Pairing", "The Great Outdoors Adventure",
            "Fitness & Wellness Expo", "Cybersecurity for Beginners", "Space Exploration Conference",
            "Entrepreneurship Summit", "Women's Leadership Forum", "International Film Festival",
            "Stand-up Comedy Night", "Hiking and Wilderness Retreat", "Cooking Masterclass"
        ]

        # Create some sample events
        self.stdout.write(self.style.SUCCESS("Seeding Events......."))
        for i in range(30):  
            # event_date = datetime.now().date() + timedelta(days=random.randint(1, 30))
            get_date = fake.date_this_year()
            event_date = get_date
            random_hour = random.randint(9,18) # For timing between 9:00 am to 6:00 pm
            random_minute = random.randint(0,59)
            start_time = timezone.make_aware(datetime.datetime.combine(get_date, datetime.time(random_hour,random_minute)))  # Start time tomorrow
            end_time = start_time + timedelta(hours=3) 

            event = Event.objects.create(
                name=random.choice(event_names),  # Random event name
                date=event_date,
                details=fake.paragraph(nb_sentences=8),  # Random event details
                start_time=start_time,
                end_time=end_time,
                posted_by=User.objects.order_by('?').first(),  # Random user from existing users
                venue_id=Venue.objects.order_by('?').first(),  # Random venue
                # status=random.choice(Event.STATUS_CHOICES)[0],
                status="UPCOMING",
                price=round(random.uniform(100, 1000), 2)  # Random price between 100 and 1000
            )
            
            #Assign random genres
            event.genres.set(random.sample(list(Genre.objects.all()),  k=random.randint(1, len(Genre.objects.all())))) #assign random genres

            self.stdout.write(f'Created Event: {event}')
        self.stdout.write(self.style.SUCCESS("Successfully Seeded Events!"))

        # Seeding Images for each event using Lorem Picsum
        self.stdout.write(self.style.SUCCESS("Seeding Images for Events......."))
        events = Event.objects.all()
        for event in events:
            media_type = random.choice(["BANNER","DETAIL"])
            image_url = f"https://picsum.photos/971/500.jpg?random={random.randint(1,1000)}"

            response = requests.get(image_url)
            if response.status_code == 200: # Meaning Successful URL 
                image_name = f"event_{event.id}_{media_type.lower()}.jpg" 
                image_path = os.path.join('images',image_name)
                image_file = ContentFile(response.content)
                saved_image_path = default_storage.save(image_path,image_file)

                media = EventMedia.objects.create(
                    event_id = event,
                    type = media_type,
                    image = saved_image_path,
                )
                self.stdout.write(f"Created Image {media.image.name} for event {event.name} ")
            else:
                self.stdout.write(self.style.ERROR(f"Download failed for image url {image_url}"))

        self.stdout.write(self.style.SUCCESS("Successfully Seeded Event Media!"))


