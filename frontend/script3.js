token = sessionStorage.getItem("token");
if (token == null) {
    window.location.href = './login.html'
}
let url = document.getElementById('url');
let btn = document.getElementById('submit');
let short_url = document.getElementById("short_url");
let lgout = document.getElementById("logout");

async function generate_url() {
    short_url.innerText= '';
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
    catch(err) {
        console.log(err);
    }
}

function logout() {
    sessionStorage.removeItem("token");
    location.reload()
}

btn.addEventListener("click", generate_url);
lgout.addEventListener("click", logout);