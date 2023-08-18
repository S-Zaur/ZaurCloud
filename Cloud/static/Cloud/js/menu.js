let i = document.getElementById("menu");
let containers = document.getElementsByClassName("container")
let currentElem = null;

document.addEventListener('contextmenu', function (e) {
    if (e.target.closest(".container") != null) return;
    close_menu();
}, false);
document.addEventListener('click', function (e) {
    if (e.target.closest(".container") != null) return;
    close_menu();
}, false);
Array.prototype.forEach.call(containers, function (container) {
    container.addEventListener('contextmenu', function (e) {
        if (e.target.closest(".container") == null) return;
        const posX = e.clientX;
        const posY = e.clientY;
        open_menu(posX, posY);

        let target = e.target.closest('.col');
        if (!target) return;
        currentElem = target;

        let link = currentElem.firstElementChild.attributes.onclick.value;
        if (link == null) {
            alert("Error");
        }

        let urls = document.getElementsByClassName("form_url")
        Array.prototype.forEach.call(urls, function (url_input) {
            url_input.value = link.substring(24, link.length - 2);
        });
        e.preventDefault();
    }, false);
    container.addEventListener('click', function (e) {
        close_menu()
    }, false);
})

function open_menu(x, y) {
    if (y + i.offsetHeight > document.documentElement.clientHeight)
        y -= i.offsetHeight;
    if (x + i.offsetWidth > document.documentElement.clientWidth)
        x -= i.offsetWidth;
    i.style.top = y + "px";
    i.style.left = x + "px";
    i.style.visibility = "visible";
    i.style.opacity = "1";
}

function close_menu() {
    i.style.opacity = "0";
    setTimeout(function () {
        i.style.visibility = "hidden";
    }, 501);
}

function deleteSubmitHandler(e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: $("#delete_form").serialize(),
        dataType: "json",
        success: function (data) {
            if (data.result === "deleted") {
                toast("Удалено");
                currentElem.remove();
            }
        },
        statusCode: {
            403: function () {
                toast("Запрещено");
            },
            404: function () {
                toast("Не найдено");
            },
            500: function () {
                toast("Ошибка");
            }
        },
    });
}
