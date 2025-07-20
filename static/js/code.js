function changeLanguage(language) {
    console.log("change language:", language);

    fetch('/setLanguage', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'id=' + language
    })
    .then(response => response.json())
    .then(data => {
        document.open();
        document.write(data["text"]);
        document.close();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
