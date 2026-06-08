import { ShowAlert } from "./utils.js";
document.addEventListener('DOMContentLoaded',() =>{
    // open expense modal
        const addExpense = document.getElementById('addExpense');
        addExpense.addEventListener('click',()=>{

            openExpense()
        })

    // close expense modal
    const closeExpenseBtn = document.getElementById('closeExpenseBtn')
    if(closeExpenseBtn){
        closeExpenseBtn.addEventListener('click',()=>{

        document.getElementById('expenseModal').style.display = 'none';
    })
    }

    const expenseModal = document.getElementById('expenseModal');
    document.addEventListener('click',(e)=>{
        if(e.target === expenseModal){
            document.getElementById('expenseModal').style.display = 'none';
        };

    })
})

// open expense modal
async function openExpense(){
    const params = new URLSearchParams(window.location.search)
    const groupId = params.get("id");
    
    const accessToken = localStorage.getItem('access_token');
    try{
    const res = await fetch(`http://127.0.0.1:8000/api/group_member/${groupId}/`,{
        method:"GET",
        headers:{
            'Content-Type':'Application/json',
            'Authorization':`Bearer ${accessToken}`
        }
    });
    const response = await res.json()
  
    console.log(response)
    if(res.ok){

        const paid_by_list = document.querySelector('.paid-by-list');
        const participants = document.querySelector('.participants-list')

        paid_by_list.innerHTML = '';
        participants.innerHTML = '';

        response.data.forEach(member => {
            
            const paid_by_member = document.createElement('option');
            paid_by_member.classList.add('paid-by-member');
            
           
            paid_by_member.textContent = member.username;
            paid_by_member.value = member.user_id;
            paid_by_list.appendChild(paid_by_member);

            // participants
            const wrapper = document.createElement('div');

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';

            checkbox.value = member.user_id;

            checkbox.classList.add('participant-checkbox');

            const label = document.createElement('label');
            label.textContent = member.username;
            wrapper.appendChild(checkbox);
            wrapper.appendChild(label);

            participants.appendChild(wrapper);
                });
            }
    document.getElementById('expenseModal').style.display = 'flex';
}catch(error){
        ShowAlert("Something went wrong");
        console.log(error)
    }

}



// create expense button

document.addEventListener('DOMContentLoaded',()=>{
    const paid_by_member = document.getElementById('paid_by_list');

    let selectpaidById = null
    // id for selected paid_by user
        paid_by_member.addEventListener('change',(e) =>{
            console.log(paid_by_member)
            selectpaidById = e.target.value;

        })
    
    const expenseCreate = document.getElementById('createExpense');
    expenseCreate.addEventListener('click',()=>{
        createExpense(selectpaidById)
    })
})


// create expense
async function createExpense(paidBy ){
    const accessToken = localStorage.getItem("access_token")
    const params = new URLSearchParams(window.location.search)
    const groupId = params.get("id")
    const expenseTitle = document.getElementById("expense-name").value;
    const expenseAmount = document.getElementById("expense-amount").value;
    
    const checkedParticipants = document.querySelectorAll('.participant-checkbox:checked')
    const participantsIds = Array.from(checkedParticipants).map(user=>user.value)

    console.log(expenseTitle,expenseAmount,groupId,paidBy,participantsIds)
    try{
        const response = await fetch(`http://127.0.0.1:8000/api/expense/${groupId}/`,{
        method: "POST",
        headers: {
            "Content-Type":"application/json",
            "Authorization":`Bearer ${accessToken}`
            
        },
        body: JSON.stringify({
            title:expenseTitle,
            amount:expenseAmount,
            paid_by:Number(paidBy),
            participants:participantsIds || []

        })
        
    });

    const res = await response.json();
    console.log(res,'aaudae xa kun res yaa ani res ma xa chai k tw')
    if(response.ok){
        ShowAlert("Expense created successfully!")
        
    }
    else{
        ShowAlert("Error:" +JSON.stringify(res) )}

    }catch(error){
        ShowAlert("Something went wrong")
    }
    
}