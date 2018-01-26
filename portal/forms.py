from django import forms
from .models import team

class create_team_form(forms.Form):

    class Meta:
        model = team
        fields = ['name','subtitle','year','under']

    def __init__(self, *args, **kwargs):
        super(create_team, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = ('Event name')

        for field_name in self.fields:
            field = self.fields.get(field_name)
            field.widget.attrs['placeholder'] = field.label