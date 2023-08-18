
let btn = document.getElementById('login');
let uname = document.getElementById('uname');
let pass = document.getElementById('password');

async function login() {
    if (uname.value === '') {
        alert("username can't be empty");
        return
    }
    if (pass.value === '') {
        alert("password can't be empty");
        return
    }
    let body1 = {};
    body1.username = uname.value;
    body1.password = pass.value;

    var requestOptions = {
        method: "POST",
        // mode: "cors",
        headers: {
            "content-type": "application/json",
        },
        body: JSON.stringify(body1)
    }
    let resp = "some error occured";
    let res;
    try {
        resp = await fetch('http://127.0.0.1:8000/api/get_token/', requestOptions);
        res = await resp.json();
        console.log(res)
    }
    catch(err) {
        console.log(err)
    }
    finally {
        uname.value = '';
        pass.value = '';
    }
    if (resp.status == 400) {
        alert(JSON.stringify(res))
    }
    else {
        console.log(res.token);
        sessionStorage.setItem("token", res.token); 
        alert("login successfull")
        window.location.href = "./index.html"
    }
}
btn.addEventListener('click', login);