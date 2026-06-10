let activeConv = null;
let pollTimer = null;
let lastMsgId = 0;

async function renderMessages(params={}){
  app.innerHTML = `<h1>Messagerie</h1>
    <div class="chat-layout">
      <div class="conv-list" id="convs">Chargement...</div>
      <div class="chat-box">
        <div class="chat-header" id="chat-h">Sélectionnez une conversation</div>
        <div class="chat-messages" id="chat-m"></div>
        <form class="chat-input" id="chat-f" onsubmit="sendMsg(event)" style="display:none">
          <input id="chat-input" placeholder="Écrire un message..." autocomplete="off">
          <button class="btn" type="submit">Envoyer</button>
        </form>
      </div>
    </div>`;
  await loadConvs();
  if (params.open) openConv(params.open);
}

async function loadConvs(){
  const convs = await API.get("/api/conversations");
  const el = document.getElementById("convs");
  el.innerHTML = convs.length ? convs.map(c => `
    <div class="conv-item ${c.id===activeConv?'active':''}" onclick="openConv(${c.id})">
      <div class="avatar">${(c.other?.prenom||'?')[0]}</div>
      <div style="flex:1;min-width:0">
        <strong>${c.other?.prenom||''} ${c.other?.nom||''}</strong>
        <div class="muted" style="font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${c.last_message||'—'}</div>
      </div>
    </div>`).join("") : `<p class="muted" style="padding:10px">Aucune conversation. Contactez un mentor depuis l'onglet Matching ou Offres.</p>`;
}

async function openConv(id){
  activeConv = id; lastMsgId = 0;
  await loadConvs();
  document.getElementById("chat-f").style.display = "flex";
  document.getElementById("chat-m").innerHTML = "";
  await pollMessages();
  if (pollTimer) clearInterval(pollTimer);
  pollTimer = setInterval(pollMessages, 2500);
}

async function pollMessages(){
  if (!activeConv) return;
  try {
    const msgs = await API.get(`/api/conversations/${activeConv}/messages?after=${lastMsgId}`);
    if (!msgs.length) return;
    const box = document.getElementById("chat-m");
    msgs.forEach(m => {
      lastMsgId = Math.max(lastMsgId, m.id);
      const mine = m.sender_id === currentUser.id;
      const div = document.createElement("div");
      div.className = "msg " + (mine ? "me" : "them");
      div.innerHTML = `${escapeHtml(m.contenu)}<time>${new Date(m.created_at).toLocaleTimeString()}</time>`;
      box.appendChild(div);
    });
    box.scrollTop = box.scrollHeight;
    const header = document.getElementById("chat-h");
    if (header) header.textContent = "Conversation";
  } catch(e){ console.error(e); }
}

async function sendMsg(e){
  e.preventDefault();
  const input = document.getElementById("chat-input");
  const v = input.value.trim(); if (!v) return;
  input.value = "";
  try {
    await API.post(`/api/conversations/${activeConv}/messages`, { contenu: v });
    await pollMessages();
  } catch(err){ alert(err.message); }
}

function escapeHtml(s){return s.replace(/[&<>"']/g, c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
