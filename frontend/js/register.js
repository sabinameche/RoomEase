// user registration

const registerBtn = document.getElementById("register")
if(registerBtn!=null){
registerBtn.addEventListener("click", async function(e) {
    e.preventDefault();
    registerUser()
})
}
async function registerUser(){

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const originalText = registerBtn.innerHTML;
    registerBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Registering...';
    registerBtn.disabled = true;

    try{
        const response = await fetch("http://127.0.0.1:8000/api/register/",{
            method : "POST",
            headers :{
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });
        const data = await response.json();
        if (response.ok){
            alert("Registration Successfull")
            window.location.href = "http://127.0.0.1:5501/RoomEase/frontend/html/login.html"

        }else{
            alert("Error:" +JSON.stringify(data) )
        }
    }
    catch(error){
    console.error(error);
    alert("Something went wrong");
}finally {
        // Restore button state
        registerBtn.innerHTML = originalText;
        registerBtn.disabled = false;
}


}
// user login

const loginBtn = document.getElementById('login');
loginBtn.addEventListener("click",async function(e){

    console.log("gererere??here")
    e.preventDefault();
    loginUser();
})


async function loginUser(){
    console.log("should be here.....")
    const username = document.getElementById("name").value;
    const password = document.getElementById("pass").value;
    const loginBtn = document.getElementById('login');

    const originalText = loginBtn.innerHTML;
    loginBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging in...';
    loginBtn.disabled = true;

    try{
        const response = await fetch('http://127.0.0.1:8000/api/login/',{
            method : "POST",
            headers : {
                "Content-Type":"application/json"
            },
            body: JSON.stringify({
                username :username,
                password : password
            })
        });
        const data = await response.json()
        console.log("refresh token",data.refresh_token)
        console.log("access_token",data.access_token)
        if(response.ok){
            alert("Login Successfull")
        }else{
            alert("Error:" +JSON.stringify(data) )
        }
    }catch(error){
        console.error(error);
        alert("Something went wrong");
    }finally {
        // Restore button state
        loginBtn.innerHTML = originalText;
        loginBtn.disabled = false;
}
}