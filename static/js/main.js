$(document).ready(function () {
    function getCsrfToken() {
        return $("input[name='csrfmiddlewaretoken']").val() || $("meta[name='csrf-token']").attr("content");
    }

    function getIndianTime() {
        let options = { timeZone: "Asia/Kolkata", hour12: true, hour: "2-digit", minute: "2-digit" };
        return new Date().toLocaleString("en-US", options);
    }

    function appendMessage(message) {
        $(".thetextdisplayer").append(`
            <div class="message user-message" id="usertext">
                ${message}
                <div class="timestamp">${getIndianTime()}</div>
            </div>
        `);
    }

    function showTypingIndicator() {
        $(".thetextdisplayer").append(`
            <div class="message bot-message typing-indicator-container">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `);
    }

    function removeTypingIndicator() {
        $(".typing-indicator-container").remove();
    }

    function respondMessage(message) {
        removeTypingIndicator(); // Remove the loader before appending the response
        $(".thetextdisplayer").append(`
            <div class="message bot-message" id="user-response">
                ${message}
                <div class="timestamp">${getIndianTime()}</div>
            </div>
        `);
    }

    function sendMessage() {
        let message = $("#themessage-sender").val().trim();
        if (message === "") {
            Swal.fire({
                icon: "warning",
                title: "Oops!",
                text: "Please type a message before sending.",
            });
            return;
        }

        console.log("Sending message:", message); // Debugging log
        appendMessage(message);
        showTypingIndicator(); // Show loader before the response

        $.ajax({
            url: "/message_Send/",
            type: "POST",
            headers: { "X-CSRFToken": getCsrfToken() },
            data: { message: message },
            success: function (response) {
                console.log("Response received:", response); // Debugging log
                respondMessage(response.message);
                $("#themessage-sender").val(""); 
            },
            error: function (xhr, status, error) {
                console.error("Error:", xhr.responseText); // Debugging log
                removeTypingIndicator();
                Swal.fire({
                    icon: "error",
                    title: "Error",
                    text: "Something went wrong. Please try again.",
                });
            }
        });
    }

    // Trigger message send on button click
    $("#send-btn").click(sendMessage);

    // Trigger message send on pressing Enter
    $("#themessage-sender").keypress(function (event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevent new line in input field
            sendMessage();
        }
    });
});
