import {currentElem} from "../menu.js";
import {STATUS_CODES} from "../consts.js";

function deleteSubmitHandler(e) {
    e.preventDefault();
    const form = $("#delete-form")
    $.ajax({
        type: "POST",
        url: form.attr("action"),
        data: form.serialize(),
        dataType: "json",
        success: function (data) {
            currentElem.remove();
        },
        statusCode: STATUS_CODES,
    });
}

export function addDeleteEventListeners() {
    document.getElementById("delete-form").addEventListener("submit", deleteSubmitHandler);
}
