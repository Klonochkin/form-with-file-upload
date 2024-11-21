getData();

document.getElementById("form").addEventListener("submit", (event) => {
  event.preventDefault();
  const formData = new FormData(event.target);
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

async function getData() {
  try {
    const response = await fetch("/data");
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const posts = await response.json();
    const postsList = document.getElementById("data");

    postsList.textContent = JSON.stringify(posts, null, 2);

    console.log(posts);
  } catch (error) {
    console.error("There was a problem with the fetch operation:", error);
  }
}
