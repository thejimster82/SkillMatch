import requests

from django.core.management.base import BaseCommand, CommandError
"""
Grab all courses in the current term from the devhub
API and store in the database. PostgreSQL supports
automatic pk generation with bulk_create so the
process is very fast.
"""
from matching.models import Course


class Command(BaseCommand):
    help = 'Load new courses from the UVA devhub API'
    current_terms = ['2019 Spring']

    def handle(self, *args, **options):
        self.delete_old_courses()
        courses = self.get_courses()
        Course.objects.bulk_create(courses)
        self.stdout.write(self.style.SUCCESS(
            'Successfully added %i courses' % len(courses)))

    def delete_old_courses(self):
        old_courses = Course.objects.all()
        if old_courses.exists():
            old_courses.delete()

    def get_courses(self):
        url = 'https://api.devhub.virginia.edu/v1/courses'
        r = requests.get(url)
        all_courses = r.json()['class_schedules']['records']

        courses = []
        unique_courses = []
        for i in range(len(all_courses)):
            if all_courses[i][12] in self.current_terms:
                course_title = all_courses[i][0] + \
                    all_courses[i][1] + ': ' + all_courses[i][4]
                courses.append(Course(course_title=course_title))

        for course in courses:
            for u in unique_courses:
                if course.course_title != u.course_title:
                    unique_courses.append(course)

        return unique_courses
