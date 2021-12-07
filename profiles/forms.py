from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # Fields that will be automatically calculated not included here
        exclude = ('user',)
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated labels 
        and set autofocus on first field
        """  
        # Call the default init method to set the form up as it would be by default
        super().__init__(*args, **kwargs)
        # Update template display to have cleaner placeholder text 
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        # Autofocus will start in Full name field as it is set to true
        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        # Iterate through form fields
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    # Add a star to field if it is required
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                # Set all fields to their values using placeholders dict above on line 21
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            # Remove form field labels as custom placeholders have been added
            self.fields[field].label = False