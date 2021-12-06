from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # Fields that will be automatically calculated not included here
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated labels 
        and set autofocus on first field
        """  
        # Call the default init method to set the form up as it would be by default
        super().__init__(*args, **kwargs)
        # Update template display to have cleaner placeholder text 
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }

        # Autofocus will start in Full name field as it is set to true
        self.fields['full_name'].widget.attrs['autofocus'] = True
        # Iterate through form fields
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    # Add a star to field if it is required
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                # Set all fields to their values using placeholders dict above on line 21
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # Remove form field labels as custom placeholders have been added
            self.fields[field].label = False