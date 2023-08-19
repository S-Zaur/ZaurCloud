let i = document.getElementById("menu");
let currentElem = null;
const STATUS_CODES = {
    403: function (data) {
        const res = JSON.parse(data.responseText)
        if (!"result" in res) {
            toast("Запрещено");
        } else if (res.result === "Downloadable object too large") {
            toast("Скачиваемая папка слишком большая");
        } else if (res.result === "DEBUG") {
            toast("Невозможно в режиме DEBUG");
        } else {
            toast("Запрещено");
        }
    }, 404: function () {
        toast("Не найдено");
    }, 500: function () {
        toast("Ошибка");
    }
}
document.addEventListener('contextmenu', function (e) {
    if (e.target.closest(".container") != null) return;
    close_menu();
}, false);
document.addEventListener('click', function (e) {
    if (e.target.closest(".container") != null) return;
    close_menu();
}, false);
document.getElementById("main_container").addEventListener('contextmenu', function (e) {
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
document.getElementById("main_container").addEventListener('click', function (e) {
    close_menu()
}, false);

document.getElementById("delete_form").addEventListener("submit", deleteSubmitHandler);
document.getElementById("download_form").addEventListener("submit", downloadSubmitHandler);
document.getElementById("rename").addEventListener("submit", function (e) {
    e.preventDefault();
    $("#new_name").val($(currentElem).find(".card-title").text())
    $("#renameModal").modal('show');
});
document.getElementById("rename_form").onkeydown = function (e) {
    if (e.key === "Enter") {
        renameSubmitHandler(e);
    }
};
document.getElementById("rename_form_submit").addEventListener("click", renameSubmitHandler);

function open_menu(x, y) {
    if (y + i.offsetHeight > document.documentElement.clientHeight) y -= i.offsetHeight;
    if (x + i.offsetWidth > document.documentElement.clientWidth) x -= i.offsetWidth;
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
            toast("Удалено");
            currentElem.remove();
        },
        statusCode: STATUS_CODES,
    });
}

function renameSubmitHandler(e) {
    e.preventDefault();
    $("#renameModal").modal('hide');
    const title = $(currentElem).find(".card-title")
    const name = $("#new_name").val()
    if (title.text() === name) return;
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: $("#rename_form").serialize(),
        dataType: "json",
        success: function (data) {
            if (data.result === "ok") {
                title.text(name);
            }
        },
        statusCode: STATUS_CODES,
    });
}

function downloadSubmitHandler(e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: window.location.href,
        data: $("#download_form").serialize(),
        dataType: "json",
        statusCode: STATUS_CODES,
    });
}

function toast(text) {
    $("#message_text").text(text);
    $(".toast").toast('show');
}
