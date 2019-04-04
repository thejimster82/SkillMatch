import requests

from django.core.management.base import BaseCommand, CommandError
from matching.models import Course


class Command(BaseCommand):
    help = 'Load new courses from the UVA devhub API'
    current_terms = ['2019 Spring', '2019 Fall', '2019 Summer']

    def handle(self, *args, **options):
        self.delete_old_courses()
        courses = self.get_courses()
        Course.objects.bulk_create(courses)
        self.stdout.write(self.style.SUCCESS(
            'Successfully added %i courses' % len(courses)))

    def delete_old_courses(self):
        old_courses = Course.objects.all()
        if old_courses.exists():
            old_courses._raw_delete(old_courses.db)

    def get_courses(self):
        url = 'https://api.devhub.virginia.edu/v1/courses'
        r = requests.get(url)
        all_courses = r.json()['class_schedules']['records']

        courses = []
        for i in range(len(all_courses)):
            if all_courses[i][12] in self.current_terms:
                course_title = all_courses[i][0] + \
                    all_courses[i][1] + ': ' + all_courses[i][4]
                courses.append(Course(course_title=course_title))
        return courses
