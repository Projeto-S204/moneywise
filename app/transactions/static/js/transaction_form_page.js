document.addEventListener("DOMContentLoaded", function () {
  const now = new Date();
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const currentTime = `${hours}:${minutes}`;
  console.log(currentTime);

  document.getElementById('transaction_date').value = now.toISOString().split('T')[0];
  document.getElementById('transaction_hour').value = currentTime;

  document.getElementById('is_recurring').addEventListener('change', () => {
    const startDateField = document.getElementById('start_date');
    const endDateField = document.getElementById('end_date');
    const frequencyField = document.getElementById('interval');

    if (document.getElementById('is_recurring').checked) {
      startDateField.style.display = 'block';
      endDateField.style.display = 'block';
      frequencyField.style.display = 'block';
    } else {
      startDateField.style.display = 'none';
      endDateField.style.display = 'none';
      frequencyField.style.display = 'none';
    }
  });
});