const app = document.getElementById("app");
const topbar = document.getElementById("topbar");
let currentUser = null;

const routes = {
  login: renderAuth,
  dashboard: renderDashboard,
  profil: renderProfil,
  offres: renderOffres,
  match: renderMatch,
  messages: renderMessages,
};

async function go(name, params={}) {
  if (name !== "login" && !API.token()) { name = "login"; }
  topbar.classList.toggle("hidden", name === "login");
  if (name !== "login" && !currentUser) {
    try { currentUser = await API.get("/api/me"); }
    catch { API.clear(); return go("login"); }
  }
  app.innerHTML = "";
  await routes[name](params);
}
function logout(){ API.post("/api/logout").catch(()=>{}); API.clear(); currentUser=null; go("login"); }

function renderDashboard(){
  app.innerHTML = `
    <h1>Bienvenue, ${currentUser.prenom} 👋</h1>
    <p class="muted">Trouvez un mentor ou aidez un pair via IFRI MentorLink.</p>
    <div class="grid cols-3">
      <div class="card"><h3>🎯 Matching</h3><p class="muted">Découvrez les profils compatibles avec vos compétences et disponibilités.</p>
        <button class="btn" onclick="go('match')">Voir mes matchs</button></div>
      <div class="card"><h3>📋 Offres & demandes</h3><p class="muted">Publiez une offre de mentorat ou cherchez de l'aide.</p>
        <button class="btn" onclick="go('offres')">Parcourir</button></div>
      <div class="card"><h3>💬 Messagerie</h3><p class="muted">Échangez avec vos mentors et mentorés.</p>
        <button class="btn" onclick="go('messages')">Ouvrir</button></div>
    </div>`;
}

document.addEventListener("DOMContentLoaded", ()=> go(API.token() ? "dashboard" : "login"));
