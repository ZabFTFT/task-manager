from django import forms


class CreateTaskForm(forms.ModelForm):
    class Meta:
        fields = ["name", "description", "deadline", "priority", ]