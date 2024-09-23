document.getElementById('fetch_btn').addEventListener('click', function() {
    const stockId = document.getElementById('stock_id').value;
    fetch('/get_stock', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ stock_id: stockId })
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = '';
        if (data.length === 0) {
            resultDiv.innerHTML = '<p>無法取得資料，請檢查股票代號。</p>';
        } else {
            const table = document.createElement('table');
            table.innerHTML = '<tr><th>日期</th><th>股號</th>' + Object.keys(data[0]).slice(2).map(key => `<th>${key}</th>`).join('') + '</tr>';
            data.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `<td>${item.日期}</td><td>${item.股號}</td>` + Object.values(item).slice(2).map(value => `<td>${value}</td>`).join('');
                table.appendChild(row);
            });
            resultDiv.appendChild(table);
        }
    });
});
