import {toast} from "../toast.js";
import {STATUS_CODES} from "../consts.js";

function addFavoriteSubmitHandler(e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: $("#add-to-favorite-form").serialize(),
        dataType: "json",
        success: function (data) {
            if (data.result === "Already added") {
                toast("Уже в избранном")
            } else {
                toast("Добавлено в избранное");
            }
        },
        statusCode: STATUS_CODES,
    });
}

export function addAddFavoriteEventListeners() {
    document.getElementById("add-to-favorite-form").addEventListener("submit", addFavoriteSubmitHandler);
}
