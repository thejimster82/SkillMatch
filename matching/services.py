import requests

from .models import Course


def update_courses():
    current_terms = ['2019 Spring', '2019 Fall', '2019 Summer']
    url = 'https://api.devhub.virginia.edu/v1/courses'
    r = requests.get(url)
    courses = r.json()[records]
    current_courses = []

    for i in range(len(courses)):
        if courses[i][12] in current_terms:
            current_courses.append(Course(course_title=courses[i][4]))

    Course.objects.bulk_create(current_courses)
