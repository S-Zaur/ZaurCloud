import {addHitEventListeners} from "./modules/submit_handlers/hit_submit_handler.js"
import {addEmailEventListeners} from "./modules/submit_handlers/email_submit_handler.js";

$(document).ready(function () {
    addHitEventListeners();
    addEmailEventListeners();
})