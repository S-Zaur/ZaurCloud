import {STATUS_CODES} from "../consts.js";

export function hitSubmitHandler(e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: window.location.href,
        data: $("#hit-form").serialize(),
        dataType: "json",
        success: function (data) {
            let battle_log = $("#battle-log");
            battle_log.append($("<div>").append(document.createTextNode(data.description + "\n")));
            if ("player_pokemon" in data) {
                $("#player_hp").attr("value", data.player_pokemon.hp);
                $("#player_pokemon").val(JSON.stringify(data.player_pokemon))
                if (data.player_pokemon.hp === 0) {
                    save("LOSS");
                    battle_log.append($("<div>").append($("<b>").append(document.createTextNode("Вы проиграли"))));
                    $("#battle-img").css("transform", "rotate(180deg)")
                    $("#hit-submit").attr("disabled", "disabled");
                    $("#battle-form").css("display", "block");
                    $("#revenge-form").css("display", "block");
                }
            }
            if ("opponent_pokemon" in data) {
                $("#opponent_hp").attr("value", data.opponent_pokemon.hp);
                $("#opponent_pokemon").val(JSON.stringify(data.opponent_pokemon))
                if (data.opponent_pokemon.hp === 0) {
                    save("WIN");
                    battle_log.append($("<div>").append($("<b>").append(document.createTextNode("Вы выиграли"))));
                    $("#hit-submit").attr("disabled", "disabled");
                    $("#battle-form").css("display", "block");
                }
            }
        },
        statusCode: STATUS_CODES,
    });
}

export function addHitEventListeners() {
    document.getElementById("hit-form").addEventListener("submit", hitSubmitHandler);
}

function save(result) {
    $("#battle_result").val(result);
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: $("#result-form").serialize(),
        dataType: "json",
        statusCode: STATUS_CODES,
    });
}