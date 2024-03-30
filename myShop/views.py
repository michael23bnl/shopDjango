from django.views.generic import TemplateView
from django.views.generic.list import ListView
from myShop.models import Customer, Order, Category, Product
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm

class HomePageView(TemplateView):
    template_name = 'home.html'

class CustomersListView(ListView):
    template_name = "customer.html"
    model = Customer
    context_object_name = "list_of_all_customers"

class OrdersListView(ListView):
    template_name = "orders.html"
    model = Order
    context_object_name = "list_of_all_orders"

class SearchView(ListView):
    template_name = "search.html"
    model = Order
    context_object_name = "list_of_all_orders"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is None:
            return
        splittedQuery = query.rstrip().split()
        if len(splittedQuery) > 1:
            firstName = splittedQuery[0]
            lastName = splittedQuery[1]
            return Order.objects.filter(
                Q(customer__first_name__icontains=firstName) and Q(customer__last_name__icontains=lastName)
            ).order_by('order_date').reverse()
        return Order.objects.filter(
            Q(customer__first_name__icontains=query) | Q(customer__last_name__icontains=query)
        ).order_by('order_date').reverse()

class ProductListView(ListView):
    template_name = "base.html"
    model = Product
    context_object_name = "list_of_all_products"

    def product_list(request, category_slug=None):
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'shop/product/list.html',
                      {
                          'category': category,
                          'categories': categories,
                          'products': products
                      })

    def product_detail(request, id, slug):
        product = get_object_or_404(Product, id=id, slug=slug, available=True)
        cart_product_form = CartAddProductForm()
        return render(request, 'shop/product/detail.html', {'product': product,
                                                            'cart_product_form': cart_product_form})
