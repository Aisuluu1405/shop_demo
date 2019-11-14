from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import reverse, redirect

from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from webapp.models import Product, OrderProduct, Order


class IndexView(ListView):
    model = Product
    template_name = 'index.html'


class ProductView(DetailView):
    model = Product
    template_name = 'product/detail.html'


class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    template_name = 'product/create.html'
    fields = ('name', 'category', 'price', 'photo')
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.add_product'
    permission_denied_message = "Доступ запрещен"


class BasketChangeView(View):                    #метод заполнения корзины
    def get(self, request, *args, **kwargs):
        products = request.session.get('products', [])   #если в корзине есть товар, находим товар, если пустая корзина, создаем новый список товаров

        pk = request.GET.get('pk')            # достаем ключ добавляемого товара
        action = request.GET.get('action')       #добавляем из запроса действие(добавить или удалить товар)
        next_url = request.GET.get('next', reverse('webapp:index'))        # находим ссылку куда перекинуть

        if action == 'add':              #если добавить, добавляем
            products.append(pk)
        else:
            for product_pk in products:     #если нет , удаляем из списков товаров
                if product_pk == pk:
                    products.remove(product_pk)
                    break

        request.session['products'] = products                  #обновляем список товаров
        request.session['products_count'] = len(products)        #обновляем кол-во товаров

        return redirect(next_url)


class BasketView(CreateView):                                             #корзина
    model = Order
    fields = ('first_name', 'last_name', 'phone', 'email')    # так как нет formclass поля прописываем здесь
    template_name = 'product/basket.html'
    success_url = reverse_lazy('webapp:index')

    def get_context_data(self, **kwargs):
        basket, basket_total = self._prepare_basket()
        kwargs['basket'] = basket
        kwargs['basket_total'] = basket_total
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if self._basket_empty():
            form.add_error(None, 'В корзине отсутствуют товары!')
            return self.form_invalid(form)
        response = super().form_valid(form)
        self._save_order_products()
        self._clean_basket()
        return response

    def _prepare_basket(self):               #формирование корзины
        totals = self._get_totals()
        basket = []
        basket_total = 0
        for pk, qty in totals.items():
            product = Product.objects.get(pk=int(pk))
            total = product.price * qty
            basket_total += total
            basket.append({'product': product, 'qty': qty, 'total': total})
        return basket, basket_total

    def _get_totals(self):
        products = self.request.session.get('products', [])            #достаем список ключей товаров из сессии или пустой список, если корзина пустая
        totals = {}                                      #группировка ключей по кол-вуб подсчитывается кол-во каждого ключа
        for product_pk in products:                     # цикл проходитяс по всем ключам в списке ключей, и если ключ еще не учтен, заводит для него новую запись
            if product_pk not in totals:              #в словаре totals со значением =0
                totals[product_pk] = 0
            totals[product_pk] += 1          #Значение этой записи увеличивается на 1 за каждый совпадающий ключ товара в списке
        return totals

    def _basket_empty(self):
        products = self.request.session.get('products', [])
        return len(products) == 0

    def _save_order_products(self):
        totals = self._get_totals()
        for pk, qty in totals.items():
            OrderProduct.objects.create(product_id=pk, order=self.object, amount=qty)

    def _clean_basket(self):
        if 'products' in self.request.session:
            self.request.session.pop('products')
        if 'products_count' in self.request.session:
            self.request.session.pop('products_count')
