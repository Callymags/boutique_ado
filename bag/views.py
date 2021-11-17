from django.shortcuts import render, redirect, reverse

# Create your views here.

def view_bag(request):
    """ A view to return the bag contents page """ 

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None 
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    # If item has size
    if size:
        if item_id in list(bag.keys()):
            # Checks if there is another item with same id and size 
            if size in bag[item_id]['items_by_size'].keys():
                # If so, increment quantity of size
                bag[item_id]['item_by_size'][size] += quantity
            else: 
                # If not, add new item with size to basket
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    # If item doesn't have a size
    else: 
        # Increase quantity of item in bag if item id is already in bag
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:     
            bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    size = None 
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    # If item has size
    if size:
        # Set the items new quantity if quantity is above 0
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        # Remove the item from bag if quantity = 0
        else:
            del bag[item_id]['items_by_size'][size]
    # If item doesn't have a size
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:     
            bag.pop(item_id)

    request.session['bag'] = bag
    # Redirect back to bag url using reverse function
    return redirect(reverse('view_bag'))

