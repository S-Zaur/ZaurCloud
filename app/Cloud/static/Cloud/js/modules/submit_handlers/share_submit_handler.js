import {toast} from "../toast.js";
import {STATUS_CODES} from "../consts.js";

function shareSubmitHandler(e) {
    e.preventDefault();
    const form = $("#share-form")
    $.ajax({
        type: "POST",
        url: form.attr("action"),
        data: form.serialize(),
        dataType: "json",
        success: function (data) {
            if (navigator.clipboard) {
                navigator.clipboard.writeText(data.url)
                    .then(() => {
                        toast("Ссылка скопирована в буфер обмена. " + data.url);
                    })
                    .catch(err => {
                        toast('Что-то пошло не так. Вот ваша ссылка:' + data.url);
                    });
            } else {
                toast("Ссылка: " + data.url);
            }
        },
        statusCode: STATUS_CODES,
    });
}

export function addShareEventListeners() {
    document.getElementById("share-form").addEventListener("submit", shareSubmitHandler);
}
