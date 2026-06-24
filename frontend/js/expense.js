import { ShowAlert } from "./utils.js";
document.addEventListener('DOMContentLoaded',() =>{
    // open expense modal
        const addExpense = document.getElementById('addExpense');
        addExpense.addEventListener('click',()=>{
            document.getElementById('expense-header-title').innerText = 'Create Expense'
            document.getElementById('select-participants').style.display = 'flex';
            document.getElementById('createExpense').style.display = 'flex';
            document.getElementById('editExpense').style.display = 'none';
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
    if(paid_by_member){
        paid_by_member.addEventListener('change',(e) =>{
            selectpaidById = e.target.value;

        })
    }
    
    // creating new expense
    const expenseCreate = document.getElementById('createExpense');
    if(expenseCreate){
        expenseCreate.addEventListener('click',()=>{
        createExpense(selectpaidById)
    })
    }

})


// create expense
async function createExpense(paidBy ){
    const accessToken = localStorage.getItem("access_token")
    const params = new URLSearchParams(window.location.search)
    const groupId = params.get("id")
    const expenseTitle = document.getElementById("expense-name").value;
    const expenseAmount = document.getElementById("expense-amount").value;

    const expenseCategory = document.getElementById("expenseCategory").value;

    const splitType = document.getElementById('split-amount').value;
    const participants = {}
    if(splitType == "EQUAL"){
        const checkedParticipants = document.querySelectorAll('.participant-checkbox:checked')
        checkedParticipants.forEach(user=>{
            participants[user.value] = 0
        })
    }


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
            participants:participants || 
            {},
            category:expenseCategory,
            split_type:splitType

        })
        
    });

    const res = await response.json();
    
    if(response.ok){
        ShowAlert("Expense created successfully!")
        document.getElementById('expenseModal').style.display = 'none';
        
    }
    else{
        ShowAlert("Error:" +JSON.stringify(res) )}

    }catch(error){
        ShowAlert("Something went wrong")
    }
    
}

export async function displayExpense(){
    const accessToken = localStorage.getItem("access_token")
    const params = new URLSearchParams(window.location.search);
    const groupId = params.get("id")

    try{

    const response = await fetch(`http://127.0.0.1:8000/api/expense/total/${groupId}/`,{
        method: "GET",
        headers: {
            "Content-Type":"application/json",
            "Authorization":`Bearer ${accessToken}`
        }

    }),
    
        res =  await response.json()
        if(response.ok){

            const expenseList = document.getElementById("expense-list");
            expenseList.innerHTML = "";

            res.data.forEach(expense => {
    
                const expenseDiv = document.createElement('div');
                const expenseTDiv = document.createElement('div');
                const expenseH = document.createElement('h3')
                expenseH.textContent = expense.title
                const expenseP = document.createElement('p');
                expenseP.textContent = `Paid by ${expense.user_name}`
                const expenseSpan = document.createElement('span')
                expenseSpan.innerHTML = `${expense.amount} <button data-id = "${expense.id}" class = 'edit-expense'>edit</button> <button data-id= "${expense.id}" class='delete-expense' >delete</button>`
                             
                expenseDiv.appendChild(expenseH)
                expenseDiv.appendChild(expenseP)
                expenseTDiv.appendChild(expenseSpan)

                const row = document.createElement("div");
                row.classList.add("expense-row");

                row.appendChild(expenseDiv);
                row.appendChild(expenseTDiv);
                
                expenseList.appendChild(row);

            });
            


        }
    }catch(error){
        ShowAlert("Something went wrong")
    }

}

let expenseId = null
document.addEventListener('click',(e)=>{
    const target = e.target
    
    if(target.classList.contains('edit-expense')){
        expenseId = target.dataset.id
        
        document.getElementById('expense-header-title').innerText = 'Edit Expense'
        document.getElementById('select-participants').style.display = 'none';
        document.getElementById('createExpense').style.display = 'none';
        document.getElementById('editExpense').style.display = 'flex';
        openExpense();
        fillExpenseForm(expenseId)
    } 

    // editing expense
    if(target.classList.contains('edit-expense-btn')){
      
        editExpense(expenseId)
    }

    // deleting expense
    if(target.classList.contains('delete-expense')){
        const id = target.dataset.id
        console.log('yaa value xaina rw kina po',id)
        deleteExpense(id)
    }
})

async function fillExpenseForm(id){
    const response = await fetch(`http://127.0.0.1:8000/api/expense/single/${id}/`,{
        method:"GET",
        headers:{
            'Content-Type':'application/json'
        }
    }
    )
    const res = await response.json()
    document.getElementById('expense-name').value = res.data.title
    document.getElementById('expense-amount').value = res.data.amount
    document.getElementById('expenseCategory').value = res.data.category
    document.getElementById('paid_by_list').value = res.data.paid_by
    
}


// edit  expense
async function editExpense(expenseId){
    const accessToken = localStorage.getItem('access_token')
    const titleInput = document.getElementById('expense-name').value
    const amountInput = document.getElementById('expense-amount').value
    const categoryInput = document.getElementById('expenseCategory').value
    const paidByInput = document.getElementById('paid_by_list').value
    // const splitInput = document.getElementById('split-amount').value

    try{
        const res = await fetch(`http://127.0.0.1:8000/api/expense/${expenseId}/`,{
            method:"PATCH",
            headers:{
                "Content-Type":"application/json",
                "Authorization":`Bearer ${accessToken}`
            },
            body:JSON.stringify({
                title:titleInput,
                amount:amountInput,
                paid_by:paidByInput,
                category:categoryInput
            })
        })

        if(res.ok){
            ShowAlert("Expense updated successfully!")
            document.getElementById('expenseModal').style.display = 'none';
        }

    }catch(error){
        ShowAlert("Something went wrong here!")
    }
}

// delete expense
async function deleteExpense(id){
    console.log('lets see the id',id)
    const accessToken = localStorage.getItem('access_token');
    try{
        const response = await fetch(`http://127.0.0.1:8000/api/expense/${id}/`,{
        method:"DELETE",
        headers:{
            "Authorization":`Bearer ${accessToken}`
        }
    })
    if(response.ok){
        ShowAlert("Expense deleted successfully!")
        
    }

    }catch(error){
        ShowAlert("Something went wrong while deleting the expense!")
    }
    
}