const Apiurl = "https://ambitiouspotato-ragger.hf.space";
const themecheckbox = document.getElementById("checkbox");
let currentdocid = null;
let selfile = null;
const body = document.body;
const dropzone = document.getElementById("dropzone");
const file = document.getElementById("file");
const filedet = document.getElementById("filedet");
const filenama = document.getElementById("filename");
const actbtn = document.getElementById("actbtn");
const btntxt = document.getElementById("btntxt");
const btnhid = document.getElementById("btnhid");
const statusdis = document.getElementById("statusdis");






//theme toggler
themecheckbox.addEventListener("change", () => {
    if(themecheckbox.checked) {
        body.classList.add('darkmode');
    } else {
        body.classList.remove('darkmode');
    }
});






const activedocindi = document.getElementById("activedocindi");
const activedocname = document.getElementById("activedocname");
const question = document.getElementById("question");
const sendbtn = document.getElementById("sendbtn");
const chathistory = document.getElementById("chathistory");
const welcomestat = document.getElementById("welcomestat");







dropzone.addEventListener('click', () => file.click());
file.addEventListener('change', (e) => {
    if(e.target.files.length > 0) {
        selfile = e.target.files[0];
        filenama.innerText = selfile.name;
        filedet.classList.remove("hidden");
        actbtn.classList.remove("actionbtnin");
        actbtn.classList.add("actionbtnac");
        statusdis.classList.remove("statusdis");
        statusdis.classList.add("statusdishid");
    }
});






actbtn.addEventListener("click", async () => {
    if(!selfile || actbtn.classList.contains('actionbtnin')) return;
    btntxt.innerText = "loading";
    btnhid.classList.remove("loaderhid");
    btnhid.classList.add("loaderactive");
    statusdis.classList.remove("statusdishid");
    statusdis.classList.add("statusdis");
    statusdis.innerText = "uploading and embedding pdf";
    statusdis.style.color = "#a0a0a0";
    const formdata = new FormData();
    formdata.append("file", selfile);
    try {
        const responce = await fetch(`${Apiurl}/upload`, {
            method: "POST",
            body: formdata
        });
        if(responce.ok){
            const data = await responce.json();
            currentdocid = data.document_id;
            statusdis.innerText = "knowledge base is Ready!!!";
            statusdis.style.color = "#09AB3B";
            activedocindi.classList.remove("hidden");
            activedocname.innerText = currentdocid;
            welcomestat.classList.add("hidden");
            question.disabled = false;
            sendbtn.disabled = false;
            question.focus();
        }
        else {
            statusdis.innerText = "something went wrong upload failed";
            statusdis.style.color = "#020202";
        }
    }catch (error) {
        statusdis.innerText = "server offline try again later";
        statusdis.style.color = "#ff4b4b";
    } finally {
        btntxt.innerText = "Build Knowledge database";
        btnhid.classList.remove("loaderactive");
        btnhid.classList.add("loaderhid");
    }
});





sendbtn.addEventListener('click', sendmessage);
question.addEventListener('keydown', (e) => {
    if(e.key === "Enter") {
        sendmessage();
    }
});
async function sendmessage() {
    const text = question.value.trim();
    if(!text || !currentdocid) return;
    appendmessage("user", text);
    question.value ='';
    const loadingid = appendmessage("AI", "thinking");
    const formdata = new FormData();
    formdata.append("documentid", currentdocid);
    formdata.append("question", text);
    try {
        const responce = await fetch(`${Apiurl}/chat`, {
            method: "POST",
            body: formdata
        });
        if(responce.ok){
            const data = await responce.json();
            updatemessage(loadingid, data.answer);
        }
        else {
            updatemessage(loadingid,"eror processing request.");
        }
    }catch (error) {
        updatemessage(loadingid, "connection to backend lost");
    }
}

function appendmessage(role,text){
    const id = 'msg-' + Date.now();
    const msgdiv = document.createElement('div');
    msgdiv.id = id;
    msgdiv.style.borderRadius = "15px";
    msgdiv.style.marginBottom = "1rem";
    msgdiv.style.maxWidth = "85%";
    msgdiv.style.lineHeight = "1.5";

    if(role === "user"){
        msgdiv.style.backgroundColor = "var(--chatuserbg, rgba(0,242,254,0.1))";
        msgdiv.style.alignSelf = "flexend";
        msgdiv.style.borderBottomLeftRadius = "5px";
        msgdiv.style.border = "1px solid var(--glassborder)";
    }else {
        msgdiv.style.backgroundColor = "rgba(255, 255, 255, 0.05)";
        msgdiv.style.alignSelf = "flex-start";
        msgdiv.style.borderBottomLeftRadius = "5px";
        msgdiv.style.border = "1px solid rgba(255, 255, 255, 0.08)";
    }
    msgdiv.innerText = text;
    chathistory.appendChild(msgdiv);
    chathistory.scrollTop = chathistory.scrollHeight;
    return id;
}


function updatemessage(id, text){
    const msgdiv = document.getElementById(id);
    if(msgdiv){
        msgdiv.innerText = text;
        chathistory.scrollTop = chathistory.scrollHeight;
    }
}


        
