const socket      = io();
const convId      = document.getElementById("conv-id").value;
const messagesDiv = document.getElementById("messages");
const input       = document.getElementById("message-input");
const userId      = parseInt(document.getElementById("user-id").value);

socket.emit("rejoindre", { conv_id: convId });

socket.on("nouveau_message", (data) => {
    afficherMessage(data);
    scrollBas();
});

const typingIndicator = document.getElementById("typing-indicator");
input.addEventListener("input", () => {
    socket.emit("en_train_d_ecrire", { conv_id: convId });
});
socket.on("utilisateur_ecrit", (data) => {
    typingIndicator.textContent = `${data.prenom} est en train d'écrire…`;
    clearTimeout(typingIndicator._timeout);
    typingIndicator._timeout = setTimeout(() => {
        typingIndicator.textContent = "";
    }, 2000);
});

document.getElementById("send-btn").addEventListener("click", envoyerMessage);
input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        envoyerMessage();
    }
});

function envoyerMessage() {
    const contenu = input.value.trim();
    if (!contenu) return;
    socket.emit("envoyer_message", { conv_id: convId, contenu });
    input.value = "";
}

function afficherMessage(data) {
    const estMoi = data.expediteur === userId;
    const div    = document.createElement("div");
    div.classList.add("message", estMoi ? "message-moi" : "message-autre");
    div.innerHTML = `
        ${!estMoi ? `<span class="message-auteur">${data.prenom} ${data.nom}</span>` : ""}
        <p class="message-contenu">${escapeHtml(data.contenu)}</p>
        <span class="message-heure">${data.date}</span>
    `;
    messagesDiv.appendChild(div);
}

function scrollBas() {
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function escapeHtml(text) {
    return text.replace(/&/g,"&amp;").replace(/</g,"&lt;")
               .replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}

window.addEventListener("load", scrollBas);
