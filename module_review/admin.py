from django.contrib import admin
from .models import Module, Program, ModuleReview, ProgramReview, AcademicYear

admin.site.register(Module)
admin.site.register(Program)
admin.site.register(ModuleReview)
admin.site.register(ProgramReview)
admin.site.register(AcademicYear)