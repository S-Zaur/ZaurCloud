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

    currentElem = e.target.closest(".col")
    let link = $("#grid").attr("data-url")
    if (currentElem != null) {
        link = currentElem.firstElementChild.dataset.url;
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
document.getElementById("properties_form").addEventListener("submit", propertiesSubmitHandler);
document.getElementById("create_directory_form").addEventListener("submit", createDirectorySubmitHandler);
document.getElementById("rename").addEventListener("submit", function (e) {
    e.preventDefault();
    if (currentElem != null) {
        $("#new_name").val($(currentElem).find(".card-title").text())
    } else {
        $("#new_name").val($("#grid").data("name"))
    }
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
    const current = $(currentElem)
    const title = current.find(".card-title")
    const name = $("#new_name").val()
    if (title.text() === name) return;
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: $("#rename_form").serialize(),
        dataType: "json",
        success: function (data) {
            if (currentElem == null) {
                window.location.assign(data.abs_url);
            } else {
                title.text(name);
                current.removeAttr("onclick")
                current.removeAttr("data-url")
                current.find(".card").attr("onclick", "window.location='" + data.abs_url + "'")
                current.find(".card").attr("data-url", data.rel_url)
            }
        },
        statusCode: STATUS_CODES,
    });
}

function propertiesSubmitHandler(e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: window.location.href,
        data: $("#properties_form").serialize(),
        dataType: "json",
        success: function (data) {
            const table = $('#propertiesTable')
            table.find('tbody').empty();
            for (const [key, value] of Object.entries(data)) {
                table.find('tbody')
                    .append($('<tr>')
                        .append($('<td>')
                            .text(key)).append($('<td>')
                            .text(value)));
            }
            $("#propertiesModal").modal('show');
        },
        statusCode: STATUS_CODES,
    });
}

function createDirectorySubmitHandler(e) {
    e.preventDefault();
    const cb = $("#in_place_cb")
    if (currentElem == null) {
        cb.prop("checked", true);
    } else {
        cb.prop("checked", false);
    }
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: $("#create_directory_form").serialize(),
        dataType: "json",
        success: function (data) {
            $('#grid').append($('<div>')
                .addClass("col d-flex align-items-stretch mb-3")
                .append($('<div>')
                    .addClass("card")
                    .attr("data-url", data.rel_url)
                    .attr("onclick", "window.location='" + data.abs_url + "'")
                    .append($("<img>")
                        .addClass("card-img-top img-fluid img-thumbnail")
                        .attr("src", data.img)
                        .attr("alt", "object"))
                    .append($("<div>")
                        .addClass("card-body")
                        .append($("<h5>")
                            .addClass("card-title")
                            .text(data.name)))));
        },
        statusCode: STATUS_CODES,
    });
}

function toast(text) {
    $("#message_text").text(text);
    $(".toast").toast('show');
}
