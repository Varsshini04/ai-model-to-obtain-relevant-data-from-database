document.getElementById("submitQuery").addEventListener("click", () => {
    const queryInput = document.getElementById("queryInput");
    const chatArea = document.getElementById("chatArea");

    const userQuery = queryInput.value;

    if (!userQuery) return;

    const userMessage = document.createElement("div");
    userMessage.className = "message user-message";
    userMessage.textContent = userQuery;
    chatArea.appendChild(userMessage);
    queryInput.value = "";

    fetch("http://127.0.0.1:5000/api/query", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: userQuery }),
    })
        .then((response) => response.json())
        .then((data) => {
            const botMessage = document.createElement("div");
            botMessage.className = "message bot-message";
            botMessage.textContent = data.response;
            chatArea.appendChild(botMessage);
            chatArea.scrollTop = chatArea.scrollHeight;
        })
        .catch((error) => {
            console.error("Error:", error);
        });
});
