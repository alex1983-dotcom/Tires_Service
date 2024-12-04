from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from .serializers import CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer
from django.core.mail import send_mail
from django.shortcuts import render
from django.views import View
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.http import JsonResponse


class CategoryListView(View):
    """
    Представление для отображения списка категорий товаров.
    """
    def get(self, request):
        """
        Обрабатывает GET-запрос для отображения списка категорий.
        """
        categories = Category.objects.all()
        return render(request, 'shop/category_list.html', {'categories': categories})

class CategoryProductsView(View):
    """
    Представление для отображения списка товаров в категории.
    """
    def get(self, request, category_id):
        """
        Обрабатывает GET-запрос для отображения списка товаров в категории.
        """
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category)
        return render(request, 'shop/category_products.html', {'category': category, 'products': products})


class ProductListView(View):
    """
    Представление для отображения списка товаров.
    """
    def get(self, request):
        """
        Обрабатывает GET-запрос для отображения списка товаров.
        """
        products = Product.objects.all()
        return render(request, 'shop/product_list.html', {'products': products})


@method_decorator(login_required, name='dispatch')
class CartDetailView(View):
    """
    Представление для отображения деталей корзины.
    """
    def get(self, request):
        """
        Обрабатывает GET-запрос для отображения деталей корзины.
        """
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'shop/cart_detail.html', {'cart': cart, 'cart_items': cart_items, 'total_price': total_price})

    def post(self, request):
        """
        Обрабатывает POST-запрос для обновления количества товаров в корзине.
        """
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            item_id = request.POST.get(f'item_id_{item.id}')
            quantity = request.POST.get(f'quantity_{item.id}')
            if item_id and quantity:
                item.quantity = int(quantity)
                item.save()
        return redirect('cart-detail')


@method_decorator(login_required, name='dispatch')
class AddToCartView(View):
    """
    Представление для добавления товара в корзину.
    """
    def post(self, request, product_id):
        """
        Обрабатывает POST-запрос для добавления товара в корзину.
        """
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_item.quantity = 1
        else:
            cart_item.quantity += 1
        cart_item.save()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Товар добавлен в корзину'})
        else:
            return redirect(request.META.get('HTTP_REFERER', reverse('category-products', args=[product.category.id])))


@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    """
    Представление для оформления заказа.
    """
    def post(self, request):
        """
        Обрабатывает POST-запрос для оформления заказа.
        """
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        try:
            order = Order.objects.create(
                user=request.user,
                cart=cart
            )

            order_items = []
            total_price = 0
            for item in cart_items:
                order_item = OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                order_items.append(order_item)
                total_price += item.product.price * item.quantity

            cart_items.delete()

            order_details = '\n'.join([f"{item.quantity} x {item.product.name} - {item.price} руб." for item in order_items])
            email_body = f"Ваш заказ #{order.id} был обработан и находится в обработке.\n\n" \
                         f"Детали заказа:\n{order_details}\n\n" \
                         f"Общая сумма: {total_price} руб."

            send_mail(
                'Заказ обработан',
                email_body,
                'alebarda2018@gmail.com',
                [request.user.email],
                fail_silently=False,
            )
            return redirect('order-success', order_id=order.id)
        except Exception as e:
            print("Error processing order:", e)
            return render(request, 'shop/order_error.html', {'error': str(e)})


@method_decorator(login_required, name='dispatch')
class ClearCartView(View):
    """
    Представление для очистки корзины.
    """
    def post(self, request):
        """
        Обрабатывает POST-запрос для очистки корзины.
        """
        cart = get_object_or_404(Cart, user=request.user)
        CartItem.objects.filter(cart=cart).delete()
        return redirect('cart-detail')


class OrderSuccessView(View):
    """
    Представление для отображения страницы успешного заказа.
    """
    def get(self, request, order_id):
        """
        Обрабатывает GET-запрос для отображения страницы успешного заказа.
        """
        order = get_object_or_404(Order, id=order_id, user=request.user)
        return render(request, 'shop/order_success.html', {'order': order})


class CategoryList(APIView):
    """
    Представление для получения списка всех категорий.
    """
    def get(self, request):
        """
        Обрабатывает GET-запрос для получения списка всех категорий.
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Обрабатывает POST-запрос для создания новой категории.
        """
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductList(APIView):
    """
    Представление для получения списка всех товаров.
    """
    def get(self, request):
        """
        Обрабатывает GET-запрос для получения списка всех товаров.
        """
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Обрабатывает POST-запрос для создания нового товара.
        """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetail(APIView):
    """
    Представление для получения деталей корзины текущего пользователя.
    """
    def get(self, request):
        """
        Обрабатывает GET-запрос для получения деталей корзины текущего пользователя.
        """
        cart = get_object_or_404(Cart, user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCart(APIView):
    """
    Представление для добавления товара в корзину.
    """
    def post(self, request, product_id):
        """
        Обрабатывает POST-запрос для добавления товара в корзину.
        """
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_item.quantity = 1
        else:
            cart_item.quantity += 1
        cart_item.save()
        return Response({'status': 'added to cart'}, status=status.HTTP_200_OK)


class Checkout(APIView):
    """
    Представление для оформления заказа.
    """
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        order = Order.objects.create(user=request.user, cart=cart)
        cart_items.update(cart=None)  # Освобождаем корзину для нового заказа
        try:
            send_mail(
                'Заказ обработан',
                f'Ваш заказ #{order.id} был обработан и находится в обработке.',
                'from@example.com',
                [request.user.email],
                fail_silently=False,
            )
            return Response({'status': 'order placed', 'order_id': order.id}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Ошибка при отправке письма: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
