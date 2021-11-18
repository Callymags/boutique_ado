from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product

# Create your views here.

def view_bag(request):
    """ A view to return the bag contents page """ 

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
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
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')

            else: 
                # If not, add new item with size to basket
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added size {size.upper()} {product.name} to your bag')

        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added size {size.upper()} {product.name} to your bag')

    # If item doesn't have a size
    else: 
        # Increase quantity of item in bag if item id is already in bag
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')

        else:     
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
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
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')


        # Remove the item from bag if quantity = 0
        else:
            del bag[item_id]['items_by_size'][size]
            # If only size in bag, remove item id so that there is not an empty 'items_by_size' dictionary
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
    # If item doesn't have a size
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:     
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')


    request.session['bag'] = bag
    # Redirect back to bag url using reverse function
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None 
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        # If item has size
        if size:
            # Remove only the specific size requested
            del bag[item_id]['items_by_size'][size]
            # If only size in bag, remove item id so that there is not an empty 'items_by_size' dictionary
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')

        # If item doesn't have a size
        else:  
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')


        request.session['bag'] = bag
        # Redirect back to bag url using reverse function
        return HttpResponse(status=200)
        
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
