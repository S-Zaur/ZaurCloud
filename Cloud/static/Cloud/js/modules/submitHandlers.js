import {currentElem} from "./menu.js";
import {STATUS_CODES} from "./consts.js";
import {toast} from "./toast.js";

export function deleteSubmitHandler(e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: $("#delete-form").serialize(),
        dataType: "json",
        success: function (data) {
            toast("Удалено");
            currentElem.remove();
        },
        statusCode: STATUS_CODES,
    });
}

export function renameSubmitHandler(e) {
    e.preventDefault();
    $("#renameModal").modal('hide');
    const current = $(currentElem)
    const title = current.find(".card-title")
    const name = $("#new-name").val()
    if (title.text() === name) return;
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: $("#rename-form").serialize(),
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

export function propertiesSubmitHandler(e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: window.location.href,
        data: $("#properties-form").serialize(),
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

export function createDirectorySubmitHandler(e) {
    e.preventDefault();
    const cb = $("#in-place-cb")
    if (currentElem == null) {
        cb.prop("checked", true);
    } else {
        cb.prop("checked", false);
    }
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: $("#create-directory-form").serialize(),
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
