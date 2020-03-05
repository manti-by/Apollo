getJSON = (url, success, error) => {
    let request = new XMLHttpRequest();

    request.open("GET", url, true);
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest");

    request.onreadystatechange = () => {
        if (request.readyState === XMLHttpRequest.DONE) {
            if (request.status >= 200 && request.status < 400) {
                let json = JSON.parse(request.responseText);
                success(json);
            } else {
                error();
            }
        }
    };
    request.send();
};

