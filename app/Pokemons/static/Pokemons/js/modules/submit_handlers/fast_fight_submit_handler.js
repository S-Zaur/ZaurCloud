import {STATUS_CODES} from "../consts.js";

export function fastFightSubmitHandler(e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: window.location.href,
        data: $("#fast-fight-form").serialize(),
        dataType: "json",
        success: function (data) {
            let battle_log = $("#battle-log");
            $("#opponent_hp").attr("value", data.opponent_pokemon.hp);
            $("#player_hp").attr("value", data.player_pokemon.hp);
            data.description_list.forEach((element) =>
                battle_log.append($("<div>").append(document.createTextNode(element.description + "\n")))
            )
            $("#fast-fight-submit").attr("disabled", "disabled");
            $("#hit-submit").attr("disabled", "disabled");
            $("#battle-form").css("display", "block");
            $("#email-form").css("display", "block");
        },
        statusCode: STATUS_CODES,
    });
}

export function addFastFightEventListeners() {
    document.getElementById("fast-fight-form").addEventListener("submit", fastFightSubmitHandler);
}
