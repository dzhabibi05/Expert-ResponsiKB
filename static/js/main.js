document.getElementById("yr").textContent = new Date().getFullYear();

const allChecks   = () => [...document.querySelectorAll(".g-check")];
const countNum    = document.getElementById("count-num");
const btnDiagnosa = document.getElementById("btn-diagnosa");
const btnClear    = document.getElementById("btn-clear");
const btnUlang    = document.getElementById("btn-ulang");
const searchInput = document.getElementById("search-input");

const idleState   = document.getElementById("idle-state");
const resultState = document.getElementById("result-state");
const noMatch     = document.getElementById("no-match");
const diagCards   = document.getElementById("diag-cards");
const recapWrap   = document.getElementById("recap-wrap");
const resultMeta  = document.getElementById("result-meta");

// Count
function refreshCount() {
  const n = allChecks().filter(c => c.checked).length;
  countNum.textContent = n;
}

document.querySelectorAll(".g-check").forEach(cb =>
  cb.addEventListener("change", refreshCount)
);

// Search
searchInput.addEventListener("input", () => {
  const q = searchInput.value.toLowerCase().trim();
  document.querySelectorAll(".gejala-item").forEach(item => {
    const match = !q || item.dataset.search.includes(q);
    item.classList.toggle("hide", !match);
  });
  document.querySelectorAll(".gejala-group").forEach(grp => {
    const visible = [...grp.querySelectorAll(".gejala-item")].some(i => !i.classList.contains("hide"));
    grp.style.display = visible ? "" : "none";
  });
});

// Clear
function clearAll() {
  allChecks().forEach(c => c.checked = false);
  refreshCount();
  showIdle();
}

btnClear.addEventListener("click", clearAll);
btnUlang.addEventListener("click", clearAll);

function showIdle() {
  resultState.classList.add("hidden");
  idleState.classList.remove("hidden");
}

// Shake animation
const shakeStyle = document.createElement("style");
shakeStyle.textContent = `@keyframes shake{0%,100%{transform:translateX(0)}20%{transform:translateX(-6px)}40%{transform:translateX(6px)}60%{transform:translateX(-4px)}80%{transform:translateX(4px)}}`;
document.head.appendChild(shakeStyle);

function shake(el) {
  el.style.animation = "";
  void el.offsetWidth;
  el.style.animation = "shake 0.4s ease";
  setTimeout(() => el.style.animation = "", 450);
}

// Diagnosa
btnDiagnosa.addEventListener("click", async () => {
  const selected = allChecks().filter(c => c.checked).map(c => c.value);
  if (!selected.length) { shake(btnDiagnosa); return; }

  btnDiagnosa.classList.add("busy");
  btnDiagnosa.querySelector(".btn-text").textContent = "Menganalisis...";

  try {
    const res  = await fetch("/diagnosa", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ gejala: selected }),
    });
    const data = await res.json();
    renderResult(data);
  } catch {
    alert("Gagal menghubungi server. Pastikan Flask berjalan.");
  } finally {
    btnDiagnosa.classList.remove("busy");
    btnDiagnosa.querySelector(".btn-text").textContent = "Diagnosa";
  }
});

// Render
function renderResult(data) {
  idleState.classList.add("hidden");
  resultState.classList.remove("hidden");
  noMatch.classList.add("hidden");
  diagCards.innerHTML = "";
  recapWrap.innerHTML = "";

  resultMeta.textContent =
    `${data.total_gejala} gejala dipilih · ${data.ditemukan} diagnosis cocok`;

  // Recap chips
  Object.values(data.gejala_labels).forEach(lbl => {
    const chip = document.createElement("div");
    chip.className = "recap-chip";
    chip.title = lbl;
    chip.textContent = lbl;
    recapWrap.appendChild(chip);
  });

  if (!data.ditemukan) {
    noMatch.classList.remove("hidden");
    return;
  }

  data.hasil.forEach((item, i) => {
    const card = buildCard(item, i === 0);
    diagCards.appendChild(card);
    if (i === 0) setTimeout(() => card.querySelector(".d-body").classList.add("open"), 350);
  });
}


function buildCard(item, isTop) {
  const card = document.createElement("div");
  card.className = `d-card${isTop ? " top-card" : ""}`;

  const cfColor = item.confidence >= 70 ? item.warna
                : item.confidence >= 40 ? "#d35400" : "#a08060";

  const bahayaStyle =
    item.tingkat_bahaya === "Sangat Tinggi" ? "background:#dc262618;color:#dc2626;"
  : item.tingkat_bahaya === "Tinggi"        ? "background:#ea580c18;color:#ea580c;"
  : "background:#ca8a0418;color:#ca8a04;";

  const jenisColor =
    item.jenis === "Jamur"   ? "background:#8b5cf618;color:#7c3aed;" 
  : item.jenis === "Bakteri" ? "background:#2563eb18;color:#1d4ed8;"
  : item.jenis === "Virus"   ? "background:#dc262618;color:#dc2626;"
  : "background:#0891b218;color:#0369a1;";

  const gejalaItems  = item.gejala_utama.map(g => `<li>${g}</li>`).join("");
  const penanganItems = item.penanganan.map(p => `<li>${p}</li>`).join("");
  const matchTags    = item.gejala_kuat_cocok.map(g =>
    `<span class="match-tag" style="background:${item.warna}15;color:${item.warna};border-color:${item.warna}40">${g}</span>`
  ).join("");

  card.innerHTML = `
    <div class="d-head" onclick="toggleCard(this)">
      <div class="d-emoji">${item.emoji}</div>
      <div class="d-info">
        <div class="d-nama">${item.nama}</div>
        <div class="d-meta">
          <span class="d-jenis" style="${jenisColor}">${item.jenis}</span>
          <span class="d-bahaya" style="${bahayaStyle}">● ${item.tingkat_bahaya}</span>
        </div>
      </div>
      <div class="d-cf">
        <div class="cf-num" style="color:${cfColor}">${item.confidence}%</div>
        <div class="cf-lbl">KEYAKINAN</div>
        <div class="cf-track">
          <div class="cf-fill" style="width:${item.confidence}%;background:${cfColor}"></div>
        </div>
      </div>
    </div>
    <div class="d-body">
      <div class="d-divider"></div>
      <div class="d-desc">${item.deskripsi}</div>
      <div class="d-section">Patogen</div>
      <p style="font-size:12.5px;color:var(--text2);font-style:italic">${item.patogen}</p>
      <div class="d-section">Gejala Utama Penyakit</div>
      <ul class="d-list">${gejalaItems}</ul>
      <div class="d-section">Langkah Penanganan</div>
      <ul class="d-list">${penanganItems}</ul>
      <div class="pencegahan-box">${item.pencegahan}</div>
      ${matchTags ? `
      <div class="d-section">Gejala Kuat yang Cocok</div>
      <div class="match-tags">${matchTags}</div>` : ""}
    </div>
  `;

  return card;
}

function toggleCard(header) {
  header.nextElementSibling.classList.toggle("open");
}
