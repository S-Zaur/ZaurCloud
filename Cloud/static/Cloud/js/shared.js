import {addMenu, addSharedMenu} from "./modules/menu.js";
import {addPropertiesEventListeners} from "./modules/submit_handlers/properties_submit_handler.js";
import {addUnshareEventListeners} from "./modules/submit_handlers/unshare_submit_handler.js";

$(document).ready(function () {
    addMenu();
    addSharedMenu();
    addPropertiesEventListeners();
    addUnshareEventListeners();
})
