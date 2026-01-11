const API_BASE = "http://127.0.0.1:8000";

async function ingest() {
  const text = document.getElementById("docInput").value;
  const status = document.getElementById("ingestStatus");

  status.textContent = "Ingesting...";

  const res = await fetch(`${API_BASE}/ingest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });

  const data = await res.json();
  status.textContent = `Ingested ${data.chunks_ingested} chunks`;
}

async function ask() {
  const question = document.getElementById("questionInput").value;

  const answerEl = document.getElementById("answer");
  const citationsEl = document.getElementById("citations");

  answerEl.textContent = "Thinking...";
  citationsEl.innerHTML = "";

  const res = await fetch(`${API_BASE}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
  });

  const data = await res.json();

  answerEl.textContent = data.answer;

  data.citations.forEach(cite => {
    const li = document.createElement("li");
    li.textContent = `[${cite.position}] ${cite.text}`;
    citationsEl.appendChild(li);
  });
}
