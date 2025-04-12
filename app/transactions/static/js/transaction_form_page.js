function setTransactionType(type) {
  document.getElementById("transaction_type").value = type;
}

function changeButtonColor(button) {
  document
    .querySelectorAll(".transaction-type-buttons button")
    .forEach((btn) => {
      btn.classList.remove("active");
      btn.style.backgroundColor = "";
      btn.style.color = btn.classList.contains("income-btn")
        ? "#92CA7E"
        : "#CA7E7E";
    });

  if (button) {
    button.classList.add("active");
    button.style.backgroundColor = button.classList.contains("income-btn")
      ? "#92CA7E"
      : "#CA7E7E";
    button.style.color = "#18181B";
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const transactionType = document
    .getElementById("transaction_type")
    .value.trim();

  if (transactionType === "income") {
    changeButtonColor(document.getElementById("income-btn"));
  } else if (transactionType === "expense") {
    changeButtonColor(document.getElementById("expense-btn"));
  }
});

function toggleNumberOfPayments() {
  var checkbox = document.getElementById("checkbox");
  var numberOfPayments = document.getElementById(
    "number-of-payments-container"
  );
  var numberOfPaymentsInput = document.getElementById(
    "number-of-payments-container"
  );

  if (checkbox.checked) {
    numberOfPayments.style.display = "block";
    numberOfPaymentsInput.setAttribute("required", "required");
  } else {
    numberOfPayments.style.display = "none";
    numberOfPaymentsInput.removeAttribute("required");
  }
}

window.onload = function () {
  toggleNumberOfPayments();
};

document
  .getElementById("checkbox")
  .addEventListener("change", toggleNumberOfPayments);

document.querySelectorAll("select option").forEach((option) => {
  if (option.disabled) {
    option.style.color = "gray";
  } else {
    option.style.color = "white";
  }
});
