# products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_staff or user.is_superuser


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


@login_required
@user_passes_test(is_admin) 
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()  # Save the product instance

            # Check stock level and display a warning if it's low
            if product.stock_level <= product.reorder_level:
                messages.warning(request, f'Low stock alert for: {product.name}')

            return redirect('product_list')
        else:
            return render(request, 'products/product_form.html', {'form': form})
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})


@login_required
@user_passes_test(is_admin) 
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form})

@login_required
@user_passes_test(is_admin) 
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})


@login_required
@user_passes_test(is_admin)
def check_reorder_levels(request):
    products = Product.objects.all()
    low_stock_products = []

    for product in products:
        if product.quantity <= product.reorder_level:
            low_stock_products.append(product)

    if low_stock_products:
        messages.warning(request, 'The following products need to be restocked: {}'.format(', '.join([product.name for product in low_stock_products])))

    return render(request, 'products/check_reorder_levels.html', {'low_stock_products': low_stock_products})