import {currentElem} from "../menu.js";
import {STATUS_CODES} from "../consts.js";

function renameSubmitHandler(e) {
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

export function addRenameEventListeners() {
    document.getElementById("rename-form-submit").addEventListener("click", renameSubmitHandler);
    document.getElementById("rename").addEventListener("submit", function (e) {
        e.preventDefault();
        if (currentElem != null) {
            $("#new-name").val($(currentElem).find(".card-title").text())
        } else {
            $("#new-name").val($("#grid").data("name"))
        }
        $("#renameModal").modal('show');
    });
    document.getElementById("rename-form").onkeydown = function (e) {
        if (e.key === "Enter") {
            renameSubmitHandler(e);
        }
    };
}
