/* script.js */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function () {
    let itemCount = 1;

    // Привязываем событие клика к кнопке с классом ".add-item-btn"
    $('.add-item-btn').on('click', function () {
        const newItemRow = `
            <div class="item-row">
                <input type="text" placeholder="Блюдо" class="item-input" required>
                <input type="number" step="any" min="0" placeholder="Цена" class="item-input" required>
                <button type="button" class="btn btn-danger remove-item-btn">X</button>
            </div>
        `;
        $('#items-container').append(newItemRow);
        itemCount++;
    });

    $(document).on('click', '.remove-item-btn', function () {
        $(this).closest('.item-row').remove();
        itemCount--;
    });

    $('#order-form').on('submit', function (e) {
        e.preventDefault();
        const tableNumber = $('#table-number').val();
        const items = [];

        $('.item-row').each(function () {
            const dishName = $(this).find('input[type="text"]').val();
            const price = parseFloat($(this).find('input[type="number"]').val());
            if (dishName && price > 0) {
                items.push({ name: dishName, price: price });
            }
        });

        if (!tableNumber || !items.length) {
            $('#error-message').text('Заполните все обязательные поля.');
            return;
        }

        $.ajax({
            url: '/api/orders/',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                table_number: tableNumber,
                items: items
            }),
            success: function (response) {
                window.location.href = '/total-list/';
            },
            error: function (xhr, status, error) {
                $('#error-message').text(xhr.responseText);
            }
        });
    });
});
