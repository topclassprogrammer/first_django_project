import pytest
from django.urls import reverse

from students.models import Course


@pytest.mark.django_db
def test_retrieve_course(client, course_factory):
    courses = course_factory(_quantity=1)
    url = reverse('courses-detail', args=[1])

    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data['name'] == courses[0].name


@pytest.mark.django_db
def test_list_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')

    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for idx, course in enumerate(data):
        assert course['name'] == courses[idx].name


@pytest.mark.django_db
def test_filter_courses_by_id(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    max_id = max(course.id for course in courses)

    response = client.get(url, data={'id': max_id})

    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[-1].name


@pytest.mark.django_db
def test_filter_courses_by_name(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    last_course_name = courses[-1].name

    response = client.get(url, data={'name': last_course_name})

    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[-1].name


@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    url = reverse('courses-list')
    new_course = {'name': 'some course'}

    response = client.post(url, data=new_course)

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=1)
    course_id = courses[0].id
    url = reverse('courses-detail', args=[course_id])
    course_update = {'name': 'updated course name'}

    response = client.patch(url, data=course_update)

    assert response.status_code == 200
    data = response.json()
    assert data['name'] != courses[0].name


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=1)
    course_id = courses[0].id
    url = reverse('courses-detail', args=[course_id])

    response = client.delete(url)

    assert response.status_code == 204
    assert not Course.objects.filter(id=course_id)


@pytest.mark.parametrize('students_number', [19, 20, 21])
def test_max_students_per_course(settings, students_number):
    course = Course(name='some course')

    if students_number <= settings.MAX_STUDENTS_PER_COURSE:
        assert True
    else:
        assert False, f'На курсе {course.name} студентов {students_number}, ' \
                      f'что больше, чем {settings.MAX_STUDENTS_PER_COURSE}'
