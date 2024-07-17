from django.db import models
from account.models import User

from django.db import models

class AcademicYear(models.Model):
    academic_year = models.CharField(max_length=15, unique=True)  
    eval_accepting = models.BooleanField(default=True)

    def __str__(self):
        return self.academic_year

class Module(models.Model):
    module_code = models.CharField(max_length=50)
    module_name = models.CharField(max_length=250)
    module_leader = models.CharField(max_length=250)
    created_at = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['module_code']
    
    def __str__(self):
        return f'{self.module_code} ({self.module_name})'
    
    
class ModuleReview(models.Model):
    module = models.ForeignKey(Module, related_name='module_review', on_delete=models.CASCADE)
    module_details = models.CharField(max_length=150)
    school = models.CharField(max_length=150)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    student_nap = models.TextField(blank=True, null=True)
    evolution_to_teaching = models.TextField(blank=True, null=True)
    evolution_of_op_module = models.TextField(blank=True, null=True)
    inclusive_nature_of_curriculum = models.TextField(blank=True, null=True)
    past_changes = models.TextField(blank=True, null=True)
    future_changes = models.TextField(blank=True, null=True)
    other_comment = models.TextField(default='None')
    completed =models.BooleanField(default=False)
    completed_by = models.CharField(max_length=250)
    completion_date = models.DateField(auto_now=True)  # Renamed from date_completed

    class Meta:
        ordering = ['academic_year']

    def __str__(self):
        return f'{self.module.module_code} ({self.module.module_name})'
    
    
    
    
class Program(models.Model):
    program_code = models.CharField(max_length=50, blank=True, null=True)
    program_name = models.CharField(max_length=250)
    program_leader = models.CharField(max_length=250)
    created_at = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['program_code']
        
    def save(self, *args, **kwargs):
        if not self.program_code:
            self.program_code = self._generate_program_code()
        super().save(*args, **kwargs)

    def _generate_program_code(self):
        last_report = Program.objects.order_by('id').last()
        new_id = 1 if not last_report else last_report.id + 1
        return f'{new_id:03d}'
    
    def __str__(self):
        return f'{self.program_code} ({self.program_name})'
    
    
class ProgramReview(models.Model):
    program = models.ForeignKey(Program, related_name='program_review', on_delete=models.CASCADE)
    program_details = models.CharField(max_length=150)
    school = models.CharField(max_length=150)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    student_nap = models.TextField(blank=True, null=True)
    evolution_to_teaching = models.TextField(blank=True, null=True)
    evolution_of_op_program = models.TextField(blank=True, null=True)
    inclusive_nature_of_curriculum = models.TextField(blank=True, null=True)
    past_changes = models.TextField(blank=True, null=True)
    future_changes = models.TextField(blank=True, null=True)
    other_comment = models.TextField(default='None')
    completed = models.BooleanField(default=False)
    completed_by = models.CharField(max_length=250)
    completion_date = models.DateField(auto_now=True) 
    
    class Meta:
        ordering = ['academic_year']

    def __str__(self):
        return f'{self.program.program_code} ({self.program.program_name})'

