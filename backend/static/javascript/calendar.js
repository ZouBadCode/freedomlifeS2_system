let calendar = document.getElementById("calendar");
let showCalendarButton = document.querySelector(".show-calendar-button");
document.querySelector(".close-calendar").addEventListener("click", function () {
    calendar.style.display = "none";
});
showCalendarButton.onclick = function () {
    calendar.style.display = "block";
    fetchDate();
};

// 實現可移動的功能
dragElement(calendar);

function dragElement(element) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    if (document.querySelector(".calendar-header")) {
        // 如果存在，則在header上應用拖動功能
        document.querySelector(".calendar-header").onmousedown = dragMouseDown;
    } else {
        // 否則，在整個元素上應用拖動功能
        element.onmousedown = dragMouseDown;
    }

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // 獲取滑鼠游標的初始位置
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // 當滑鼠游標移動時，調用元素位置重新計算的函數
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // 計算滑鼠的新位置
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // 設置元素的新位置
        element.style.top = (element.offsetTop - pos2) + "px";
        element.style.left = (element.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        // 停止移動時停止執行這些動作
        document.onmouseup = null;
        document.onmousemove = null;
    }
}

// 添加日曆生成和切換月份的功能...
const monthYear = document.querySelector('.month-year');
const prevMonthButton = document.querySelector('.prev-month');
const nextMonthButton = document.querySelector('.next-month');
const calendarBody = document.querySelector('.calendar-body');

let currentDate = new Date();

function renderCalendar(gapDayRemindDate, nextGapDayReturnDate) {
    const today = new Date();
    const todayDate = today.getDate(); // 獲取今天的日期（日）
    const todayMonth = today.getMonth(); // 獲取今天的月份
    const todayYear = today.getFullYear(); // 獲取今天的年份
    console.log(today)


    const gapDayRemind = {
        year: gapDayRemindDate.getFullYear(),
        month: gapDayRemindDate.getMonth(),
        date: gapDayRemindDate.getDate()
    };

    const nextGapDayReturn = {
        year: nextGapDayReturnDate.getFullYear(),
        month: nextGapDayReturnDate.getMonth(),
        date: nextGapDayReturnDate.getDate()
    };


    
    const monthDays = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate();
    const firstDayIndex = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay();

    let daysHtml = '';
    for (let i = 0; i < firstDayIndex; i++) {
        daysHtml += '<div></div>'; // 填充空白，直到第一天
    }

    for (let day = 1; day <= monthDays; day++) {
        let dayID = '';
        if (day === todayDate && currentDate.getMonth() === todayMonth && currentDate.getFullYear() === todayYear) {
            dayID = 'today';
        }
        if (day === gapDayRemind.date && currentDate.getMonth() === gapDayRemind.month && currentDate.getFullYear() === gapDayRemind.year) {
            dayID = 'gap-day-remind';
        }
        if (day === nextGapDayReturn.date && currentDate.getMonth() === nextGapDayReturn.month && currentDate.getFullYear() === nextGapDayReturn.year) {
            dayID = 'next-gap-day-return';
        }
        daysHtml += `<div id="${dayID}">${day}</div>`
    }

    calendarBody.innerHTML = daysHtml;
    monthYear.textContent = currentDate.toLocaleDateString('default', { month: 'long', year: 'numeric' });
}

prevMonthButton.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    fetchDate()
});

nextMonthButton.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    fetchDate()
});


function fetchDate() {
    fetch('/calendar_time')
        .then(response => response.json())
        .then(data => {
            const gapDayRemindDate = new Date(data.gap_day_remind);
            const nextGapDayReturnDate = new Date(data.next_gap_day_return);


            console.log(gapDayRemindDate, nextGapDayReturnDate)
            // 呼叫 renderCalendar，並傳入特殊日期
            renderCalendar(gapDayRemindDate, nextGapDayReturnDate);
        })
        .catch(error => console.error('Error fetching data:', error));
}