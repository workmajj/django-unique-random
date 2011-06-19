from django.contrib import admin

from unique_random.models import UniqueRandom, UniqueRandomAdmin

admin.site.register(UniqueRandom, UniqueRandomAdmin)
