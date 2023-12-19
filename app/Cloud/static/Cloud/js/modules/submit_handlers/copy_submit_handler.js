import {STATUS_CODES} from "../consts.js";

function copySubmitHandler(e) {
    e.preventDefault();
    const form = $("#copy-form")
    $.ajax({
        type: "POST",
        url: form.attr("action"),
        data: form.serialize(),
        dataType: "json",
        statusCode: STATUS_CODES,
    });
}

export function addCopyEventListeners() {
    document.getElementById("copy-form").addEventListener("submit", copySubmitHandler);
}
