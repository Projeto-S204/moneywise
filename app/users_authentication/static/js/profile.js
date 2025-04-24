document.addEventListener("DOMContentLoaded", () => {
  const editBtn = document.getElementById("edit-btn");
  const inputs = document.querySelectorAll(".info input");
  const title = document.querySelector("h2");

  let originalValues = [];
  let buttonWrapper = null;

  // Botões de ação
  const cancelBtn = document.createElement("button");
  cancelBtn.textContent = "Cancelar";
  cancelBtn.classList.add("btn-cancelar");

  const saveBtn = document.createElement("button");
  saveBtn.textContent = "Salvar";
  saveBtn.classList.add("btn-salvar");

  // Lógica de cancelar edição
  cancelBtn.addEventListener("click", () => {
    title.firstChild.textContent = "Perfil";
    inputs.forEach((input, i) => {
      input.value = originalValues[i];
      input.disabled = true;
      input.style.backgroundColor = "#0F0F10";
      input.style.color = "#FFFFFF";
    });

    buttonWrapper.remove();
    buttonWrapper = null;
    editBtn.style.display = "inline";
  });

  // Lógica de salvar as alterações
  saveBtn.addEventListener("click", () => {
    const [name, email, birthday] = [...inputs].map((input) => input.value);

    // Converte a data de nascimento para o formato adequado (YYYY-MM-DD) para o backend
    const formattedBirthday = new Date(birthday.split("/").reverse().join("-"))
      .toISOString()
      .split("T")[0];

    // Envia os dados para a rota do servidor
    fetch("/profile/update", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, email, birthday: formattedBirthday }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          alert("Perfil atualizado com sucesso!");
          location.reload();
        } else {
          alert("Erro ao atualizar perfil.");
        }
      });
  });

  // Lógica de editar perfil
  editBtn.addEventListener("click", () => {
    title.firstChild.textContent = "Editar Perfil";
    editBtn.style.display = "none";

    originalValues = Array.from(inputs).map((input) => input.value);
    inputs.forEach((input) => {
      input.disabled = false;
      input.style.backgroundColor = "#D9D9D9";
      input.style.color = "#000000";
    });

    buttonWrapper = document.createElement("div");
    buttonWrapper.classList.add("button-wrapper");
    buttonWrapper.appendChild(cancelBtn);
    buttonWrapper.appendChild(saveBtn);

    document.querySelector(".info").appendChild(buttonWrapper);
  });

  // Lógica de deletar a conta com confirmação
  const deleteBtn = document.getElementById("delete-account-btn");
  const deleteModal = document.getElementById("delete-confirm-modal");
  const cancelDeleteBtn = document.getElementById("cancel-delete-btn");
  const confirmDeleteBtn = document.getElementById("confirm-delete-btn");

  if (deleteBtn) {
    deleteBtn.addEventListener("click", (e) => {
      e.preventDefault();
      // Exibe o modal de confirmação de exclusão
      deleteModal.style.display = "block";
    });

    // Cancelar a exclusão
    cancelDeleteBtn.addEventListener("click", () => {
      deleteModal.style.display = "none"; // Fecha o modal
    });

    // Confirmar a exclusão
    confirmDeleteBtn.addEventListener("click", () => {
      document.getElementById("delete-account-form").submit(); // Envia o formulário para deletar a conta
    });
  }
});
