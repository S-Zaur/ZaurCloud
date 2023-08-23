import {addMenu} from "./modules/menu.js";
import {addMenuFormsEventListeners} from "./modules/menuForms.js";
import {dragAndDrop} from "./modules/dragAndDrop.js";

$(document).ready(function () {
    addMenu();
    addMenuFormsEventListeners();
    dragAndDrop();
})
