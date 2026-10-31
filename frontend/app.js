// This page only sends prediction requests. All training lives in the notebook.
const sections = ["fuel", "bank", "sentiment"];
const buttons = document.querySelectorAll("nav button");
buttons.forEach((button) => {
  button.addEventListener("click", () => {
    sections.forEach(
      (name) =>
        (document.getElementById(name).hidden = name !== button.dataset.tab),
    );
    buttons.forEach((item) => {
      const active = item === button;
      item.classList.toggle("active", active);
      item.setAttribute("aria-current", active ? "page" : "false");
    });
  });
});
function element(tag, text) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  return node;
}
function showPrediction(task, result) {
  const box = document.getElementById(task + "-result");
  box.className = "result";
  box.replaceChildren();
  const title =
    task === "fuel"
      ? result.predicted_mpg.toFixed(1) + " MPG"
      : result.predicted_class;
  box.append(element("h3", title), element("p", result.model));
  if (task !== "fuel") {
    const probability =
      task === "bank"
        ? result.probability_subscribes
        : result.probability_positive;
    const description =
      task === "bank"
        ? "Estimated subscription probability"
        : "Estimated positive-sentiment probability";
    box.append(
      element("p", description + ": " + (probability * 100).toFixed(1) + "%"),
    );
    const bar = element("div");
    bar.className = "probability";
    const fill = element("span");
    fill.style.width = probability * 100 + "%";
    bar.append(fill);
    box.append(bar);
    if (task === "bank")
      box.append(element("p", "Decision threshold: " + result.threshold));
  }
  box.append(element("p", result.note));
}
document.querySelectorAll("form").forEach((form) => {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const task = form.dataset.task;
    const button = form.querySelector("button");
    const originalText = button.textContent;
    const box = document.getElementById(task + "-result");
    const data = Object.fromEntries(new FormData(form));
    if (task !== "sentiment")
      Object.keys(data).forEach((key) => (data[key] = Number(data[key])));
    button.disabled = true;
    button.textContent = "Predicting…";
    box.className = "result";
    box.replaceChildren(element("p", "Waiting for the exported model…"));
    try {
      const response = await fetch("/api/predict/" + task, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      const result = await response.json();
      if (!response.ok)
        throw new Error(
          typeof result.detail === "string"
            ? result.detail
            : JSON.stringify(result.detail),
        );
      showPrediction(task, result);
    } catch (error) {
      box.className = "result error";
      box.replaceChildren(
        element("p", "Prediction unavailable: " + error.message),
      );
    } finally {
      button.disabled = false;
      button.textContent = originalText;
    }
  });
});
async function checkModels() {
  const status = document.getElementById("health");
  try {
    const response = await fetch("/api/status");
    if (!response.ok) throw new Error("Could not check models.");
    const result = await response.json();
    const missing = Object.entries(result.models)
      .filter(([, exists]) => !exists)
      .map(([name]) => name);
    status.textContent = missing.length
      ? "Missing exported models: " +
        missing.join(", ") +
        ". Run the notebook export cell."
      : "Three exported models are ready. Training stays in the notebook.";
  } catch (error) {
    status.textContent =
      "Start the FastAPI server and open the address it provides.";
  }
}
checkModels();
