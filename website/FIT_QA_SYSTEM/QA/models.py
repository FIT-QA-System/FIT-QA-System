from django.db import models

# Create your models here.

class Building(models.Model):
    city = models.CharField("City", max_length=20)
    state = models.CharField("State", max_length=2)
    street = models.CharField("Street", max_length=100)
    zip = models.CharField("Zip", max_length=10)

    building_code = models.CharField("Building Code", max_length=20)
    building_description = models.CharField("Building Description", max_length=100)
    building_name = models.CharField("Building Name", max_length=100)
    building_number = models.CharField("Building Number", max_length=20)
    building_abbr = models.CharField("Building Abbreviation", max_length=3)
    latitude = models.FloatField("Latitude")
    longitude = models.FloatField("Longitude")

    update_date = models.DateTimeField('last update')

    def __str__(self):
        return self.building_code + " " + self.building_name

    class Meta:
        ordering = ('building_name',)


class Department(models.Model):
    department_id = models.CharField('Department ID', max_length=20)
    parent_department_id = models.CharField('Parent Department ID', max_length=20)
    name = models.CharField('Department Name', max_length=100)
    descriptions = models.CharField('Department Descriptions', max_length=300, null=True)

    contact_phone_international_code = models.CharField('International Code', max_length=5)
    contact_phone_area_code = models.CharField('Area Code', max_length=3)
    contact_phone_number = models.CharField('Number', max_length=7)
    contact_phone_extension = models.CharField('Extension', max_length=10)

    contact_email = models.EmailField('Email')

    contact_facebook = models.URLField('Facebook')

    contact_website = models.URLField('Website')

    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)

    update_date = models.DateTimeField('last update')

    def __str__(self):
        return self.department_id + " " + self.name

    class Meta:
        ordering = ('name',)


class Employee(models.Model):
    supervisor = models.CharField("Supervisor", max_length=100)
    supervisee = models.CharField("Supervisee", max_length=100)
    # supervisee = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    tracks =models.CharField("Tracks Account", max_length=20)

    first_name = models.CharField("First Name", max_length=100)
    last_name = models.CharField("Last Name", max_length=100)
    middle_name = models.CharField("Middle Name", null=True, max_length=100)
    prefix_name = models.CharField("Prefix", null=True, max_length=100)
    suffix_name = models.CharField("Suffix", null=True, max_length=100)

    email = models.EmailField("Email")

    phone_international_code = models.CharField('International Code', max_length=5)
    phone_area_code = models.CharField('Area Code', max_length=3)
    phone_number = models.CharField('Number', max_length=7)
    phone_extension = models.CharField('Extension', max_length=10)

    title = models.CharField("Title", max_length=200)

    position = models.CharField("Position (Primary and Additional) JSON", max_length=100)

    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.prefix_name + " " + self.first_name + " " + self.last_name + " " + self.email

    class Meta:
        ordering = ('tracks',)





class Course(models.Model):
    crn = models.CharField("CRN", max_length=100)
    subject = models.CharField("Subject", max_length=100)
    course_number = models.CharField("Course Number", max_length=100)
    section = models.CharField("Section", max_length=100)
    title = models.CharField("Title", max_length=100)
    term = models.CharField("Term", max_length=100)
    year = models.CharField("Year", max_length=100)

    description = models.TextField("Description", max_length=200)
    description_prereqs = models.TextField("Description with Prereqs", max_length=200)

    prerequisites = models.TextField("Prerequisites", max_length=100)

    instructor = models.CharField("Instructor", max_length=100)

    credit_hours = models.IntegerField("Credit Hours")

    building = models.ForeignKey(Building, on_delete=models.SET_NULL, null=True)

    room = models.CharField("Room", max_length=100)

    days = models.CharField("Days", max_length=100)

    begin_time = models.CharField("Begin Time", max_length=100)
    end_time = models.CharField("End Time", max_length=100)

    max_enroll = models.IntegerField("Max Enroll")
    actual_enroll = models.IntegerField("Actual Enroll")

    def __str__(self):
        return self.subject + " " + self.course_number + " " + self.title

    class Meta:
        ordering = ('subject', 'course_number')






