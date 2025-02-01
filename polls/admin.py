from django.contrib import admin
from .models import Question, Choice


def reset_all_votes(modeladmin, request, queryset):
    for question in queryset:
        for choice in question.choice_set.all():
            choice.votes = 0
            choice.save()


reset_all_votes.short_description = "Stimmen für die ausgewählte Fragen zurücksetzen"


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0
    readonly_fields = ('votes',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'total_votes', 'pub_date')
    inlines = [ChoiceInline]
    actions = [reset_all_votes]

    def total_votes(self, obj):
        return sum(choice.votes for choice in obj.choice_set.all())
    total_votes.short_description = "Gesamtstimmen"


admin.site.register(Question, QuestionAdmin)
