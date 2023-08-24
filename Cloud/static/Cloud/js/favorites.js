import {addMenu} from "./modules/menu.js";
import {addDeleteFavoriteEventListeners} from "./modules/submit_handlers/delete_favorite_submit_handler.js";

$(document).ready(function () {
    addMenu();
    addDeleteFavoriteEventListeners();
})
