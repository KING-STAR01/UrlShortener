token = sessionStorage.getItem("token");
if (token == null) {
    window.location.href = './login.html'
}
let url = document.getElementById('url');
let btn = document.getElementById('submit');
let short_url = document.getElementById("short_url");
let lgout = document.getElementById("logout");
let all_urls = document.getElementById("getall");
let url_text = document.getElementById("all_urls");

async function generate_url() {
    short_url.innerText = '';
    if (url.value == "") {
        alert("url cannot be empty");
        return
    }
    let body1 = {};
    body1.long_url = url.value;
    let long_url = url.value;
    let requestOptions = {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "Authorization": token
        },
        body: JSON.stringify(body1)
    }
    try {
        let resp = await fetch("http://localhost:8000/api/url/", requestOptions);
        let res = await resp.json();
        console.log(JSON.stringify(res));
        short_url.innerText = "http://localhost:8000/api/" + res.short_url;
        short_url.style.background = '#e1eaea';
    }
    catch (err) {
        console.log(err);
    }
}

function logout() {
    sessionStorage.removeItem("token");
    location.reload()
}

async function get_all_urls() {
    url_text.innerText = '';

    let long_url = url.value;
    let requestOptions = {
        method: "GET",
        headers: {
            "Authorization": token
        }
    }
    try {
        let resp = await fetch("http://localhost:8000/api/all_urls/", requestOptions);
        let res = await resp.json();
        console.log(JSON.stringify(res));
        for (let i = 0; i < res.length; i++) {
            let long_url = res[i].long_url;
            let short_url = res[i].short_url;

            let ul = document.createElement('ul');
            let li1 = document.createElement('li');
            li1.setAttribute("id","long_url_id");
            let li2 = document.createElement('li');
            li2.setAttribute("id", "short_url_id");
            let white_space = document.createTextNode("              ");

            li1.appendChild(document.createTextNode("long_url:" ));
            li1.appendChild(white_space);
            li1.appendChild(document.createTextNode(long_url));
            li2.appendChild(document.createTextNode("short_url: " + "http://localhost:8000/api/" + short_url));
            ul.appendChild(li1);
            ul.appendChild(li2);
            url_text.appendChild(ul)
        }
    }
    catch (err) {
        console.log(err);
    }
}

btn.addEventListener("click", generate_url);
lgout.addEventListener("click", logout);
all_urls.addEventListener("click", get_all_urls);