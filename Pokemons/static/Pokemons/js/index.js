import {addMenu} from "./modules/menu.js";
import {addPropertiesEventListeners} from "./modules/submit_handlers/properties_submit_handler.js"
$(document).ready(function () {
    addMenu();
    addPropertiesEventListeners();
})
