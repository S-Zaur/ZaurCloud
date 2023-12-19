import {currentElem} from "../menu.js";
import {STATUS_CODES} from "../consts.js";

function createDirectorySubmitHandler(e) {
    e.preventDefault();
    const cb = $("#in-place-cb")
    if (currentElem == null) {
        cb.prop("checked", true);
    } else {
        cb.prop("checked", false);
    }
    const form = $("#create-directory-form")
    $.ajax({
        type: "POST",
        url: form.attr("action"),
        data: form.serialize(),
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

export function addCreateDirectoryEventListeners() {
    document.getElementById("create-directory-form").addEventListener("submit", createDirectorySubmitHandler);
}
