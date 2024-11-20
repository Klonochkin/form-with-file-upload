document.getElementById("form").addEventListener("submit", (event) => {
  event.preventDefault();
  const filesInput = document.getElementById("files");
  const fileCount = filesInput.files.length;
  console.log(fileCount);
  const firstName = document.getElementById("first_name").value;
  const lastName = document.getElementById("last_name").value;
  const files = document.getElementById("files").files;

  const formData = new FormData();
  formData.append("first_name", firstName);
  formData.append("last_name", lastName);

  if (filesInput.files.length > 0) {
    for (let i = 0; i < filesInput.files.length; i++) {
      formData.append("files", filesInput.files[i]);
    }
  }
  sendForm(formData);
});

async function sendForm(formData) {
  try {
    await fetch("/sendForm", {
      method: "POST",
      body: formData,
    });
  } catch (error) {
    console.error("Ошибка:", error);
  }
}
