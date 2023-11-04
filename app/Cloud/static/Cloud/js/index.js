import {addMenu} from "./modules/menu.js";
import {addDragAndDrop} from "./modules/dragAndDrop.js";
import {addAddFavoriteEventListeners} from "./modules/submit_handlers/add_favorite_submit_handler.js";
import {addCreateDirectoryEventListeners} from "./modules/submit_handlers/create_directory_submit_handler.js";
import {addDeleteEventListeners} from "./modules/submit_handlers/delete_submit_handler.js";
import {addPropertiesEventListeners} from "./modules/submit_handlers/properties_submit_handler.js";
import {addRenameEventListeners} from "./modules/submit_handlers/rename_submit_handler.js";
import {addShareEventListeners} from "./modules/submit_handlers/share_submit_handler.js";
import {addCopyEventListeners} from "./modules/submit_handlers/copy_submit_handler.js";
import {addCutEventListeners} from "./modules/submit_handlers/cut_submit_handler.js";
import {addPasteEventListeners} from "./modules/submit_handlers/paste_submit_handler.js";

$(document).ready(function () {
    addMenu();
    addDragAndDrop();
    addAddFavoriteEventListeners();
    addCreateDirectoryEventListeners();
    addDeleteEventListeners();
    addPropertiesEventListeners();
    addRenameEventListeners();
    addShareEventListeners();
    addCopyEventListeners();
    addCutEventListeners();
    addPasteEventListeners();
})
