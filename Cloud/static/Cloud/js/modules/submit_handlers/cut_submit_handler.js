import {STATUS_CODES} from "../consts.js";

function cutSubmitHandler(e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: $("#cut-form").serialize(),
        dataType: "json",
        statusCode: STATUS_CODES,
    });
}

export function addCutEventListeners() {
    document.getElementById("cut-form").addEventListener("submit", cutSubmitHandler);
}
