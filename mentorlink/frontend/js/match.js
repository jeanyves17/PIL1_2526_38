async function renderMatch(){
  app.innerHTML = `<h1>Matching intelligent</h1>
    <p class="muted">Basé sur vos compétences, lacunes, disponibilités et filière.</p>
    <div id="m_list">Chargement...</div>`;
  try {
    const list = await API.get("/api/match");
    if (!list.length) {
      document.getElementById("m_list").innerHTML =
        `<div class="card"><p class="muted">Aucun match trouvé. Complétez votre profil (compétences, lacunes, disponibilités).</p>
          <button class="btn" onclick="go('profil')">Compléter mon profil</button></div>`;
      return;
    }
    document.getElementById("m_list").innerHTML = `<div class="grid cols-2">${
      list.map(m => `
      <div class="card match-card">
        <span class="score">Score ${m.score}</span>
        <div class="row">
          <div class="avatar">${(m.prenom||'?')[0]}</div>
          <div><strong>${m.prenom} ${m.nom}</strong>
            <div class="muted">${m.filiere||''} · ${m.niveau||''}</div></div>
        </div>
        <p class="muted" style="margin:10px 0 4px">Rôle proposé : <strong>${m.role_propose}</strong></p>
        <div>${(m.matieres_communes||[]).map(t=>`<span class="tag">${t}</span>`).join("")||'<span class="muted">—</span>'}</div>
        <div class="muted" style="margin-top:8px">📅 Communes : ${(m.disponibilites_communes||[]).join(", ")||"—"}</div>
        <div style="margin-top:12px">
          <button class="btn sm" onclick="contact(${m.id})">💬 Contacter</button>
        </div>
      </div>`).join("")}</div>`;
  } catch(e){ document.getElementById("m_list").innerHTML = `<div class="error">${e.message}</div>`; }
}
