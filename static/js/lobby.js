$(function() {
    const socket = io();
    const roomNumber = location.pathname.split("/").pop();

    socket.on("connect", function() {
        socket.emit("join", {"room_number": roomNumber});
    });

    socket.on("update_room", function(data) {
        // const json = JSON.parse(JSON.stringify(data));

        if (data["room_number"] === roomNumber) {
            updatePlayerList(data["players"]);
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

            console.log(player);

            playerList.append(item);
        });
    }
});