# products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required, user_passes_test
import matplotlib.pyplot as plt
import io, base64
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse 

def is_admin(user):
    return user.is_staff or user.is_superuser


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def all_products_api(request):
    # Fetch all products
    products = Product.objects.all()
    
    # Prepare the data to be returned
    data = [
        {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'sku': product.sku,
            'price': float(product.price),  # Convert Decimal to float for JSON compatibility
            'stock_level': product.stock_level,
            'reorder_level': product.reorder_level,
            'low_stock_alert': product.low_stock_alert,
            'needs_reorder': product.needs_reorder(),  # Call the dynamic method
        }
        for product in products
    ]
    
    return JsonResponse({'products': data}, safe=False)


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
    # Your view logic for rendering the product chart
    products = Product.objects.all()
    if not products.exists():
        return HttpResponse("No products available.", content_type="text/plain")
    product_names = [product.name for product in products]
    product_quantities = [product.stock_level for product in products]
    reorder_levels = [product.reorder_level for product in products]
    below_reorder_level = [
        product.stock_level < product.reorder_level for product in products
    ]
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_colors = ['red' if below else 'skyblue' for below in below_reorder_level]
    ax.bar(product_names, product_quantities, color=bar_colors)
    ax.set_xticks(range(len(product_names)))
    ax.set_xticklabels(product_names, rotation=45, ha='right')
    ax.set_title('Product Stock Levels', fontsize=16)
    ax.set_xlabel('Products', fontsize=12)
    ax.set_ylabel('Stock Levels', fontsize=12)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    return render(request, 'chart.html', {'chart': img_str})