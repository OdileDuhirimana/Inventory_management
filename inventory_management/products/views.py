# products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required, user_passes_test
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
from django.contrib import messages

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
        if product.stock_level <= product.reorder_level:
            low_stock_products.append(product)

    if low_stock_products:
        messages.warning(request, 'The following products need to be restocked: {}'.format(', '.join([product.name for product in low_stock_products])))

    return render(request, 'products/check_reorder_levels.html', {'low_stock_products': low_stock_products})

# views.py


@login_required
@user_passes_test(is_admin)
def product_chart(request):
    # Get the data
    products = Product.objects.all()
    product_names = [product.name for product in products]
    product_quantities = [product.stock_level for product in products]

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))  # Increase the figure size to give more space
    ax.bar(product_names, product_quantities)

    # Rotate the x-axis labels to make them more readable
    ax.set_xticklabels(product_names, rotation=45, ha='right')

    # Add a title to the chart
    ax.set_title('Analytics', fontsize=16)

    # Improve layout to prevent clipping of labels
    plt.tight_layout()

    # Save it to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Return the image in the response
    return HttpResponse(buf, content_type='image/png')


