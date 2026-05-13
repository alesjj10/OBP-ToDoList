from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status', 'tags']

        widgets = {

            'title': forms.TextInput(attrs={
                'class': 'form-control rounded-pill'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),

            'due_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),

            'status': forms.Select(attrs={
                'class': 'form-select'
            }),

            'tags': forms.CheckboxSelectMultiple(),
        }