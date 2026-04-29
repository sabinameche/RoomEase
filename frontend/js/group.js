import { ShowAlert } from "./utils.js";

document.addEventListener("DOMContentLoaded", async function(){
    await loadModal();
    displayGroup();

    const modal = document.getElementById('groupModal');

    // Single event delegation for all clicks
    document.addEventListener("click", (e) => {
        const target = e.target;

        // Create Group Button
        if (target.id === 'create-group') {
            e.preventDefault();
            openModal('create');
        }

        // Close Modal Button
        if (target.classList.contains('closeBtn') || target.id === 'closeBtn') {
            closeModal();
        }

        // Add Email Button
        if (target.classList.contains('addEmail')) {
            e.preventDefault();
            addEmail();
        }

        // Edit Button
        if (target.classList.contains('edit-btn')) {
            console.log('id aru pani aaunu parxa',target.dataset.groupId)
            const editGroupBtn = document.getElementById('edit-group-btn')
            editGroupBtn.dataset.groupId = target.dataset.groupId;

            console.log('ya ni same id aaunu parxa haii',editGroupBtn.dataset.groupId)
            openModal('edit');
        }

        // Delete Button
        if (target.classList.contains('delete-btn')) {
            // Find the group container and ID
            const groupDiv = target.closest('.group-container');
            const groupName = groupDiv.querySelector('h3').textContent;
            const groupId = target.dataset.groupId; 
            
            if (confirm(`Delete group "${groupName}"?`)) {
                deleteGroup(groupDiv, groupId);
            }
        }

        // Create Group 
        if (target.id === 'create-group-btn') {
            createGroup();
        }

        // Edit Group 
        if (target.id === 'edit-group-btn') {
            const Id = target.dataset.groupId;
            console.log(Id,'id audae xa ki nai')
            editGroup(Id);
        }
    });

    // Modal background click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });
});

function openModal(mode = 'create') {
    const modal = document.getElementById('groupModal');
    const emailContainer = document.getElementById('email-container');
    
    // Reset email container
    emailContainer.innerHTML = `
        <div class="email-row">
            <input type="email" placeholder="Enter email" class="email-detail">
            <button class="addEmail" type="button">+</button>
        </div>
    `;
    
    if (mode === 'create') {
        document.getElementById('group-form-title').textContent = 'Create Group';
        document.getElementById('email-box').style.display = 'flex';
        document.getElementById('edit-group-btn').style.display = 'none';
        document.getElementById('create-group-btn').style.display = 'flex';
    } else {
        document.getElementById('group-form-title').textContent = 'Edit Group';
        document.getElementById('email-box').style.display = 'none';
        document.getElementById('edit-group-btn').style.display = 'flex';
        document.getElementById('create-group-btn').style.display = 'none';
    }
    
    modal.style.display = "flex";
}

export function closeModal(){
    document.getElementById('groupModal').style.display = "none";
}

export function addEmail(){
    const container = document.getElementById('email-container');
    const div = document.createElement("div");
    div.classList.add("email-row");
    
    div.innerHTML = `
        <input type="email" placeholder="Enter email" class="email-detail">
        <button class="addEmail" type="button">+</button>
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

            const editBtn = document.createElement('button');
            
            editBtn.classList.add('edit-btn');
            editBtn.dataset.groupId = data.id;
            editBtn.textContent = 'Edit';
            
            
            const deleteBtn = document.createElement('button');
            deleteBtn.classList.add('delete-btn');
            deleteBtn.dataset.groupId = data.id;
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
    const createGroupBtn = document.getElementById('create-group-btn');

    const originalText = createGroupBtn.innerHTML;
    createGroupBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating...';
    createGroupBtn.disabled = true;

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
            currency:currency || 'NPR',
            email:emails || []
        })
    });
    const res = await response.json();

    if (response.ok){
        ShowAlert("Group created successfully!")
        
        setTimeout(() => {
            createGroupBtn.innerHTML = originalText;
            createGroupBtn.disabled = false
            closeModal()
        },2000);

    }else{
        ShowAlert("Error:" +JSON.stringify(res) )
    }
    }catch(error){
        ShowAlert("Something went wrong");
    }
    
}


async function editGroup(Id){

    const accessToken = localStorage.getItem('access_token');
    const name = document.getElementById('group-name').value;
    const currency = document.getElementById('currency-type').value;
    const editGroupBtns = document.getElementById('edit-group-btn');

    const originalText = editGroupBtns.innerHTML;
    editGroupBtns.innerHTML = '<i class = "fas fa-spinner fa-spin"></i>Editing...'
    editGroupBtns.disabled = true;

    try{
        const response = await fetch(`http://127.0.0.1:8000/api/group/${Id}/`,{
            method:"PATCH",
            headers:{
                "Content-Type":"application/json",
                "Authorization":`Bearer ${accessToken}`
            },
            body: JSON.stringify({
                name :name,
                currency :currency || 'NPR',
               
            })
        });

        const res = await response.json();
        console.log(response.status);
        console.log(res);
        if(response.ok){
            ShowAlert("Group created successfully!");
    
            
            setTimeout(() => {
                editGroupBtns.innerHTML = originalText;
                editGroupBtns.disabled = false;
                closeModal();
            }, 2000);
        }else{
            ShowAlert("Error:" +JSON.stringify(res) )
        }
    }catch(error){
        ShowAlert("Something went wrong");
        
    }


}

async function deleteGroup(groupDiv,groupId){
    const accessToken = localStorage.getItem('access_token')
    try{
        const response = await fetch(`http://127.0.0.1:8000/api/group/${groupId}/`,{
            method:"DELETE",
            headers:{
                "Content-Type":"Application/json",
                "Authorization":`Bearer ${accessToken}`
            }
        });
        
        if(response.ok){
            ShowAlert("Group deleted successfully!!")
            //remove UI
            groupDiv.remove()
        }
        else{
            console.log("Backend error:", err);
        }


    }catch(error){
        ShowAlert("Something went wrong!")
    }
}

