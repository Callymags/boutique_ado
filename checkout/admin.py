from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    # When we look at order, we can see list of editable line items on same page
    # rather than having to go to the OrderLineItem interface
    model = OrderLineItem
    # Make the line_item total read only 
    read_only_fields = ('lineitem_total',)



class OrderAdmin(admin.ModelAdmin):
    # Add lineitem total to Order Admin interface 
    inlines = (OrderLineItemAdminInline,)
    # Users will not be able to input info in these fields as these settings are 
    # calculated by the methods in models.py
    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total',)

    # Allows us to specify the order of the field in the admin interface
    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country', 
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total',)

    # Restrict the columns that show up in the order list to only a few key items
    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost', 'grand_total',)

    # Set the most recent orders to the top
    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)
