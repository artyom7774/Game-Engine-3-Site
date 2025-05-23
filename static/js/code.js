function clickHandler(id) {
    fetch('/click', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'id=' + id
    })
    .then(response => response.json())
    .then(data => {
        document.getElementsByClassName("main")[0].innerHTML = `${data.body}`;
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}

function changeLanguage(language) {
    fetch('/setLanguage', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'id=' + language
    })
    .then(response => response.json())
    .then(data => {
        document.getElementsByClassName("main")[0].innerHTML = `${data.body}`;
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}