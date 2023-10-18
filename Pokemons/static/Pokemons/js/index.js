import {addMenu} from "./modules/menu.js";
import {addPropertiesEventListeners} from "./modules/submit_handlers/properties_submit_handler.js"
import {addFtpSaveEventListeners} from "./modules/submit_handlers/ftp_save_submit_handler.js";
$(document).ready(function () {
    addMenu();
    addPropertiesEventListeners();
    addFtpSaveEventListeners();
})
