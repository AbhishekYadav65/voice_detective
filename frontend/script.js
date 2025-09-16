let uploadedTranscripts = []; // store transcripts for analysis

// Upload & Transcribe
document.getElementById("uploadBtn").addEventListener("click", async () => {
  const fileInput = document.getElementById("fileInput");
  if (!fileInput.files.length) {
    alert("⚠️ Please select at least one audio file.");
    return;
  }

  const formData = new FormData();
  for (let i = 0; i < fileInput.files.length; i++) {
    formData.append("files", fileInput.files[i]); // backend expects "files"
  }

  try {
    const status = document.getElementById("status");
    status.textContent = "⏳ Uploading & transcribing...";
    status.style.color = "yellow";

    const response = await fetch("http://127.0.0.1:8000/upload-audio", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error(`Upload failed (${response.status})`);

    const data = await response.json();
    console.log("Response:", data);

    status.textContent = "✅ Upload complete!";
    status.style.color = "lightgreen";

    uploadedTranscripts = data.transcripts;

    // Show transcripts
    let transcriptBox = document.getElementById("transcript");
    transcriptBox.textContent = "";
    uploadedTranscripts.forEach(t => {
      transcriptBox.textContent += `🎵 ${t.filename}:\n${t.transcript}\n\n`;
    });

    document.getElementById("transcriptCard").style.display = "block";

  } catch (err) {
    console.error(err);
    document.getElementById("status").textContent = "❌ Failed to upload & transcribe";
    document.getElementById("status").style.color = "red";
  }
});

// Analyze transcripts
document.getElementById("analyzeBtn").addEventListener("click", async () => {
  if (!uploadedTranscripts.length) {
    alert("⚠️ No transcripts available to analyze.");
    return;
  }

  const analyzeStatus = document.getElementById("analyzeStatus");
  analyzeStatus.textContent = "⏳ Analyzing transcripts...";
  analyzeStatus.style.color = "yellow";

  try {
    const response = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ transcripts: uploadedTranscripts }),
    });

    if (!response.ok) throw new Error(`Analysis failed (${response.status})`);

    const data = await response.json();
    console.log("Analysis:", data);

    analyzeStatus.textContent = "✅ Analysis complete!";
    analyzeStatus.style.color = "lightgreen";

    const report = document.getElementById("report");
    report.innerHTML = ""; // clear old content

    // ✅ Handle `analysis` array returned from backend
    if (data.analysis && Array.isArray(data.analysis)) {
      data.analysis.forEach(item => {
        const scorePercent = Math.round((item.truth_score || 0) * 100);

        // 🟢 Quick summary card
        const summary = document.createElement("div");
        summary.className = "summary-card";

        let scoreClass = "score-low";
        if (scorePercent >= 75) scoreClass = "score-high";
        else if (scorePercent >= 50) scoreClass = "score-medium";
        summary.classList.add(scoreClass);

        summary.innerHTML = `
          <p>🕵️ <b>${item.shadow_id}</b></p>
          <p>Truth Score: <b>${scorePercent}%</b></p>
          <p>Experience: <i>${item.revealed_truth?.programming_experience || "unknown"}</i></p>
        `;
        report.appendChild(summary);

        // 📂 Collapsible JSON
        const block = document.createElement("details");
        block.open = false;
        block.innerHTML = `
          <summary>📂 Raw JSON Analysis</summary>
          <div class="truth-score-bar" data-score="${scorePercent}"></div>
          <pre>${JSON.stringify(item, null, 2)}</pre>
        `;
        report.appendChild(block);

        // ✅ Animate truth score bar with gradient
        const bar = block.querySelector(".truth-score-bar");
        if (scorePercent < 50) {
          bar.style.background = "linear-gradient(to right, #e53935, #ff7043)";
        } else if (scorePercent < 75) {
          bar.style.background = "linear-gradient(to right, #ff9800, #fdd835)";
        } else {
          bar.style.background = "linear-gradient(to right, #4caf50, #81c784)";
        }

        requestAnimationFrame(() => {
          bar.style.width = scorePercent + "%";
        });
      });
    } else {
      // fallback
      report.textContent = JSON.stringify(data, null, 2);
    }

    document.getElementById("reportCard").style.display = "block";
  } catch (err) {
    console.error(err);
    analyzeStatus.textContent = "❌ Analysis failed";
    analyzeStatus.style.color = "red";
  }
});
