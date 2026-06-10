function renderAuth(){
  app.innerHTML = `
  <div class="auth-wrap">
    <h1 style="text-align:center">IFRI MentorLink</h1>
    <p class="muted" style="text-align:center;margin-bottom:20px">Connectez-vous pour trouver mentors et mentorés.</p>
    <div class="card">
      <div class="tabs">
        <button id="tab-login" class="active" onclick="switchTab('login')">Connexion</button>
        <button id="tab-reg" onclick="switchTab('reg')">Inscription</button>
      </div>
      <div id="auth-form"></div>
    </div>
  </div>`;
  switchTab("login");
}

function switchTab(t){
  document.getElementById("tab-login").classList.toggle("active", t==="login");
  document.getElementById("tab-reg").classList.toggle("active", t==="reg");
  const f = document.getElementById("auth-form");
  if (t==="login") {
    f.innerHTML = `
      <div id="err"></div>
      <label>Email ou téléphone</label><input id="ident">
      <label>Mot de passe</label><input id="pw" type="password">
      <div style="margin-top:14px"><button class="btn" onclick="doLogin()">Se connecter</button></div>`;
  } else {
    f.innerHTML = `
      <div id="err"></div>
      <div class="grid cols-2">
        <div><label>Prénom</label><input id="prenom"></div>
        <div><label>Nom</label><input id="nom"></div>
      </div>
      <label>Email</label><input id="email" type="email">
      <label>Téléphone</label><input id="tel">
      <div class="grid cols-2">
        <div><label>Filière</label>
          <select id="filiere"><option>IA</option><option>IM</option><option>GL</option><option>SE&IoT</option><option>SI</option></select></div>
        <div><label>Niveau</label>
          <select id="niveau"><option>L1</option><option>L2</option><option>L3</option><option>M1</option><option>M2</option></select></div>
      </div>
      <label>Compétences (séparées par virgule)</label><input id="comp" placeholder="Python, Algèbre, Web...">
      <label>Lacunes / matières où j'ai besoin d'aide</label><input id="lac" placeholder="SQL, Réseaux...">
      <label>Disponibilités (ex: lundi-soir,mercredi-matin)</label><input id="dispo">
      <label>Mot de passe</label><input id="pw" type="password">
      <div style="margin-top:14px"><button class="btn" onclick="doRegister()">Créer mon compte</button></div>`;
  }
}

async function doLogin(){
  const err = document.getElementById("err");
  try {
    const r = await API.post("/api/login", {
      identifiant: document.getElementById("ident").value,
      password: document.getElementById("pw").value,
    });
    API.setToken(r.token); currentUser = null; go("dashboard");
  } catch (e) { err.innerHTML = `<div class="error">${e.message}</div>`; }
}

async function doRegister(){
  const err = document.getElementById("err");
  try {
    const r = await API.post("/api/register", {
      prenom: prenom.value, nom: nom.value, email: email.value, telephone: tel.value,
      password: pw.value, filiere: filiere.value, niveau: niveau.value,
      competences: comp.value, lacunes: lac.value, disponibilites: dispo.value,
    });
    API.setToken(r.token); currentUser=null; go("dashboard");
  } catch (e) { err.innerHTML = `<div class="error">${e.message}</div>`; }
}
