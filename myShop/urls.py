

from .views import HomePageView, CustomersListView, OrdersListView, SearchView, ProductListView

from django.urls import path

app_name = 'myshop'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('customers/', CustomersListView.as_view(), name='customers'),
    path('orders/', OrdersListView.as_view(), name='orders'),
    path('search/', SearchView.as_view(), name='search'),
    path('product_list/', ProductListView.product_list, name='product_list'),
    path('<slug:category_slug>/', ProductListView.product_list,
         name='product_list_by_category'
         ),
    path('<int:id>/<slug:slug>', ProductListView.product_detail,
         name='product_detail'),
]




