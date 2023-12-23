import {toast} from "./toast.js";

export const mainContainer = document.getElementById("main-container");
export const STATUS_CODES = {
    400: function (data) {
        const res = JSON.parse(data.responseText);
        if (!"result" in res) {
            toast("Ошибка")
        } else {
            toast(res.error)
        }
    }, 403: function (data) {
        const res = JSON.parse(data.responseText)
        if (!"result" in res) {
            toast("Запрещено");
        } else {
            toast(res.error);
        }
    }, 404: function () {
        toast("Не найдено");
    }, 500: function () {
        toast("Ошибка сервера");
    }
}
