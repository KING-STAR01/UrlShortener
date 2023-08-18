let btn = document.getElementById('submit');
let uname = document.getElementById('uname');
let fname = document.getElementById('fname');
let lname = document.getElementById('lname');
let pass = document.getElementById('password');
let email = document.getElementById('email');
let log = document.getElementById('login');
let log_name = document.getElementById('login_name');
let log_pas = document.getElementById('login_pass');

async function register() {
    if (uname.value === '') {
        alert("username can't be empty");
        return
    }
    if (fname.value === '') {
        alert("firstname can't be empty");
        return
    }
    if (lname.value === '') {
        alert("lastname can't be empty");
        return
    }
    if (pass.value === '') {
        alert("password can't be empty");
        return
    }
    if (email.value === '') {
        alert("email can't be empty");
        return
    }
    let body1 = {}
    body1.username = uname.value;
    body1.password = pass.value;
    body1.password2 = pass.value;
    body1.email = email.value;
    body1.firs_tname = fname.value;
    body1.last_name = lname.value;

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
        resp = await fetch('http://127.0.0.1:8000/api/register/', requestOptions);
        res = await resp.json();
        console.log(res)
    }
    catch(err) {
        console.log(err)
    }
    finally {
        uname.value = '';
        pass.value = '';
        email.value = '';
        fname.value = '';
        lname.value = '';
    }
    if (resp.status == 400) {
        alert(JSON.stringify(res))
    }
    else {
        alert("user created sucessfully please login")
    }
}
btn.addEventListener('click', register);