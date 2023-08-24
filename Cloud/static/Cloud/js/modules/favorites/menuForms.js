import {deleteFromFavSubmitHandler} from "./submitHandlers.js";

export function addMenuFormsEventListeners() {
    document.getElementById("delete-from-favorite-form").addEventListener("submit", deleteFromFavSubmitHandler);
}
