export function toast(text) {
    $("#message_text").text(text);
    $(".toast").toast('show');
}
