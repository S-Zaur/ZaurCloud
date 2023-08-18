let i = document.getElementById("menu");
let container = document.getElementById("main_container")
let currentElem = null;

document.addEventListener('contextmenu', function (e) {
    if (e.target.closest(".container") != null) return;
    close_menu();
}, false);
document.addEventListener('click', function (e) {
    if (e.target.closest(".container") != null) return;
    close_menu();
}, false);
container.addEventListener('contextmenu', function (e) {
    if (e.target.closest(".container") == null) return;
    e.preventDefault();

    let target = e.target.closest('.col');
    if (target == null) {
        toast("Error")
        return;
    }
    currentElem = target;

    let link = currentElem.firstElementChild.dataset.url;
    if (link == null) {
        toast("Error")
        return;
    }
    let urls = document.getElementsByClassName("form_url")
    Array.prototype.forEach.call(urls, function (url_input) {
        url_input.value = link;
    });

    const posX = e.clientX;
    const posY = e.clientY;
    open_menu(posX, posY);
}, false);
container.addEventListener('click', function (e) {
    close_menu()
}, false);

document.getElementById("delete_form").addEventListener("submit", deleteSubmitHandler);

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

function toast(text) {
    $("#message_text").text(text);
    $(".toast").toast('show');
}
