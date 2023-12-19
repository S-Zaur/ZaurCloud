import {STATUS_CODES} from "../consts.js";

export function propertiesSubmitHandler(e) {
    e.preventDefault();
    const form = $("#properties-form")
    $.ajax({
        type: "GET",
        url: form.attr('action'),
        data: form.serialize(),
        dataType: "json",
        success: function (data) {
            const tbody = $("<tbody>")
            for (const [key, value] of Object.entries(data)) {
                tbody
                    .append($('<tr>')
                        .append($('<td>')
                            .text(key)).append($('<td>')
                            .text(value)));
            }
            const table = $("<table>")
                .addClass("table")
                .append(tbody)
            const body = $("#modal-body")
            body.empty()
            body.append(table)
            $("#modal").modal('show');
        },
        statusCode: STATUS_CODES,
    });
}

export function addPropertiesEventListeners() {
    document.getElementById("properties-form").addEventListener("submit", propertiesSubmitHandler);
}
