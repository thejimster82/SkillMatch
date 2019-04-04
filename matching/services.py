import requests

from .models import Course


def update_courses():
    old_courses = Course.objects.all()
    if old_courses.exists():
        old_courses._raw_delete(old_courses.db)

    current_terms = ['2019 Spring', '2019 Fall', '2019 Summer']
    url = 'https://api.devhub.virginia.edu/v1/courses'
    r = requests.get(url)
    courses = r.json()['class_schedules']['records']

    current_courses = []
    for i in range(len(courses)):
        if courses[i][12] in current_terms:
            current_courses.append(Course(course_title=courses[i][4]))

    Course.objects.bulk_create(current_courses)


if __name__ == '__main__':
    update_courses()
