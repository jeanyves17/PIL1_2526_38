async function renderProfil(){
  const u = currentUser;
  app.innerHTML = `
  <h1>Mon profil</h1>
  <div class="card">
    <div id="msg"></div>
    <div class="grid cols-2">
      <div><label>Prénom</label><input id="p_prenom" value="${u.prenom||''}"></div>
      <div><label>Nom</label><input id="p_nom" value="${u.nom||''}"></div>
      <div><label>Filière</label>
        <select id="p_filiere">${["IA","IM","GL","SE&IoT","SI"].map(f=>`<option ${u.filiere===f?'selected':''}>${f}</option>`).join("")}</select></div>
      <div><label>Niveau</label>
        <select id="p_niveau">${["L1","L2","L3","M1","M2"].map(f=>`<option ${u.niveau===f?'selected':''}>${f}</option>`).join("")}</select></div>
    </div>
    <label>Photo (URL)</label><input id="p_photo" value="${u.photo_url||''}">
    <label>Bio</label><textarea id="p_bio">${u.bio||''}</textarea>
    <label>Compétences (séparées par virgule)</label><input id="p_comp" value="${u.competences||''}">
    <label>Lacunes</label><input id="p_lac" value="${u.lacunes||''}">
    <label>Disponibilités</label><input id="p_dispo" value="${u.disponibilites||''}">
    <div style="margin-top:14px"><button class="btn" onclick="saveProfil()">Enregistrer</button></div>
  </div>`;
}
async function saveProfil(){
  try {
    await API.put("/api/me", {
      prenom:p_prenom.value, nom:p_nom.value, filiere:p_filiere.value, niveau:p_niveau.value,
      photo_url:p_photo.value, bio:p_bio.value,
      competences:p_comp.value, lacunes:p_lac.value, disponibilites:p_dispo.value,
    });
    currentUser = await API.get("/api/me");
    document.getElementById("msg").innerHTML = `<div class="success">Profil mis à jour</div>`;
  } catch(e){ document.getElementById("msg").innerHTML = `<div class="error">${e.message}</div>`; }
}
