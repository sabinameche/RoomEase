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
    console.log('group ko id kati aayo',groupId)
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

        paid_by_list.innerHTML = '';

        response.data.forEach(member => {
            
            const paid_by_member = document.createElement('option');
            paid_by_member.classList.add('paid-by-member');
           
            paid_by_member.textContent = member.username;
            paid_by_list.appendChild(paid_by_member)
        });
    }
    document.getElementById('expenseModal').style.display = 'flex';
}catch(error){
        ShowAlert("Something went wrong");
        console.log(error)
    }

}