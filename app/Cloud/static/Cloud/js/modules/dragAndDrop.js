import {mainContainer, STATUS_CODES} from "./consts.js";
import {toast} from "./toast.js";

const dropArea = document.getElementById("drop-area")

export function addDragAndDrop() {
    ;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        mainContainer.addEventListener(eventName, preventDefaults, false);
        dropArea.addEventListener(eventName, preventDefaults, false);
    });
    ['dragenter', 'dragover'].forEach(eventName => {
        mainContainer.addEventListener(eventName, highlight, false)
    });
    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unHighlight, false)
    })
    dropArea.addEventListener('drop', handleDrop, false);
    $('#file-input').on('change', function () {
        uploadFiles(document.getElementById('file-input').files);
    })
    $("#upload-file-button").on('click', function () {
        document.getElementById('file-input').click();
    })
}

function preventDefaults(e) {
    e.preventDefault()
    e.stopPropagation()
}

function highlight(e) {
    dropArea.style.display = "block"
}

function unHighlight(e) {
    dropArea.style.display = "none";
}

function handleDrop(e) {
    let dt = e.dataTransfer
    let files = dt.files
    uploadFiles(files)
}

function uploadFiles(files) {
    let formData = new FormData()
    const form = $("#upload-form")
    const csrf = form.serialize().split("=")
    formData.append(csrf[0], csrf[1]);
    ([...files]).forEach((file) => {
        formData.append(file.name, file);
    })
    formData.append("url", $("#grid").attr("data-url"))
    $.ajax({
        type: "POST", url: form.attr("action"), data: formData, success: function (data) {
            let exists = [];
            data.files.forEach((file) => {
                if ("exists" in file) {
                    exists.push(file.name);
                } else {
                    $('#grid').append($('<div>')
                        .addClass("col d-flex align-items-stretch mb-3")
                        .append($('<div>')
                            .addClass("card")
                            .attr("data-url", file.rel_url)
                            .append($("<img>")
                                .addClass("card-img-top img-fluid img-thumbnail")
                                .attr("src", file.img)
                                .attr("alt", "object"))
                            .append($("<div>")
                                .addClass("card-body")
                                .append($("<h5>")
                                    .addClass("card-title")
                                    .text(file.name)))));
                }
            });
            if (exists.length > 0) {
                toast("Файлы: " + exists.join(", ") + " уже существуют, для замены удалите их")
            } else {
                toast("OK")
            }
        }, processData: false, contentType: false, statusCode: STATUS_CODES,
    });
}
