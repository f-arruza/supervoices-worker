from django.contrib import admin
from .models import Competition, Voice, Winner


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', )


@admin.register(Voice)
class VoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'competition_id', 'author_firstname')


@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    pass
