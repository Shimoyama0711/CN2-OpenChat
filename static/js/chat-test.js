$(function() {
    const socket = io();

    function sendMessage() {
        const input = $("#message-input");
        const message = input.val();

        console.log(`SEND: ${message}`);
        socket.emit("send_message", {"message": message});

        input.val(""); // 初期化
    }

    const sendButton = $("#send-button");
    sendButton.on("click", sendMessage);

    socket.on("connect", function() {
        console.log("I'm connected!! :)");

        socket.on("receive_message", function(data) {
            console.log("TRIGGERED!! :)");
            const messageList = $("#message-list");
            messageList.append(`
            <li class="list-group-item">
                ${data.message}
            </li>
        `);
        });
    });
});

function check() {

}