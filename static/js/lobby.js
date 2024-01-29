$(function() {
    const socket = io();
    const roomNumber = location.pathname.split("/").pop();

    const messageInput = $("#message-input");
    const sendMessageButton = $("#send-message-button");

    messageInput.on("input", checkSendButton);

    sendMessageButton.on("click", function () {
        const message = messageInput.val();
        const yourName = $("#your-name").text();

        socket.emit("send_message", {
            "room_number": roomNumber,
            "message": message,
            "name": yourName
        });

        messageInput.val("");
    });

    // Socket IO //

    socket.on("connect", function() {
        socket.emit("join", {
            "room_number": roomNumber
        });
    });

    socket.on("update_room", function(data) {
        if (data["room_number"] === roomNumber) {
            updatePlayerList(data["players"]);
        }
    });

    socket.on("receive_message", function(data) {
        if (data["room_number"] === roomNumber) {
            updateMessageList(data["messages"]);
        }
    });

    function updatePlayerList(players) {
        const playerList = $("#player-list");
        playerList.empty(); // 初期化

        players.forEach(function(player) {
            const item = $("<li></li>");
            item.addClass("list-group-item");

            item.html(`
                <img class="avatar" src="${player["avatar"]}" alt="${player["name"]}'s Avatar">
                ${player["name"]}
                ${player["is_owner"] ? '<i class="bi-star-fill" style="color: #db9925"></i>' : ""}
            `);

            // console.log(player);

            playerList.append(item);
        });
    }

    function updateMessageList(messages) {
        const messageList = $("#message-list");
        messageList.empty(); // 初期化

        messages.forEach(function(message) {
            const item = $("<li></li>");
            item.addClass("list-group-item");

            item.html(`
                <img class="avatar" src="${message["avatar"]}" alt="${message["name"]}'s Avatar">
                ${message["name"]} <span style="color: #b1b1b1; font-style: italic">${message["date"]}</span> <br>
                ${message["msg"]}
            `);

            // console.log(player);

            messageList.append(item);
        });
    }
});

function checkSendButton() {
    const messageInput = $("#message-input");
    const sendMessageButton = $("#send-message-button");

    if (messageInput.val().length > 0) {
        sendMessageButton.removeClass("disabled");
    } else {
        sendMessageButton.addClass("disabled");
    }
}