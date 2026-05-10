document.addEventListener('DOMContentLoaded',() =>{
    // open expense modal
        const addExpense = document.getElementById('addExpense');
        addExpense.addEventListener('click',()=>{
            console.log('am i clicking')
            document.getElementById('expenseModal').style.display = 'flex';
        })

    // close expense modal
    document.getElementById('closeExpenseBtn').addEventListener('click',()=>{
        document.getElementById('expenseModal').style.display = 'none';
    })
})