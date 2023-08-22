let menu = document.getElementById("menu");
let currentElem = null;
let mainContainer = document.getElementById("main_container");
let dropArea = document.getElementById("drop-area")
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
    if (e.target.closest("#main_container") != null) return;
    close_menu();
}, false);
document.addEventListener('click', function (e) {
    if (e.target.closest("#main_container") != null) return;
    close_menu();
}, false);
mainContainer.addEventListener('contextmenu', function (e) {
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
mainContainer.addEventListener('click', function (e) {
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

;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    mainContainer.addEventListener(eventName, preventDefaults, false);
    dropArea.addEventListener(eventName, preventDefaults, false);
});
['dragenter', 'dragover'].forEach(eventName => {
    mainContainer.addEventListener(eventName, highlight, false)
});
['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unHighlight, false)
})
dropArea.addEventListener('drop', handleDrop, false)

function open_menu(x, y) {
    if (y + menu.offsetHeight > document.documentElement.clientHeight) y -= menu.offsetHeight;
    if (x + menu.offsetWidth > document.documentElement.clientWidth) x -= menu.offsetWidth;
    menu.style.top = y + "px";
    menu.style.left = x + "px";
    menu.style.display = "block";
}

function close_menu() {
    menu.style.display = "none";
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

function preventDefaults(e) {
    e.preventDefault()
    e.stopPropagation()
}

function highlight(e) {
    dropArea.style.display = "block"
}

function unHighlight(e) {
    dropArea.style.display = "none";
}

function handleDrop(e) {
    let dt = e.dataTransfer
    let files = dt.files
    uploadFiles(files)
}

function uploadFiles(files) {
    let formData = new FormData()
    const csrf = $("#upload_form").serialize().split("=")
    formData.append(csrf[0], csrf[1])
    formData.append("action", "Upload");
    ([...files]).forEach((file) => {
        formData.append(file.name, file);
    })
    formData.append("url", $("#grid").attr("data-url"))
    $.ajax({
        type: "POST", url: window.location.href, data: formData, success: function (data) {
            let exists = [];
            data.files.forEach((file) => {
                if ("exists" in file) {
                    exists.push(file.name);
                } else {
                    $('#grid').append($('<div>')
                        .addClass("col d-flex align-items-stretch mb-3")
                        .append($('<div>')
                            .addClass("card")
                            .attr("data-url", file.rel_url)
                            .append($("<img>")
                                .addClass("card-img-top img-fluid img-thumbnail")
                                .attr("src", file.img)
                                .attr("alt", "object"))
                            .append($("<div>")
                                .addClass("card-body")
                                .append($("<h5>")
                                    .addClass("card-title")
                                    .text(file.name)))));
                }
            });
            if (exists.length > 0) {
                toast("Файлы: " + exists.join(", ") + " уже существуют, для замены удалите их")
            } else {
                toast("OK")
            }
        }, processData: false, contentType: false, statusCode: STATUS_CODES,
    });
}
