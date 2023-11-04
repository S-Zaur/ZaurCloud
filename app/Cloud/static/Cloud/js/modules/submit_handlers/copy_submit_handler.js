import {STATUS_CODES} from "../consts.js";

function copySubmitHandler(e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: $("#copy-form").serialize(),
        dataType: "json",
        statusCode: STATUS_CODES,
    });
}

export function addCopyEventListeners() {
    document.getElementById("copy-form").addEventListener("submit", copySubmitHandler);
}
