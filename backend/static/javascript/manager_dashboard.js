document.addEventListener('DOMContentLoaded', function () {
    fetchData();
});

function fetchData() {
    fetch('/get_info')
        .then(response => response.json())
        .then(data => {
            displayData(data);
            console.log(data)
        })
        .catch(error => console.error('Error fetching data:', error));
}

function displayData(data) {
    const container = document.getElementById('data-container');
    container.innerHTML = ''; // 清空現有內容

    Object.keys(data).forEach(key => {
        const section = document.createElement('section');
        const header = document.createElement('h2');
        header.textContent = key.charAt(0).toUpperCase() + key.slice(1); // 轉換標題
        section.appendChild(header);

        const table = document.createElement('table');
        const thead = document.createElement('thead');
        const tbody = document.createElement('tbody');
        table.appendChild(thead);
        table.appendChild(tbody);

        const headerRow = document.createElement('tr');
        const headers = ['Email', 'Position', 'Submit Time', 'Action'];
        headers.forEach(headerText => {
            const headerCell = document.createElement('th');
            headerCell.textContent = headerText;
            headerRow.appendChild(headerCell);
        });
        thead.appendChild(headerRow);

        data[key].forEach(item => {
            const row = document.createElement('tr');
            Object.entries(item).forEach(([key, value], index) => {
                const cell = document.createElement('td');
                // 檢查是否為"Action"列且該值存在
                if (headers[index] === 'Action' && value) {
                    // 創建一個按鈕
                    const button = document.createElement('button');
                    button.textContent = '審查';
                    button.onclick = function () {
                        // 點擊時跳轉
                        window.location.href = `/query_tag?tag=${value}`;
                    };
                    cell.appendChild(button);
                } else {
                    cell.textContent = value;
                }
                row.appendChild(cell);
            });
            tbody.appendChild(row);
        });

        section.appendChild(table);
        container.appendChild(section);
    });
}