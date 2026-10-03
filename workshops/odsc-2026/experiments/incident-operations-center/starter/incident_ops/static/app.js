const list = document.querySelector("#incidents");
const feedback = document.querySelector("#feedback");
const form = document.querySelector("#create-form");

async function refresh() {
  const response = await fetch("/api/incidents");
  const incidents = await response.json();
  list.replaceChildren(...incidents.map(renderIncident));
}

function renderIncident(incident) {
  const article = document.createElement("article");
  article.innerHTML = `<strong>${incident.severity}</strong><h2></h2><p>${incident.status}</p>`;
  article.querySelector("h2").textContent = incident.title;
  return article;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = new FormData(form);
  const response = await fetch("/api/incidents", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(Object.fromEntries(data)),
  });
  feedback.textContent = response.ok ? "Incident created" : "Could not create incident";
  if (response.ok) {
    form.reset();
    await refresh();
  }
});

refresh();
