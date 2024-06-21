from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Scope, Tag


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        counter = 0
        for form in self.forms:
            counter += form.cleaned_data.get('is_main', 0)
            if not form.cleaned_data:
                if counter == 0:
                    raise ValidationError('Укажите основной раздел')
                elif counter > 1:
                    raise ValidationError('Основным может быть '
                                          'только один раздел')


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
