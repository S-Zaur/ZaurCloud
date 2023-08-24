import {toast} from "../toast.js";
import {currentElem} from "../menu.js";
import {STATUS_CODES} from "../consts.js";

export function deleteFromFavSubmitHandler(e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: $("#delete-from-favorite-form").serialize(),
        dataType: "json",
        success: function (data) {
            toast("Удалено");
            currentElem.remove();
        },
        statusCode: STATUS_CODES,
    });
}

