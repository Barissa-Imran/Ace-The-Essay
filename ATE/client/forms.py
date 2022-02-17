from django import forms
from .models import ProjectOrder

# client Project order form----------------
# view admin.py for admin form


class ProjectOrderForm(forms.ModelForm):
    class Meta:
        model = ProjectOrder
        fields = [
            'academic_level',
            'type_of_paper',
            'subject_area',
            'title',
            'paper_instructions',
            'Additional_materials',
            'paper_format',
            'number_of_pages',
            'spacing',
            'price',
            'deadline'
        ]
