const Apiurl = ""
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
const filenamadis = document.getElementById("statusdis");

//theme toggler
themecheckbox.addEventListener("change", () => {
    if(themecheckbox.checked) {
        body.classList.add('darkmode');
    } else {
        body.classList.remove('darkmode');
    }
});

