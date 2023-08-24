import {toast} from "../toast.js";
import {currentElem} from "../menu.js";
import {STATUS_CODES} from "../consts.js";

function deleteFavoriteSubmitHandler(e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: $("#delete-favorite-form").serialize(),
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
