from django.shortcuts import render

from .models import Student


def students_list(request):
    ordering = 'group'
    students = Student.objects.order_by(ordering).prefetch_related('teachers')
    template = 'school/students_list.html'
    context = {'students': students}
    return render(request, template, context)
