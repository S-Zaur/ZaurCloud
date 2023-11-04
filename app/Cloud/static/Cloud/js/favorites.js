import {addMenu} from "./modules/menu.js";
import {addDeleteFavoriteEventListeners} from "./modules/submit_handlers/delete_favorite_submit_handler.js";
import {addPropertiesEventListeners} from "./modules/submit_handlers/properties_submit_handler.js";

$(document).ready(function () {
    addMenu();
    addDeleteFavoriteEventListeners();
    addPropertiesEventListeners();
})
