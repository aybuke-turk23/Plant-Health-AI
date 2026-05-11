(function () {
  // --- DOM REFERENCES --------------------------------------------------------
  const dropzone     = document.getElementById("dropzone");
  const fileInput    = document.getElementById("file-input");
  const previewRow   = document.getElementById("preview-row");
  const previewImg   = document.getElementById("preview-img");
  const clearBtn     = document.getElementById("clear-btn");
  const analyzeBtn   = document.getElementById("analyze-btn");
  const btnLabel     = document.getElementById("btn-label");
  const spinner      = document.getElementById("spinner");
  const resultEl     = document.getElementById("result");
  const errorEl      = document.getElementById("error");
  const ringFill     = document.getElementById("ring-fill");
  const scoreValue   = document.getElementById("score-value");
  const summaryEl    = document.getElementById("summary");
  const issuesList   = document.getElementById("issues-list");
  const recsList     = document.getElementById("recs-list");

  // AI assistant panel elements
  const assistantPanel = document.getElementById("ai-assistant-panel");
  const chatMessages   = document.getElementById("chat-messages");
  const aiTextArea     = document.getElementById("ai-text-area");
  const chatInputRow   = document.getElementById("chat-input-row");
  const chatInput      = document.getElementById("chat-input");
  const chatSendBtn    = document.getElementById("chat-send-btn");

  // --- CONSTANTS -------------------------------------------------------------
  const RING_LEN       = 2 * Math.PI * 52;
  const DEV_API_ORIGIN = "http://127.0.0.1:5000";

  // --- CHAT STATE ------------------------------------------------------------
  let chatContext = "";  // Disease/status context from the last analysis
  let chatHistory = [];  // [{ role: "user"|"model", content: "..." }, ...]

  // --- URL HELPERS -----------------------------------------------------------
  function getAnalyzeUrl() {
    return window.location.protocol === "file:"
      ? DEV_API_ORIGIN + "/api/analyze"
      : window.location.origin + "/api/analyze";
  }

  function getChatUrl() {
    return window.location.protocol === "file:"
      ? DEV_API_ORIGIN + "/api/chat"
      : window.location.origin + "/api/chat";
  }

  // --- PANEL TOGGLE (called from HTML) ---------------------------------------
  window.toggleAssistant = function () {
    assistantPanel && assistantPanel.classList.toggle("open");
  };

  // --- HELPERS ---------------------------------------------------------------
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
    const list = Array.isArray(items) ? items : items ? [items] : [];
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
    previewImg.src = URL.createObjectURL(file);
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
    assistantPanel.classList.remove("open");
    chatInputRow.style.display = "none";
    chatHistory = [];
    chatContext = "";
    hideError();
  }

  // --- CHAT FUNCTIONS --------------------------------------------------------
  function appendMessage(role, text) {
    // Remove the initial placeholder bubble on first real message
    if (aiTextArea && chatMessages.contains(aiTextArea)) {
      chatMessages.removeChild(aiTextArea);
    }

    const div = document.createElement("div");
    div.className =
      role === "user" ? "chat-bubble user-bubble" : "chat-bubble ai-bubble";
    div.textContent = text;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  async function sendChatMessage() {
    const msg = chatInput.value.trim();
    if (!msg) return;

    chatInput.value = "";
    chatSendBtn.disabled = true;
    appendMessage("user", msg);

    // Show typing indicator
    const typing = document.createElement("div");
    typing.className = "chat-bubble ai-bubble typing";
    typing.textContent = "...";
    chatMessages.appendChild(typing);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
      const res = await fetch(getChatUrl(), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: msg,
          context: chatContext,
          history: chatHistory,
        }),
      });

      const data = await res.json().catch(() => ({}));
      typing.remove();

      const reply = data.reply || data.error || "Something went wrong. Please try again.";
      appendMessage("model", reply);

      // Update conversation history
      chatHistory.push({ role: "user",  content: msg });
      chatHistory.push({ role: "model", content: reply });

    } catch (err) {
      typing.remove();
      appendMessage("model", "Could not reach the server. Make sure your backend is running.");
      console.error(err);
    } finally {
      chatSendBtn.disabled = false;
      chatInput.focus();
    }
  }

  // --- EVENT LISTENERS -------------------------------------------------------
  dropzone.addEventListener("click", () => fileInput.click());

  fileInput.addEventListener("change", function () {
    const f = fileInput.files && fileInput.files[0];
    if (f) applyFile(f);
  });

  clearBtn.addEventListener("click", clearFile);

  chatSendBtn.addEventListener("click", sendChatMessage);

  chatInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendChatMessage();
    }
  });

  // Drag & drop support
  ["dragenter", "dragover"].forEach((ev) => {
    dropzone.addEventListener(ev, (e) => {
      e.preventDefault();
      dropzone.classList.add("dragover");
    });
  });
  ["dragleave", "drop"].forEach((ev) => {
    dropzone.addEventListener(ev, (e) => {
      e.preventDefault();
      dropzone.classList.remove("dragover");
    });
  });
  dropzone.addEventListener("drop", (e) => {
    const f = e.dataTransfer?.files?.[0];
    if (f) applyFile(f);
  });

  // --- MAIN ANALYSIS LOGIC ---------------------------------------------------
  analyzeBtn.addEventListener("click", async function () {
    if (!selectedFile) return;

    hideError();
    setLoading(true);
    resultEl.classList.add("hidden");

    // Reset chat state for new analysis
    chatHistory = [];
    chatContext = "";
    chatInputRow.style.display = "none";
    if (chatMessages) {
      chatMessages.innerHTML = "";
      if (aiTextArea) {
        aiTextArea.innerText = "Analyzing your plant, preparing personalized recommendations...";
        chatMessages.appendChild(aiTextArea);
      }
    }

    const form = new FormData();
    form.append("file", selectedFile);

    try {
      const res = await fetch(getAnalyzeUrl(), {
        method: "POST",
        body: form,
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        showError(data.error || data.detail || "Analysis failed.");
        return;
      }

      // Render score and summary
      setScore(data.health_percentage ?? data.accuracy ?? 0);
      summaryEl.textContent =
        data.summary ||
        (data.status === "sick"
          ? `${data.disease} detected.`
          : "Your plant looks healthy!");

      // Render findings and recommendations
      renderLists(issuesList, data.issues    || [data.disease] || ["—"]);
      renderLists(recsList,   data.recommendations || ["Ask the AI Assistant for details."]);

      // Build chatbot context from analysis result
      const disease  = data.disease  || "Unknown";
      const status   = data.status   || "unknown";
      const accuracy = data.health_percentage ?? data.accuracy ?? 0;
      const treatment = data.treatment || (data.recommendations && data.recommendations[0]) || "";

      chatContext = `Plant status: ${status}, Disease/Type: ${disease}, Health score: ${accuracy}%`;

      // Show AI recommendation in the assistant panel
      if (treatment && aiTextArea) {
        aiTextArea.innerText = treatment;
      }

      // Open assistant panel and show chat input
      assistantPanel.classList.add("open");
      chatInputRow.style.display = "flex";

      resultEl.classList.remove("hidden");

    } catch (err) {
      showError(
        "Could not reach the server. Make sure your Python backend is running on port 5000."
      );
      console.error(err);
    } finally {
      setLoading(false);
    }
  });
})();