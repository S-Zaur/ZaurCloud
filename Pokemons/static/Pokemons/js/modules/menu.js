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

        currentElem = e.target.closest(".col");
        let name = "";
        console.log(currentElem);
        if (currentElem != null) {
            name = currentElem.firstElementChild.dataset.name;
        }
        console.log(name);
        let names = document.getElementsByClassName("form-name")
        Array.prototype.forEach.call(names, function (name_input) {
            name_input.value = name;
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
