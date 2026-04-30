import { ShowAlert } from "./utils.js";

document.addEventListener('DOMContentLoaded',()=>{
    displayGroup()
})
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
        const grouplist = document.getElementById('groupList');
        grouplist.innerHTML = ``;

        res.data.forEach(data =>{

            //group container
            const groupDiv = document.createElement('div');
            groupDiv.classList.add('group')

            //title of the group
            const header = document.createElement('div');
            header.classList.add('group-name');

            const actions = document.createElement('div');
            actions.classList.add('quick-actions')

            const name = document.createElement('h3')
            name.textContent = data.name
            
            const card = document.createElement('div')
            card.classList.add('card')
            card.textContent = `${data.count_members} members`

            header.appendChild(name)
            header.appendChild(actions)
            groupDiv.appendChild(header)
            groupDiv.appendChild(card)
            grouplist.appendChild(groupDiv)
            
        })
    
        
    }
}catch(error){
        ShowAlert("Something went wrong");
        console.log(error)
    }
}