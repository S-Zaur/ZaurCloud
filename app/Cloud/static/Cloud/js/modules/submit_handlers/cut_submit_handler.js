import {STATUS_CODES} from "../consts.js";

function cutSubmitHandler(e) {
    e.preventDefault();
    const form = $("#cut-form")
    $.ajax({
        type: "POST",
        url: form.attr("action"),
        data: form.serialize(),
        dataType: "json",
        statusCode: STATUS_CODES,
    });
}

export function addCutEventListeners() {
    document.getElementById("cut-form").addEventListener("submit", cutSubmitHandler);
}
