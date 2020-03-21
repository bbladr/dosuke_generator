from django.contrib import admin
from .models import Band, Member, Config

@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    pass
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass
@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    pass