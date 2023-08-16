let i = document.getElementById("menu");
let containers = document.getElementsByClassName("container")

document.addEventListener('contextmenu', function (e) {
    if (e.target.closest(".container") != null) return;
    close_menu();
}, false);
document.addEventListener('click', function (e) {
    if (e.target.closest(".container") != null) return;
    close_menu();
}, false);
Array.prototype.forEach.call(containers, function (container) {
    container.addEventListener('contextmenu', function (e) {
        if (e.target.closest(".container") == null) return;
        const posX = e.clientX;
        const posY = e.clientY;
        open_menu(posX, posY);
        e.preventDefault();
    }, false);
    container.addEventListener('click', function (e) {
        close_menu()
    }, false);
})

function open_menu(x, y) {
    if (y + i.offsetHeight > document.documentElement.clientHeight)
        y -= i.offsetHeight;
    if (x + i.offsetWidth > document.documentElement.clientWidth)
        x -= i.offsetWidth;
    i.style.top = y + "px";
    i.style.left = x + "px";
    i.style.visibility = "visible";
    i.style.opacity = "1";
}

function close_menu() {
    i.style.opacity = "0";
    setTimeout(function () {
        i.style.visibility = "hidden";
    }, 501);
}
