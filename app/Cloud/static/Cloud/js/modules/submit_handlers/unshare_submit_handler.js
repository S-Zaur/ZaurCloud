import {toast} from "../toast.js";
import {currentElem} from "../menu.js";
import {STATUS_CODES} from "../consts.js";

function unshareSubmitHandler(e) {
    e.preventDefault();
    const form = $("#unshare-form")
    $.ajax({
        type: "POST",
        url: form.attr('action'),
        data: form.serialize(),
        dataType: "json",
        success: function (data) {
            toast("Ссылка удалена");
            currentElem.remove();
        },
        statusCode: STATUS_CODES,
    });
}

export function addUnshareEventListeners() {
    document.getElementById("unshare-form").addEventListener("submit", unshareSubmitHandler);
}
