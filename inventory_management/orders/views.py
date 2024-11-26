from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Order
from django.contrib import messages
from .forms import OrderForm
from products.models import Product  
from django.http import JsonResponse

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
def order_list(request):
    print(f"Current user ID: {request.user.id}")
    if request.user.is_staff:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)

    print("Orders retrieved:", orders) 
    return render(request, 'orders/order_list.html', {'orders': orders})


def all_orders_api(request):
    orders = Order.objects.all()   
    data = [
        {
            'product': order.product,
            'quantity': order.quantity,
            'date': order.created_at,
        }
        for order in orders
    ]
    
    return JsonResponse({'orders': data}, safe=False)

@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']  # Get the requested quantity from the form
            product = form.cleaned_data['product']  # Get the related product from the form
            
            # Check if enough stock is available
            if quantity <= product.stock_level:
                order = form.save(commit=False)  # Create the order instance but don't save yet
                order.user = request.user  # Set the user to the currently logged-in user
                product.stock_level -= quantity  # Reduce the stock level by the ordered quantity
                product.save()  # Save the updated product stock level
                order.save()  # Now save the order to the database
                return redirect('order_list')
            else:
                form.add_error('quantity', 'Not enough stock available.')  # Add an error if stock is insufficient
    else:
        form = OrderForm()
    
    return render(request, 'orders/order_form.html', {'form': form})


@login_required
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)  # Retrieve the order
    product = order.product  # Get the related product

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)  # Populate the form with the existing order data
        if form.is_valid():
            new_quantity = form.cleaned_data['quantity']  # Get the new quantity from the form
            stock_change = new_quantity - order.quantity  # Calculate the change in stock

            # Check if the new quantity exceeds the available stock
            if new_quantity > product.stock_level:
                form.add_error('quantity', 'Cannot update to a quantity greater than available stock.')
            else:
                product.stock_level -= stock_change  # Update stock level
                product.save()  # Save the updated product
                order = form.save()  # Save the order if stock is sufficient
                return redirect('order_list')

    else:
        form = OrderForm(instance=order)  # Populate the form with the existing order data for GET requests

    return render(request, 'orders/order_form.html', {'form': form})  # Render the form with any errors


@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.delete()
        return redirect('order_list')
    return render(request, 'orders/order_confirm_delete.html', {'order': order})

@login_required
def view_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})  # Create a new template for order details.

@login_required
@user_passes_test(is_admin)
def order_approve(request, pk):
    order = get_object_or_404(Order, pk=pk)
    product = order.product

    # Prevent double approval
    if order.is_approved:
        messages.info(request, 'Order has already been approved.')
        return redirect('order_list')

    # Check stock availability
    if product.stock_level >= order.quantity:
        # Update product stock and save
        product.stock_level -= order.quantity
        product.save()

        # Approve the order
        order.is_approved = True
        order.status = 'Approved'
        order.save()

        messages.success(request, 'Order approved successfully.')

        # Check if stock level is low after approval
        if product.stock_level <= product.reorder_level:
            messages.warning(request, f'Low stock alert for: {product.name}')

    else:
        messages.error(request, 'Not enough stock to fulfill this order.')

    return redirect('order_list')