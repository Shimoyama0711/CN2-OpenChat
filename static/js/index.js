$(function() {
    const roomNumber = $("#room-number");

    roomNumber.on("input", function () {
        joinCheck();
        $("#join-button").attr("href", `/game/${roomNumber.val()}`);
    });
});

function joinCheck() {
    const roomNumber = $("#room-number");
    const joinButton = $("#join-button");

    if (roomNumber.val().length === 4) {
        joinButton.removeClass("disabled");
    } else {
        joinButton.addClass("disabled");
    }
}