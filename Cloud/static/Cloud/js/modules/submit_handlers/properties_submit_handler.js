import {STATUS_CODES} from "../consts.js";

export function propertiesSubmitHandler(e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: window.location.href,
        data: $("#properties-form").serialize(),
        dataType: "json",
        success: function (data) {
            const table = $('#propertiesTable')
            table.find('tbody').empty();
            for (const [key, value] of Object.entries(data)) {
                table.find('tbody')
                    .append($('<tr>')
                        .append($('<td>')
                            .text(key)).append($('<td>')
                            .text(value)));
            }
            $("#propertiesModal").modal('show');
        },
        statusCode: STATUS_CODES,
    });
}

export function addPropertiesEventListeners() {
    document.getElementById("properties-form").addEventListener("submit", propertiesSubmitHandler);
}
