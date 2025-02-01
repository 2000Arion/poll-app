from django.contrib import admin
from django.utils.html import format_html
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0
    readonly_fields = ('votes',)

    def reset_votes(self, obj):
        return format_html(
            '<input type="checkbox" name="reset_votes_{}" />', obj.pk
        )

    fields = ('choice_text', 'votes', 'reset_votes')

    def save_model(self, request, obj, form, change):
        if f"reset_votes_{obj.pk}" in request.POST:
            obj.votes = 0
            obj.save()


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'total_votes', 'pub_date')
    inlines = [ChoiceInline]

    def total_votes(self, obj):
        return sum(choice.votes for choice in obj.choice_set.all())
    total_votes.short_description = "Gesamtstimmen"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        for choice in obj.choice_set.all():
            if f"reset_votes_{choice.pk}" in request.POST:
                choice.votes = 0
                choice.save()


admin.site.register(Question, QuestionAdmin)
