import {
    addFavoriteSubmitHandler,
    createDirectorySubmitHandler,
    deleteSubmitHandler,
    propertiesSubmitHandler,
    renameSubmitHandler
} from "./submitHandlers.js";
import {currentElem} from "./menu.js";

export function addMenuFormsEventListeners() {
    document.getElementById("delete-form").addEventListener("submit", deleteSubmitHandler);
    document.getElementById("properties-form").addEventListener("submit", propertiesSubmitHandler);
    document.getElementById("add-to-favorite-form").addEventListener("submit", addFavoriteSubmitHandler);
    document.getElementById("create-directory-form").addEventListener("submit", createDirectorySubmitHandler);
    document.getElementById("rename-form-submit").addEventListener("click", renameSubmitHandler);
    document.getElementById("rename").addEventListener("submit", function (e) {
        e.preventDefault();
        if (currentElem != null) {
            $("#new-name").val($(currentElem).find(".card-title").text())
        } else {
            $("#new-name").val($("#grid").data("name"))
        }
        $("#renameModal").modal('show');
    });
    document.getElementById("rename-form").onkeydown = function (e) {
        if (e.key === "Enter") {
            renameSubmitHandler(e);
        }
    };
}
