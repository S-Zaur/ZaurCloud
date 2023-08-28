import {STATUS_CODES} from "../consts.js";
import {toast} from "../toast.js";

function pasteSubmitHandler(e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: $("#paste-form").serialize(),
        dataType: "json",
        success: function (data) {
            let exists = [];
            data.files.forEach((file) => {
                if ("exists" in file) {
                    exists.push(file.name);
                } else {
                    const div = $('<div>')
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
                                .text(file.name)))
                    if (!file.is_file) {
                        div.attr("onclick", "window.location='" + file.abs_url + "'")
                    }
                    $('#grid').append($('<div>')
                        .addClass("col d-flex align-items-stretch mb-3")
                        .append(div));
                }
            })
            if (exists.length > 0) {
                toast("Файлы: " + exists.join(", ") + " уже существуют, для замены удалите их")
            }
        },
        statusCode: STATUS_CODES,
    });
}

export function addPasteEventListeners() {
    document.getElementById("paste-form").addEventListener("submit", pasteSubmitHandler);
}
