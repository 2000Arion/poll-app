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
    reset_votes.short_description = "Stimmen zurücksetzen"
    fields = ('reset_votes', 'choice_text', 'votes')

    def save_model(self, request, obj, form, change):
        if f"reset_votes_{obj.pk}" in request.POST:
            obj.votes = 0
            obj.save()


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date')
    inlines = [ChoiceInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        for choice in obj.choice_set.all():
            if f"reset_votes_{choice.pk}" in request.POST:
                choice.votes = 0
                choice.save()


admin.site.register(Question, QuestionAdmin)
