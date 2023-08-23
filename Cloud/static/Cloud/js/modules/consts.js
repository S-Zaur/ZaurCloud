import {toast} from "./toast.js";

export const mainContainer = document.getElementById("main_container");
export const STATUS_CODES = {
    403: function (data) {
        const res = JSON.parse(data.responseText)
        if (!"result" in res) {
            toast("Запрещено");
        } else if (res.result === "Downloadable object too large") {
            toast("Скачиваемая папка слишком большая");
        } else if (res.result === "DEBUG") {
            toast("Невозможно в режиме DEBUG");
        } else {
            toast("Запрещено");
        }
    }, 404: function () {
        toast("Не найдено");
    }, 500: function () {
        toast("Ошибка");
    }
}
