from faker import Faker

def getProfile():
    fake = Faker()
    return fake.profile()

import os 
from coding_acme.models import Employee
from coding_acme import db


def seedData():
    for seed_num in range(10):
        data = getProfile()
        employee = Employee(data['name'], data['address'],data['ssn'], data['job'],data['mail'], data['birthdate'])

        db.session.add(employee)
        db.session.commit()

seedData()