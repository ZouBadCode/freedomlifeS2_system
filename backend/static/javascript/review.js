document.getElementById('deny-button').addEventListener('click', function() {
    // 創建彈出視窗元素
    var popup = document.createElement('div');
    popup.classList.add('popup');

    var overlay = document.createElement('div');
    overlay.classList.add('overlay');
    // 彈出視窗內容
    popup.innerHTML = `
        <div class="popup-content">
            <p>你確定要執行此動作嗎？</p>
            <button id="confirmButton">確定</button>
            <button id="cancelButton">取消</button>
        </div>
    `;

    overlay.appendChild(popup);
    // 添加到文檔主體

    document.body.appendChild(overlay);


    document.getElementById('confirmButton').addEventListener('click', function() {
        var fields = document.getElementsByClassName('field');
        var tagValue = '';
        var dataTypeValue = '';
    
        // 遍歷這些元素來尋找特定的 'field-name'
        for(var i = 0; i < fields.length; i++) {
            var fieldName = fields[i].getElementsByClassName('field-name')[0].innerText;
            var fieldValue = fields[i].getElementsByClassName('field-value')[0].innerText;
    
            // 檢查 fieldName 是否為 'Tag' 或 'dataType'，並保存相應的 fieldValue
            if(fieldName === 'Tag') {
                tagValue = fieldValue;
            } else if(fieldName === 'dataType') {
                dataTypeValue = fieldValue;
            } else if(fieldName === 'DiscordUsername'){
                DiscordUsernameValue = fieldValue;
            }
        }
    
    
    
        fetch('/deny-user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                dataType: dataTypeValue,
                Tag: tagValue,
                DiscordUsername: DiscordUsernameValue
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            alert('更新成功！');
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('更新失敗，請檢查控制台了解詳情。');
        });
    });
    // 點擊確定按鈕的處理程序
    document.getElementById('confirmButton').addEventListener('click', function() {
        // 在此添加執行確認操作的代碼
        console.log('確認操作已執行');
        // 關閉彈出視窗
        document.body.removeChild(overlay);

    });

    // 點擊取消按鈕的處理程序
    document.getElementById('cancelButton').addEventListener('click', function() {
        // 在此添加取消操作的代碼（如果需要）
        console.log('取消操作');
        // 關閉彈出視窗
        document.body.removeChild(overlay);
    });
});


document.getElementById('consent-button').addEventListener('click', function() {
    // 創建彈出視窗元素
    var popup = document.createElement('div');
    popup.classList.add('popup');

    var overlay = document.createElement('div');
    overlay.classList.add('overlay');
    // 彈出視窗內容
    popup.innerHTML = `
        <div class="popup-content">
            <p>你確定要執行此動作嗎？</p>
            <button id="confirmButton">確定</button>
            <button id="cancelButton">取消</button>
        </div>
    `;

    overlay.appendChild(popup);
    // 添加到文檔主體

    document.body.appendChild(overlay);


    document.getElementById('confirmButton').addEventListener('click', function() {
        var fields = document.getElementsByClassName('field');
        var tagValue = '';
        var dataTypeValue = '';
    
        // 遍歷這些元素來尋找特定的 'field-name'
        for(var i = 0; i < fields.length; i++) {
            var fieldName = fields[i].getElementsByClassName('field-name')[0].innerText;
            var fieldValue = fields[i].getElementsByClassName('field-value')[0].innerText;
    
            // 檢查 fieldName 是否為 'Tag' 或 'dataType'，並保存相應的 fieldValue
            if(fieldName === 'Tag') {
                tagValue = fieldValue;
            } else if(fieldName === 'dataType') {
                dataTypeValue = fieldValue;
            }else if(fieldName === 'DiscordUsername'){
                DiscordUsernameValue = fieldValue;
            }
        }
    
    
    
        fetch('/accept-user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                dataType: dataTypeValue,
                Tag: tagValue,
                DiscordUsername: DiscordUsernameValue
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            alert('更新成功！');
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('更新失敗，請檢查控制台了解詳情。');
        });
    });
    // 點擊確定按鈕的處理程序
    document.getElementById('confirmButton').addEventListener('click', function() {
        // 在此添加執行確認操作的代碼
        console.log('確認操作已執行');
        // 關閉彈出視窗
        document.body.removeChild(overlay);

    });

    // 點擊取消按鈕的處理程序
    document.getElementById('cancelButton').addEventListener('click', function() {
        // 在此添加取消操作的代碼（如果需要）
        console.log('取消操作');
        // 關閉彈出視窗
        document.body.removeChild(overlay);
    });
});