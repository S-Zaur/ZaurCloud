import {addMenu} from "./modules/menu.js";
import {addMenuFormsEventListeners} from "./modules/favorites/menuForms.js";

$(document).ready(function () {
    addMenu();
    addMenuFormsEventListeners();
})
