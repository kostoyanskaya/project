$(document).ready(function() {
    const API_URL = '/api/orders/';
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function fetchOrders() {
        $.ajax({
            url: API_URL,
            method: 'GET',
            success: function(data) {
                displayOrders(data);
            },
            error: function(error) {
                console.error('Ошибка при получении заказов:', error);
                alert('Не удалось получить список заказов.');
            }
        });
    }

    function displayOrders(data) {
        const orders = data.results ? data.results : data;
        const container = $('#orders-container');
        container.empty();
    
        if (!Array.isArray(orders)) {
            console.error("Ожидался массив заказов, но получен:", orders);
            alert("Произошла ошибка при отображении заказов. Проверьте консоль.");
            return;
        }
    
        orders.forEach(order => {
            const itemsString = order.items.map(item => `${item.name} ${item.price}`).join(', ');
            const card = $(`
                <div class="order-card">
                    <h3>Заказ №${order.id}</h3>
                    <p>Номер стола: ${order.table_number}</p>
                    <p>Список блюд: ${itemsString}</p>
                    <p>Общая стоимость: ${order.total_price}</p>
                    <p>Статус: ${order.status}</p>
                    <div class="order-actions">
                        <select class="status-select" data-order-id="${order.id}">
                            <option value="pending" ${order.status === 'pending' ? 'selected' : ''}>В ожидании</option>
                            <option value="ready" ${order.status === 'ready' ? 'selected' : ''}>Готово</option>
                            <option value="paid" ${order.status === 'paid' ? 'selected' : ''}>Оплачено</option>
                        </select>
                        <button class="delete-button" data-order-id="${order.id}">Удалить</button>
                    </div>
                </div>
            `);
            container.append(card);
        });
    }
    
    $(document).on('change', '.status-select', function() {
        const orderId = $(this).data('order-id');
        const newStatus = $(this).val();
    
        $.ajax({
            url: `${API_URL}${orderId}/`,
            method: 'PATCH',
            data: JSON.stringify({ status: newStatus }),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(data) {
                console.log('Статус заказа успешно изменен:', data);
                fetchOrders();
            },
            error: function(error) {
                console.error('Ошибка при изменении статуса заказа:', error);
                alert('Не удалось изменить статус заказа.');
            }
        });
    });

    $(document).on('click', '.delete-button', function() {
        const orderId = $(this).data('order-id');
        $.ajax({
            url: `${API_URL}${orderId}/`,
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(data) {
                fetchOrders();
            },
            error: function(error) {
                console.error('Ошибка при удалении заказа:', error);
                alert('Не удалось удалить заказ.');
            }
        });
    });
    $('#search-button').click(function() {
        const query = $('#search-input').val();
        if (query) {
            $.ajax({
                url: `${API_URL}search/?q=${query}`,
                method: 'GET',
                success: function(data) {
                    displayOrders(data);
                },
                error: function(error) {
                    console.error('Ошибка при поиске заказов:', error);
                    alert('Не удалось выполнить поиск.');
                }
            });
        } else {
            fetchOrders();
        }
    });

    fetchOrders();
});
