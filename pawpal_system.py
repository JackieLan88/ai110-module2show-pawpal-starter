from dataclasses import dataclass, field
from datetime import date, time


class Owner:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.pets = []
        self.scheduler = None
        self.vets = []

    def add_pet(self, pet):
        pass

    def remove_pet(self, pet):
        pass

    def view_schedule(self):
        pass

    def contact_vet(self, vet):
        pass


@dataclass
class Pet:
    name: str
    age: int
    medication: str
    health_status: str
    tasks: list = field(default_factory=list)

    def take_medication(self):
        pass

    def update_health_status(self, status):
        pass

    def get_age(self):
        pass


class Vet:
    def __init__(self, name, doctor, location, phone):
        self.name = name
        self.doctor = doctor
        self.location = location
        self.phone = phone

    def prescribes(self, pet, medication):
        pass

    def checkup(self, pet):
        pass


class Scheduler:
    def __init__(self, date, calendar=None):
        self.date = date
        self.calendar = calendar if calendar is not None else []

    def check_calendar(self):
        pass

    def make_appt(self, task):
        pass

    def add_task(self, task):
        pass


@dataclass
class Task:
    name: str
    type: str
    time_due: time
    date_due: date
    list_tasks: list = field(default_factory=list)

    def get_deadline(self):
        pass

    def get_name(self):
        pass
