import {
    createDirectorySubmitHandler,
    deleteSubmitHandler,
    propertiesSubmitHandler,
    renameSubmitHandler
} from "./submitHandlers.js";
import {currentElem} from "./menu.js";

export function addMenuFormsEventListeners() {
    document.getElementById("delete_form").addEventListener("submit", deleteSubmitHandler);
    document.getElementById("properties_form").addEventListener("submit", propertiesSubmitHandler);
    document.getElementById("create_directory_form").addEventListener("submit", createDirectorySubmitHandler);
    document.getElementById("rename_form_submit").addEventListener("click", renameSubmitHandler);
    document.getElementById("rename").addEventListener("submit", function (e) {
        e.preventDefault();
        if (currentElem != null) {
            $("#new_name").val($(currentElem).find(".card-title").text())
        } else {
            $("#new_name").val($("#grid").data("name"))
        }
        $("#renameModal").modal('show');
    });
    document.getElementById("rename_form").onkeydown = function (e) {
        if (e.key === "Enter") {
            renameSubmitHandler(e);
        }
    };
}
