// ENTRY POINT
document.getElementById("analyzeBtn").addEventListener("click", runEvaluation);

async function runEvaluation() {

  // 1. Get files
  const tenderFile = document.getElementById("tenderFile").files[0];
  const bidderFile = document.getElementById("bidderFile").files[0];

  // 2. Validate input
  if (!tenderFile || !bidderFile) {
    alert("Please upload both Tender and Bidder documents.");
    return;
  }

  // 3. Show preview (we’ll improve later)
  showPreview(tenderFile, bidderFile);

  // 4. Show loading
  toggleLoading(true);

    try {

    // 5. Prepare form data
    const formData = new FormData();
    formData.append("tender", tenderFile);
    formData.append("bidder", bidderFile);

    // 6. API call
    const response = await fetch("http://127.0.0.1:8000/evaluate", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    console.log("API Response:", data);

    // 7. Render UI (next step)
    renderUI(data);

  } catch (error) {
    console.error("Error:", error);
    alert("Something went wrong while processing.");
  } finally {
    // 8. Hide loader
    toggleLoading(false);
  }

}

function showPreview(tenderFile, bidderFile) {

  const tenderPreview = document.getElementById("tenderPreview");
  const bidderPreview = document.getElementById("bidderPreview");

  // Create preview URLs
  const tenderURL = URL.createObjectURL(tenderFile);
  const bidderURL = URL.createObjectURL(bidderFile);

  // Set iframe sources
  tenderPreview.src = tenderURL;
  bidderPreview.src = bidderURL;

}

function renderUI(data) {

  // 1. Show hidden sections
  document.getElementById("resultHero").classList.remove("hidden");
  document.getElementById("insightsSection").classList.remove("hidden");
  document.getElementById("resultsSection").classList.remove("hidden");

  const result = data.result;

  // 2. FINAL STATUS
  const statusEl = document.getElementById("finalStatus");

  statusEl.innerText = result.final_status;

  statusEl.className = "status-text " +
    (result.final_status === "Eligible" ? "eligible" :
     result.final_status === "Not Eligible" ? "not-eligible" :
     "review");

  // 3. SUMMARY
  const summaryEl = document.getElementById("summaryBox");
  summaryEl.innerText = data.summary || "No summary available";

  // 4. CONFIDENCE SCORES
const confBox = document.getElementById("confidenceBox");
confBox.innerHTML = "";

Object.entries(data.confidence || {}).forEach(([key, val]) => {
  const percent = Math.round(val * 100);

  confBox.innerHTML += `
    <div class="confidence-item">
      <div class="confidence-label">${key} — ${percent}%</div>
      <div class="confidence-bar">
        <div class="confidence-fill" style="width:${percent}%"></div>
      </div>
    </div>
  `;
});


// 5. AUDIT TRAIL
const auditBox = document.getElementById("auditBox");
auditBox.innerHTML = "";

Object.entries(data.result.criteria_results || {}).forEach(([key, val]) => {
  auditBox.innerHTML += `
    <div class="audit-item">
      <strong>${key}</strong>: ${val.value || "-"} → ${val.status}
    </div>
  `;
});

// 6. DETAILED RESULTS
const resultsContainer = document.getElementById("resultsContainer");
resultsContainer.innerHTML = "";

Object.entries(data.result.criteria_results || {}).forEach(([key, val]) => {

  let badgeClass =
    val.status === "Eligible" ? "badge-eligible" :
    val.status === "Not Eligible" ? "badge-not" :
    "badge-review";

  resultsContainer.innerHTML += `
    <div class="result-card">

      <div class="result-title">
        ${key.toUpperCase()}
      </div>

      <div class="status-badge ${badgeClass}">
        ${val.status}
      </div>

      <div class="result-reason">
        ${val.reason || "No explanation"}
      </div>

    </div>
  `;
});

}

function toggleLoading(show) {
  const loader = document.getElementById("loader");

  if (!loader) {
    console.warn("Loader element not found");
    return;
  }

  if (show) {
    loader.classList.remove("hidden");
  } else {
    loader.classList.add("hidden");
  }
}