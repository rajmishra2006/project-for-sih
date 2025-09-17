const API = "http://127.0.0.1:5000";

document.getElementById("uploadForm").onsubmit = async (e) => {
  e.preventDefault();
  let formData = new FormData(e.target);
  let res = await fetch(API + "/upload", {method:"POST", body:formData});
  let out = await res.json();
  document.getElementById("result").innerText = JSON.stringify(out,null,2);
};

async function loadLeaderboard(){
  let res = await fetch(API + "/leaderboard");
  let out = await res.json();
  document.getElementById("board").innerText = JSON.stringify(out,null,2);
}
