import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs411f17.settings")
django.setup()

from app.models import UserInfo

from faker import Faker
import pandas as pd


def generate_fake_user(num_fakes):
    for i in range(10):
        _generate_fake_user(num_fakes, i)
        print("Generated Chunk {}".format(i))


def _generate_fake_user(num_fakes, chunk):
    fake = Faker()

    fake_users = []
    for i in range(num_fakes):
        user = {
            'id': '',
            'name': '',
            'location': '',
            'num_friends': '',
            'age_range': '',
            'religion': '',
            'education': '',
            'hometown': '',
        }

        user['id'] = [i]
        user['name'] = fake.name()
        user['location'] = fake.address()
        user['num_friends'] = fake.random_int(min=0, max=5000)
        user['age_range'] = fake.random_int(min=14, max=100)
        user['religion'] = ''
        user['education'] = "{} University".format(fake.city())
        user['hometown'] = "{}, {}".format(fake.city(), fake.state())
        fake_users.append(user)

    df = pd.DataFrame(fake_users)
    df.to_csv('fake_users{}.csv'.format(chunk))


generate_fake_user(100000)
print("Done generating users")
