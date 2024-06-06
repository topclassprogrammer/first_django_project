from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}


def dish_view(request):
    dish = request.META.get('PATH_INFO').strip('/')
    servings = request.GET.get('servings')
    if not servings:
        servings = 1
    elif not servings.isdigit() or int(servings) < 1:
        raise ValueError('Кол-во порций должно быть целым числом '
                         'и/или больше нуля')
    dish_servings = {k: round(v*int(servings), 2)
                     for k, v in DATA[dish].items()}
    template_name = 'calculator/index.html'
    context = {'recipe': dish_servings}
    return render(request, template_name, context)
