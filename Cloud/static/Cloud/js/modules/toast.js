export function toast(text) {
    $("#message-text").text(text);
    $(".toast").toast('show');
}
