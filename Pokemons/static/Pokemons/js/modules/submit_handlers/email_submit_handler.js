import {STATUS_CODES} from "../consts.js";

export function emailSubmitHandler(e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: $("#email-form").serialize(),
        dataType: "json",
        statusCode: STATUS_CODES,
    });
}

export function addEmailEventListeners() {
    document.getElementById("email-form").addEventListener("submit", emailSubmitHandler);
}

