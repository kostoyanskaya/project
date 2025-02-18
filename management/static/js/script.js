document.getElementById('calculate-revenue').addEventListener('click', function() {
    fetch('/api/orders/total_revenue/')  // Обратите внимание на правильный путь
        .then(response => {
            if (!response.ok) {
                throw new Error('Сеть не в порядке');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('total-revenue').innerText = data.total_revenue.toFixed(2);
        })
        .catch(error => console.error('Ошибка:', error));
});