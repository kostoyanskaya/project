import pytest
from django.urls import reverse
from rest_framework import status
from orders.models import Order
from rest_framework.test import APIClient
from api.serializers import OrderSerializer


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def order():
    """Создает тестовый заказ."""
    return Order.objects.create(
        table_number=1,
        items=[{'name': 'Бургер', 'price': 5.50}],
        status='pending'
    )


@pytest.fixture
def paid_order():
    """Создает тестовый оплаченный заказ."""
    return Order.objects.create(
        table_number=2,
        items=[{'name': 'Пицца', 'price': 10.00}],
        status='paid'
    )


@pytest.fixture
def order_data():
    """Данные для создания заказа."""
    return {
        'table_number': 3,
        'items': [{'name': 'Кофе', 'price': 3.00}],
        'status': 'pending'
    }


@pytest.mark.django_db
def test_order_list(api_client, order):
    """Проверяет получение списка заказов."""
    url = reverse('order-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert any(
        item['table_number'] == order.table_number
        for item in response.data['results']
    )


@pytest.mark.django_db
def test_order_create(api_client, order_data):
    """Проверяет создание нового заказа."""
    url = reverse('order-list')
    initial_count = Order.objects.count()
    response = api_client.post(url, order_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Order.objects.count() == initial_count + 1
    assert Order.objects.last().table_number == order_data['table_number']


@pytest.mark.django_db
def test_order_retrieve(api_client, order):
    """Проверяет получение конкретного заказа."""
    url = reverse('order-detail', args=[order.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['table_number'] == order.table_number


@pytest.mark.django_db
def test_order_update(api_client, order):
    """Проверяет обновление существующего заказа."""
    url = reverse('order-detail', args=[order.id])
    updated_data = {
        'table_number': 5,
        'items': [{'name': 'Чай', 'price': 2.00}],
        'status': 'ready'
    }
    response = api_client.put(url, updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    order.refresh_from_db()
    assert order.table_number == 5
    assert order.status == 'ready'


@pytest.mark.django_db
def test_total_revenue(api_client, paid_order):
    """Проверяет эндпоинт total_revenue."""
    url = reverse('order-total-revenue')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['total_revenue'] == paid_order.total_price


@pytest.mark.django_db
def test_search_by_status(api_client, order):
    """Проверяет поиск по статусу."""
    url = reverse('order-search') + f'?q={order.status}'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['status'] == order.status


@pytest.mark.django_db
def test_search_no_query(api_client):
    """Проверяет поиск без поискового запроса."""
    url = reverse('order-search')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['message'] == (
        "Укажите поисковой запрос (параметр 'q')."
    )


@pytest.mark.django_db
def test_order_serializer_validate_items_valid(order_data):
    """Проверяет валидацию items с корректными данными."""
    serializer = OrderSerializer(data=order_data)
    assert serializer.is_valid()


@pytest.mark.django_db
def test_order_serializer_validate_items_invalid_item_type():
    """Проверяет валидацию items с некорректным типом элемента."""
    invalid_data = {
        'table_number': 1,
        'items': ['строка'],
        'status': 'pending'
    }
    serializer = OrderSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'items' in serializer.errors
    assert serializer.errors['items'][0] == (
        "Каждый элемент списка блюд должен быть словарем."
    )


@pytest.mark.django_db
def test_order_serializer_validate_items_missing_keys():
    """Проверяет валидацию items с отсутствующими ключами."""
    invalid_data = {
        'table_number': 1,
        'items': [{'qty': 2}],
        'status': 'pending'
    }
    serializer = OrderSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'items' in serializer.errors
    assert serializer.errors['items'][0] == (
        "Каждый элемент должен содержать ключи 'name' и 'price'."
    )


@pytest.mark.django_db
def test_order_serializer_validate_items_invalid_name_type():
    """Проверяет валидацию items с некорректным типом имени."""
    invalid_data = {
        'table_number': 1,
        'items': [{'name': 123, 'price': 5.00}],
        'status': 'pending'
    }
    serializer = OrderSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'items' in serializer.errors
    assert serializer.errors['items'][0] == (
        "Название блюда должно быть строкой."
    )
