from ajax_select.fields import AutoCompleteSelectMultipleField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from .models import Host, Guest


def validate_word_count(value):
    if len(value.split()) < 5:
        raise ValidationError(
            '%(value)s is too short. We need at least 5 words',
            params={'value': value},
        )

class FriendFeedbackForm(forms.Form):
    rating = forms.IntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    feedback = forms.Field(
        widget=forms.Textarea(),
        validators=[
            MinLengthValidator(20, message="Please provide more details"),
            validate_word_count
        ]
    )


class HostForm(forms.ModelForm):
    hobbies = AutoCompleteSelectMultipleField('hobbies')

    class Meta:
        model = Host
        exclude = ('state', )


class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ('name', 'desired_order_value', 'hobbies')
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #
    #     # self.helper.form_id = 'id-exampleForm'
    #     # self.helper.form_class = 'blueForms'
    #     # self.helper.form_method = 'post'
    #     # self.helper.form_action = 'submit_survey'
    #     #
    #     # self.helper.add_input(Submit('submit', 'Submit'))
