from copy import copy
from dataclasses import dataclass
from datetime import date, time, timedelta


class Owner:
    """
    Represents a pet owner and manages their pets, schedule, and veterinary contacts.

    Attributes:
        first_name (str): The owner's first name.
        last_name (str): The owner's last name.
        age (int): The owner's age.
        pets (list): A list of Pet objects belonging to the owner.
        scheduler (Scheduler): The scheduling system tied to the owner's tasks.
        vets (list): A list of Vet objects the owner is registered with.
    """

    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.pets = []
        self.scheduler = Scheduler(date.today(), owner=self)
        self.vets = []

    def add_pet(self, pet):
        """
        Adds a new pet to the owner's list of pets and assigns this owner to the pet.

        Args:
            pet (Pet): The pet object to add.
        """
        if pet not in self.pets:
            self.pets.append(pet)
            pet.owner = self

    def remove_pet(self, pet):
        """
        Removes a pet from the owner's list and clears the owner reference from the pet.

        Args:
            pet (Pet): The pet object to remove.
        """
        if pet in self.pets:
            self.pets.remove(pet)
            if pet.owner is self:
                pet.owner = None

    def view_schedule(self):
        """
        Retrieves the combined schedule of tasks for all pets owned by this owner.

        Returns:
            list: A sorted list of tasks scheduled for today.
        """
        return self.scheduler.check_calendar()

    def contact_vet(self, pet):
        """
        Initiates contact with a veterinarian regarding a specific pet.

        Args:
            pet (Pet): The pet needing veterinary attention.
        """
        pass


class Pet:
    """
    Represents a pet and manages their medications, tasks, and veterinary records.

    Attributes:
        name (str): The name of the pet.
        age (int): The age of the pet.
        health_status (str): The current health status of the pet.
        medications (list): A list of medications prescribed to the pet.
        tasks (list): A list of care tasks associated with the pet.
        vets (list): A list of veterinarians the pet sees.
        owner (Owner, optional): The owner of the pet.
    """

    def __init__(self, name, age, health_status, owner=None):
        self.name = name
        self.age = age
        self.health_status = health_status
        self.medications = []
        self.tasks = []
        self.vets = []
        self.owner = owner

    def take_medication(self):
        """
        Record the administration of a medication to the pet.
        """
        pass

    def update_health_status(self, status):
        """
        Updates the current health status of the pet.

        Args:
            status (str): The new health status.
        """
        pass

    def get_age(self):
        """
        Retrieves the age of the pet.
        """
        pass

    def add_task(self, task):
        """
        Adds a care task to the pet's task list. If the task does not 
        already have a pet assigned, this pet is assigned to the task.

        Args:
            task (Task): The task to add to the pet's schedule.
        """
        self.tasks.append(task)
        if task.pet is None:
            task.pet = self


class Vet:
    """
    Represents a veterinarian and provides functionality for checkups and prescriptions.

    Attributes:
        name (str): The name of the clinic or practice.
        doctor (str): The name of the doctor/veterinarian.
        location (str): The address or location of the practice.
        phone (str): The contact phone number for the veterinarian.
    """

    def __init__(self, name, doctor, location, phone):
        self.name = name
        self.doctor = doctor
        self.location = location
        self.phone = phone

    def prescribes(self, pet, medication):
        """
        Prescribes a medication to a given pet.

        Args:
            pet (Pet): The pet receiving the prescription.
            medication (str): The medication being prescribed.
        """
        pass

    def checkup(self, pet):
        """
        Conducts a routine checkup for a pet.

        Args:
            pet (Pet): The pet being checked up.
        """
        pass


class Scheduler:
    """
    Manages scheduling of tasks and appointments for an owner's pets.

    Attributes:
        date (date): The current date of the scheduler.
        owner (Owner, optional): The owner associated with the scheduler.
        calendar (list): A list of tasks if no owner is provided.
    """

    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    def __init__(self, date, owner=None, calendar=None):
        self.date = date
        self.owner = owner
        self.calendar = calendar if calendar is not None else []

    def check_calendar(self):
        """
        Retrieves all tasks for the scheduled date, sorting them by priority (high > medium > low)
        and then chronologically by time. If an owner is attached, retrieves and flattens
        tasks from all of the owner's pets. If no owner is attached, relies on the `calendar` list.

        Returns:
            list: A sorted list of Task objects scheduled for `self.date`.
        """
        if self.owner is None:
            return sorted(self.calendar, key=lambda task: (task.date_due, task.time_due))

        all_tasks = [
            task for pet in self.owner.pets
            for task in pet.tasks
            if task.date_due == self.date
        ]

        return sorted(
            all_tasks,
            key=lambda task: (self.PRIORITY_ORDER.get(task.priority, 1), task.time_due),
        )

    def filter_tasks(self, pet_name=None, completion_status=None):
        """
        Filters today's scheduled tasks by pet name and/or completion status.

        Args:
            pet_name (str, optional): Only return tasks belonging to this pet.
            completion_status (bool, optional): True for completed, False for incomplete.

        Returns:
            list: Filtered list of Task objects from today's schedule, sorted by time due.
        """
        tasks = self.check_calendar()
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet and t.pet.name.lower() == pet_name.lower()]
        if completion_status is not None:
            tasks = [t for t in tasks if t.completion_status == completion_status]
        return sorted(tasks, key=lambda t: t.time_due)

    def detect_conflicts(self):
        """
        Detects tasks scheduled at the exact same time across all pets in the owner's schedule.

        Groups tasks by their `time_due` and identifies any timeslot that has more than one task.
        If an error occurs while fetching the schedule, it traps the exception and returns
        a warning message rather than crashing.

        Returns:
            list of str: A list of warning messages detailing the conflicts (e.g.,
            "Warning: conflict at 08:00:00 — Mochi: Morning walk | Yeontan: Give Meds").
            If no conflicts exist, returns ["No conflicts found."].
        """
        try:
            tasks = self.check_calendar()
        except Exception as e:
            return [f"Warning: could not load schedule — {e}"]

        time_groups = {}
        for task in tasks:
            time_groups.setdefault(task.time_due, []).append(task)

        warnings = []
        for slot_time, group in time_groups.items():
            if len(group) < 2:
                continue
            labels = []
            for t in group:
                pet_name = t.pet.name if t.pet else "Unknown pet"
                labels.append(f"{pet_name}: {t.description}")
            warnings.append(f"Warning: conflict at {slot_time} — {' | '.join(labels)}")

        return warnings if warnings else ["No conflicts found."]

    def make_appt(self, pet, vet, task):
        """
        Schedules a new veterinary appointment.

        Args:
            pet (Pet): The pet the appointment is for.
            vet (Vet): The veterinarian the appointment is with.
            task (Task): The task details representing the appointment.
        """
        pass

    def add_task(self, task):
        """
        Adds a single task directly to the scheduler.

        Args:
            task (Task): The task to be added.
        """
        pass


@dataclass
class Task:
    """
    Represents a specific care task or activity required for a pet.

    Attributes:
        description (str): A brief description of the task (e.g., "Morning walk").
        time_due (time): The time the task should be completed.
        frequency (str): How often the task occurs (e.g., "daily", "weekly").
        completion_status (bool): Whether the task has been completed.
        date_due (date): The date the task is scheduled for.
        pet (object, optional): The pet associated with this task.
    """
    description: str
    time_due: time
    frequency: str
    completion_status: bool
    date_due: date
    priority: str = "medium"
    pet: object = None

    def get_deadline(self):
        """
        Retrieves the deadline for the task.
        """
        pass


    def mark_complete(self):
        """
        Marks the task as completed and schedules the next occurrence
        for daily (tomorrow) or weekly (7 days) recurring tasks.
        The new task is automatically added to the pet's task list.
        """
        self.completion_status = True

        intervals = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}
        delta = intervals.get(self.frequency)

        if delta and self.pet is not None:
            next_task = copy(self)
            next_task.date_due = self.date_due + delta
            next_task.completion_status = False
            self.pet.tasks.append(next_task)
