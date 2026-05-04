(function () {
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("file-input");
  const previewRow = document.getElementById("preview-row");
  const previewImg = document.getElementById("preview-img");
  const clearBtn = document.getElementById("clear-btn");
  const analyzeBtn = document.getElementById("analyze-btn");
  const btnLabel = document.getElementById("btn-label");
  const spinner = document.getElementById("spinner");
  const resultEl = document.getElementById("result");
  const errorEl = document.getElementById("error");
  const ringFill = document.getElementById("ring-fill");
  const scoreValue = document.getElementById("score-value");
  const summaryEl = document.getElementById("summary");
  const issuesList = document.getElementById("issues-list");
  const recsList = document.getElementById("recs-list");

  const RING_LEN = 2 * Math.PI * 52;

  /** If opened via file://, match this with your local API port (e.g. uvicorn port) */
  var DEV_API_ORIGIN = "http://127.0.0.1:5000";

  function getAnalyzeUrl() {
    if (window.location.protocol === "file:") {
      return DEV_API_ORIGIN + "/api/analyze";
    }
    return window.location.origin + "/api/analyze";
  }

  /** @type {File | null} */
  let selectedFile = null;

  function showError(message) {
    errorEl.textContent = message;
    errorEl.classList.remove("hidden");
  }

  function hideError() {
    errorEl.classList.add("hidden");
    errorEl.textContent = "";
  }

  function setLoading(loading) {
    analyzeBtn.disabled = loading || !selectedFile;
    btnLabel.classList.toggle("hidden", loading);
    spinner.classList.toggle("hidden", !loading);
  }

  function setScore(percent) {
    const p = Math.max(0, Math.min(100, Number(percent) || 0));
    scoreValue.textContent = String(Math.round(p));
    const offset = RING_LEN - (RING_LEN * p) / 100;
    ringFill.style.strokeDashoffset = String(offset);
    ringFill.style.stroke =
      p >= 70 ? "#3ecf8e" : p >= 40 ? "#fbbf24" : "#f87171";
  }

  function renderLists(ul, items) {
    ul.innerHTML = "";
    const list = Array.isArray(items) ? items : [];
    list.forEach(function (text) {
      const li = document.createElement("li");
      li.textContent = String(text);
      ul.appendChild(li);
    });
  }

  function applyFile(file) {
    if (!file || !file.type.startsWith("image/")) {
      showError("Please select a valid image.");
      return;
    }
    selectedFile = file;
    hideError();
    resultEl.classList.add("hidden");
    const url = URL.createObjectURL(file);
    previewImg.src = url;
    previewRow.classList.remove("hidden");
    analyzeBtn.disabled = false;
  }

  function clearFile() {
    selectedFile = null;
    if (previewImg.src) URL.revokeObjectURL(previewImg.src);
    previewImg.src = "";
    previewRow.classList.add("hidden");
    fileInput.value = "";
    analyzeBtn.disabled = true;
    resultEl.classList.add("hidden");
    hideError();
  }

  dropzone.addEventListener("click", function () {
    fileInput.click();
  });

  dropzone.addEventListener("keydown", function (e) {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      fileInput.click();
    }
  });

  fileInput.addEventListener("change", function () {
    const f = fileInput.files && fileInput.files[0];
    if (f) applyFile(f);
  });

  ["dragenter", "dragover"].forEach(function (ev) {
    dropzone.addEventListener(ev, function (e) {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.add("dragover");
    });
  });

  ["dragleave", "drop"].forEach(function (ev) {
    dropzone.addEventListener(ev, function (e) {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.remove("dragover");
    });
  });

  dropzone.addEventListener("drop", function (e) {
    const f = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
    if (f) applyFile(f);
  });

  clearBtn.addEventListener("click", clearFile);

  analyzeBtn.addEventListener("click", async function () {
    if (!selectedFile) return;
    hideError();
    setLoading(true);
    resultEl.classList.add("hidden");

    const form = new FormData();
    form.append("file", selectedFile);

    try {
      const res = await fetch(getAnalyzeUrl(), {
        method: "POST",
        body: form,
      });
      const data = await res.json().catch(function () {
        return {};
      });
      if (!res.ok) {
        const detail = data.detail;
        showError(
          typeof detail === "string"
            ? detail
            : Array.isArray(detail)
              ? detail.map(function (d) { return d.msg || d; }).join(" ")
              : "Analysis failed."
        );
        return;
      }
      setScore(data.health_percentage);
      summaryEl.textContent = data.summary || "";
      renderLists(issuesList, data.issues);
      renderLists(recsList, data.recommendations);
      resultEl.classList.remove("hidden");
    } catch (err) {
      var lines = [
        "Could not reach the server; the request did not complete (network / CORS / server offline).",
        "",
      ];
      if (window.location.protocol === "file:") {
        lines.push(
          "If you opened the page as a file (double-click): you must run the Python server and access the site via browser URL."
        );
        lines.push("");
      }
      lines.push("1) Activate your virtual environment in the project folder, then run:");
      lines.push("   uvicorn main:app --reload --host 127.0.0.1 --port 8080");
      lines.push("2) Open in browser: http://127.0.0.1:8080");
      lines.push("(Port 8000 may be blocked on Windows; try 8080. If using another port, update DEV_API_ORIGIN in app.js.)");
      if (err && err.message) {
        lines.push("");
        lines.push("Browser: " + err.message);
      }
      showError(lines.join("\n"));
    } finally {
      setLoading(false);
    }
  });
})();