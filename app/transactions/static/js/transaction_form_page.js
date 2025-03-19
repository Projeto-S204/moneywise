function setTransactionType(type) {
  document.getElementById('transaction_type').value = type;
  console.log('entrou aqui')
}

function changeButtonColor(button) {
  document.querySelectorAll('.transaction-type-buttons button').forEach(btn => {
    btn.classList.remove('active');
    btn.style.backgroundColor = '';
  });

  document.querySelectorAll('.transaction-type-buttons .income-btn').forEach(btn => {
    btn.style.color = '#92CA7E';
  });
  document.querySelectorAll('.transaction-type-buttons .expense-btn').forEach(btn => {
    btn.style.color = '#CA7E7E';
  });

  button.classList.add('active');

  if (button.classList.contains('income-btn')) {
    button.style.backgroundColor = '#92CA7E';
    button.style.color = '#18181B';
  } else if (button.classList.contains('expense-btn')) {
    button.style.backgroundColor = '#CA7E7E';
    button.style.color = '#18181B';
  }
}