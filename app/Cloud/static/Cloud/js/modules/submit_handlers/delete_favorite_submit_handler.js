import {toast} from "../toast.js";
import {currentElem} from "../menu.js";
import {STATUS_CODES} from "../consts.js";

function deleteFavoriteSubmitHandler(e) {
    e.preventDefault();
    const form = $("#delete-favorite-form")
    $.ajax({
        type: "POST",
        url: form.attr("action"),
        data: form.serialize(),
        dataType: "json",
        success: function (data) {
            toast("Удалено");
            currentElem.remove();
        },
        statusCode: STATUS_CODES,
    });
}

export function addDeleteFavoriteEventListeners() {
    document.getElementById("delete-favorite-form").addEventListener("submit", deleteFavoriteSubmitHandler);
}
