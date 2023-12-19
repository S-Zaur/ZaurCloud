import {toast} from "../toast.js";
import {STATUS_CODES} from "../consts.js";

function addFavoriteSubmitHandler(e) {
    e.preventDefault();
    const form = $("#add-to-favorite-form")
    $.ajax({
        type: "POST",
        url: form.attr("action"),
        data: form.serialize(),
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
