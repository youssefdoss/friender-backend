"""Generates CSVs of random data for friender users"""

import csv
from random import choice
from faker import Faker
from random_address import real_random_address

USERS_CSV_HEADERS = [
    'first_name',
    'last_name',
    'email',
    'image_url',
    'bio',
    'location',
    'radius',
    'password'
]

NUM_USERS = 20

fake = Faker()

# Generate random profile image URLs to use for users

image_urls = [
    f"https://randomuser.me/api/portraits/{kind}/{i}.jpg"
    for kind, count in [("lego", 10), ("men", 100), ("women", 100)]
    for i in range(count)
]

with open('generator/users.csv', 'w') as users_csv:
    users_writer = csv.DictWriter(users_csv, fieldnames=USERS_CSV_HEADERS)
    users_writer.writeheader()

    for i in range(NUM_USERS):
        users_writer.writerow(dict(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            image_url=choice(image_urls),
            bio=fake.sentence(),
            location=real_random_address()['postalCode'],
            radius=10000,
            password='$2b$12$Q1PUFjhN/AWRQ21LbGYvjeLpZZB6lfZ1BPwifHALGO6oIbyC3CmJe'
        ))