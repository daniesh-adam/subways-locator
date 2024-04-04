function getResponse() {
  const userPrompt = document.getElementById("user-prompt-input").value;

  document.getElementById("user-prompt-btn").classList.add("disabled");
  document.getElementById("prompt-response-spinner").classList.remove("d-none");

  document.getElementById("user-prompt").innerText = `${userPrompt}`;
  document.getElementById("prompt-response").innerHTML = " ";
}
