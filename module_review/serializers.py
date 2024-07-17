from rest_framework import serializers
from module_review.models import Module, ModuleReview, Program, ProgramReview, AcademicYear


class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = ['id', 'academic_year', 'eval_accepting']


class ModuleReviewSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = ModuleReview
        fields = [
            'id', 'module', 'module_details', 'academic_year', 'school', 'student_nap',
            'evolution_to_teaching', 'past_changes', 'future_changes',
            'evolution_of_op_module', 'inclusive_nature_of_curriculum',
            'other_comment', 'completed', 'completed_by', 'completion_date'
        ]
        read_only_fields = ['completed', 'completion_date']

    def create(self, validated_data):
        validated_data['completed'] = True
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['completed'] = True
        return super().update(instance, validated_data)



class ModuleSerializer(serializers.ModelSerializer):
    module_reviews = ModuleReviewSerializer(many=True, read_only=True, source='module_review')

    class Meta:
        model = Module
        fields = ['id', 'module_code', 'module_name', 'module_leader', 'created_at', 'module_reviews']
     
        
        

# =========================================Program ===================================================

class ProgramReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProgramReview
        fields = [
            'id', 'program', 'program_details', 'academic_year', 'school', 'student_nap',
            'evolution_to_teaching', 'past_changes', 'future_changes',
            'evolution_of_op_program', 'inclusive_nature_of_curriculum',
            'other_comment', 'completed', 'completed_by', 'completion_date'
        ]
        read_only_fields = ['completed', 'completion_date']

    def create(self, validated_data):
        validated_data['completed'] = True
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['completed'] = True
        return super().update(instance, validated_data)



class ProgramSerializer(serializers.ModelSerializer):
    program_reviews = ProgramReviewSerializer(many=True, read_only=True, source='program_review')

    class Meta:
        model = Program
        fields = ['id', 'program_code', 'program_name', 'program_leader', 'created_at', 'program_reviews']