function appendMessage(text, role){
  const chat = document.getElementById("chat");
  const div = document.createElement("div");
  div.className = "msg " + role;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

async function sendQuestion(questionText){
  if(!questionText) return;
  appendMessage(questionText, "user");
  document.getElementById("user-input").value = "";
  try {
    const resp = await fetch("/ask", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({question: questionText})
    });
    const data = await resp.json();
    appendMessage(data.answer || "No response", "bot");
  } catch (e) {
    appendMessage("Network error. Please try again.", "bot");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("user-input");
  const btn = document.getElementById("send-btn");
  const select = document.getElementById("qa-select");

  btn.addEventListener("click", () => {
    const text = input.value.trim();
    if(text) sendQuestion(text);
  });

  input.addEventListener("keydown", (e) => {
    if(e.key === "Enter"){
      const text = input.value.trim();
      if(text) sendQuestion(text);
    }
  });

  if(select){
    select.addEventListener("change", (e) => {
      const q = e.target.value;
      if(q){
        sendQuestion(q);
        select.value = "";
      }
    });
  }

  document.querySelectorAll(".qa-item").forEach(btn => {
    btn.addEventListener("click", () => {
      const q = btn.getAttribute("data-question");
      sendQuestion(q);
    });
  });
});