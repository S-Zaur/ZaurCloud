import {mainContainer} from "./consts.js";

const menu = document.getElementById("menu");
export let currentElem = null;

export function addMenu() {
    document.addEventListener('contextmenu', function (e) {
        if (e.target.closest("#main-container") != null) return;
        closeMenu();
    }, false);
    document.addEventListener('click', function (e) {
        if (e.target.closest("#main-container") != null) return;
        closeMenu();
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
        openMenu(posX, posY);
    }, false);
    mainContainer.addEventListener('click', function () {
        closeMenu()
    }, false);
}

function openMenu(x, y) {
    if (y + menu.offsetHeight > document.documentElement.clientHeight) y -= menu.offsetHeight;
    if (x + menu.offsetWidth > document.documentElement.clientWidth) x -= menu.offsetWidth;
    menu.style.top = y + "px";
    menu.style.left = x + "px";
    menu.style.display = "block";
}

function closeMenu() {
    menu.style.display = "none";
}
