import {mainContainer} from "./consts.js";

const menu = document.getElementById("menu");
export let currentElem = null;

export function addMenu() {
    document.addEventListener('contextmenu', function (e) {
        if (e.target.closest("#main-container") != null) return;
        close_menu();
    }, false);
    document.addEventListener('click', function (e) {
        if (e.target.closest("#main-container") != null) return;
        close_menu();
    }, false);
    mainContainer.addEventListener('contextmenu', function (e) {
        e.preventDefault();

        currentElem = e.target.closest(".col")
        let link = $("#grid").attr("data-url")
        if (currentElem != null) {
            link = currentElem.firstElementChild.dataset.url;
        }
        let urls = document.getElementsByClassName("form-url")
        Array.prototype.forEach.call(urls, function (url_input) {
            url_input.value = link;
        });

        const posX = e.clientX;
        const posY = e.clientY;
        open_menu(posX, posY);
    }, false);
    mainContainer.addEventListener('click', function () {
        close_menu()
    }, false);
}

function open_menu(x, y) {
    if (y + menu.offsetHeight > document.documentElement.clientHeight) y -= menu.offsetHeight;
    if (x + menu.offsetWidth > document.documentElement.clientWidth) x -= menu.offsetWidth;
    menu.style.top = y + "px";
    menu.style.left = x + "px";
    menu.style.display = "block";
}

function close_menu() {
    menu.style.display = "none";
}
