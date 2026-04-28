import { ShowAlert } from "./utils.js";

document.addEventListener("DOMContentLoaded", function(){
    displayGroup()

    const modal = document.getElementById('groupModal')

    document.getElementById('create-group').addEventListener('click',(e) => {
    e.preventDefault()
    
    modal.style.display = "flex";

    })

    modal.addEventListener('click',(e)=> {
        if (e.target == modal){
            closeModal()
        }
    })

    document.getElementById("create-group-btn").addEventListener("click",() => {
        createGroup()
    })

    document.getElementById("closeBtn").addEventListener("click",() =>{
        closeModal()
    })

    document.getElementById("addEmail").addEventListener("click",() =>{
        addEmail()
    })

});

// async function membername(){
//     try{
//         const response = await fetch("http://127.0.0.1:8000/api/group_member/",{
//             method:"GET",
//             headers: {
//                 "Content-Type":"Application/json"
//             }
//         });
//         const res = await response.json()
//         if (response.ok){
//             const data = res.
//         }
//     }
// }

export function closeModal(){
        document.getElementById('groupModal').style.display = "none";
}

//email addition
export function addEmail(){
    const container = document.getElementById('email-container')
    const div = document.createElement("div")
    div.classList.add("email-row")
    
    div.innerHTML=`
    <input type="email" placeholder="Enter email" class="email-detail">
    <button class="add-btn" onclick="addEmail()">+</button>
    `;
    container.appendChild(div);
}

//display group according to the user
async function displayGroup(){
    const accessToken = localStorage.getItem("access_token")
    try{
    const response = await fetch("http://127.0.0.1:8000/api/group/",{
        method: "GET",
        headers: {
            "Content-Type":"Application/json",
            "Authorization":`Bearer ${accessToken}`
        }
    });
    const res = await response.json()
    
    if (response.ok){
        const groupInfo = document.getElementById('groupInfo');
        groupInfo.innerHTML = ``;

        res.data.forEach(data =>{

            //group container
            const groupDiv = document.createElement('div');
            groupDiv.classList.add('group-container')

            //title of the group
            const header = document.createElement('div');
            header.classList.add('group-header');

            const actions = document.createElement('div');
            actions.classList.add('group-actions')

            const editBtn = document.createElement('button')
            editBtn.classList.add('edit-btn');
            editBtn.textContent = 'Edit';

            const deleteBtn = document.createElement('button')
            deleteBtn.classList.add('delete-btn')
            deleteBtn.textContent = 'Delete';

            actions.appendChild(editBtn)
            actions.appendChild(deleteBtn)

            const title = document.createElement('h3')
            title.textContent = data.name

            //card to show memebers
            const card = document.createElement('div');
            card.classList.add('card')
        
            let memberHTML = `<h3>Members</h3>`
            
            data.members.forEach(member=>{
                memberHTML += `<p>${member.username}</p>`
                })
            card.innerHTML = memberHTML
            
            header.appendChild(title)
            header.appendChild(actions)
            groupDiv.appendChild(header)
            groupDiv.appendChild(card)
            groupInfo.appendChild(groupDiv)
        })
    
        
    }
}catch(error){
        ShowAlert("Something went wrong");
        console.log(error)
    }
}

//creating the group
async function createGroup(){

    let emails  = [];
    const accessToken = localStorage.getItem("access_token")
    const name = document.getElementById('group-name').value
    const currency = document.getElementById('currency-type').value

    const emailInputs = document.querySelectorAll('.email-detail')
    emailInputs.forEach(email => {
        if(email.value.trim() !== ""){
            emails.push(email.value)
        }
        
    });
    
    try{
        const response = await fetch("http://127.0.0.1:8000/api/group/",{
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${accessToken}`
        },
        body: JSON.stringify({
            name:name,
            currency:currency,
            email:emails
        })
    });
    const res = await response.json();
    if (response.ok){
        ShowAlert("Group created successfully!")
    }else{
        ShowAlert("Error:" +JSON.stringify(res) )
    }
    }catch(error){
        ShowAlert("Something went wrong");
    }
    
}

// async function deleteGroup(){
//     try{
//         const deleteBbtn = document.querySelectorAll('deleteBtn')
//     }
// }