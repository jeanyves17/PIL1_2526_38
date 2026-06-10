async function renderOffres(){
  app.innerHTML = `
  <h1>Offres & demandes de mentorat</h1>
  <div class="card">
    <h3>Publier</h3>
    <div class="grid cols-2">
      <div><label>Type</label>
        <select id="o_type"><option value="offre">J'offre du mentorat</option><option value="demande">Je demande de l'aide</option></select></div>
      <div><label>Matière / compétence</label><input id="o_mat" placeholder="Ex: Python, SQL"></div>
      <div><label>Disponibilités</label><input id="o_dispo" placeholder="lundi-soir,..."></div>
      <div><label>Format</label>
        <select id="o_format"><option value="les_deux">Les deux</option><option value="presentiel">Présentiel</option><option value="en_ligne">En ligne</option></select></div>
    </div>
    <label>Description</label><textarea id="o_desc"></textarea>
    <div style="margin-top:10px"><button class="btn" onclick="postOffre()">Publier</button></div>
  </div>
  <div class="row" style="margin:10px 0">
    <input id="o_q" placeholder="Rechercher une matière..." style="flex:1">
    <select id="o_filter"><option value="">Tous</option><option value="offre">Offres</option><option value="demande">Demandes</option></select>
    <button class="btn secondary" onclick="loadOffres()">Filtrer</button>
  </div>
  <div id="o_list"></div>`;
  loadOffres();
}
async function postOffre(){
  try {
    await API.post("/api/offres", {
      type:o_type.value, matiere:o_mat.value, description:o_desc.value,
      disponibilites:o_dispo.value, format:o_format.value });
    o_mat.value=""; o_desc.value=""; loadOffres();
  } catch(e){ alert(e.message); }
}
async function loadOffres(){
  const q = new URLSearchParams();
  if (o_filter.value) q.set("type", o_filter.value);
  if (o_q.value) q.set("q", o_q.value);
  const list = await API.get("/api/offres?" + q);
  document.getElementById("o_list").innerHTML = list.length ? list.map(o => `
    <div class="card">
      <div class="row" style="justify-content:space-between">
        <div class="row">
          <div class="avatar">${(o.prenom||'?')[0]}</div>
          <div><strong>${o.prenom} ${o.nom}</strong><div class="muted">${o.filiere||''}</div></div>
        </div>
        <span class="tag">${o.type === 'offre' ? '🎓 Offre' : '🙋 Demande'}</span>
      </div>
      <h3 style="margin:10px 0 4px">${o.matiere}</h3>
      <p>${o.description||''}</p>
      <div class="muted">📅 ${o.disponibilites||'—'} · 📍 ${o.format}</div>
      ${o.user_id !== currentUser.id ? `<div style="margin-top:10px">
        <button class="btn sm" onclick="contact(${o.user_id})">💬 Contacter</button>
      </div>` : '<div class="muted" style="margin-top:6px">— Votre publication —</div>'}
    </div>`).join("") : `<p class="muted">Aucune publication.</p>`;
}
async function contact(userId){
  try {
    const r = await API.post("/api/conversations", { user_id: userId });
    go("messages", { open: r.conversation_id });
  } catch(e){ alert(e.message); }
}
