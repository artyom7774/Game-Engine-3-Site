function changeLanguage(language) {
    console.log("change language:", language);

    fetch("/setLanguage", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: "id=" + language
    })
    .then(response => response.json())
    .then(data => {
        document.open();
        document.write(data["text"]);
        document.close();
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

function updateOnline(online) {
    const widget = document.getElementById("footer__another__text__online");

    if (widget) {
        widget.textContent = "Online: " + online;
    }
}
