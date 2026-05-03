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
            
            groupDiv.addEventListener('click',()=>{
                window.location.href = `http://127.0.0.1:5501/RoomEase/frontend/html/group.html?id=${data.id}`
            })

            //title of the group
            const header = document.createElement('div');
            header.classList.add('group-name');

            const actions = document.createElement('button');
            actions.classList.add('quick-actions')
            actions.innerHTML = `<i class="fa-solid fa-right-from-bracket"></i> Leave`;
           
            actions.addEventListener('click', () => {
                console.log("leave is clicked");
                leaveGroup(data.id,groupDiv);
            });

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

async function leaveGroup(id,groupDiv){
    const accessToken = localStorage.getItem('access_token');
    
    try{
        const response = await fetch(`http://127.0.0.1:8000/api/group_member/${id}/`,{
            method:'DELETE',
            headers:{
            "Authorization":`Bearer ${accessToken}`
            }
        });
        const res = await response.json()
        if(response.ok){
            ShowAlert("You left the group!")
            groupDiv.remove()
            

        }
    }catch(error){
        ShowAlert("Something went wrong");
        console.log(error)
    }
}