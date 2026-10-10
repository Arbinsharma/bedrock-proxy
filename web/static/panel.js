let CHEAT_NAMES = ["fly","speed","automine","noclip","killaura","reach","nofall","scaffold","antikick","nolag","fastbreak","secure"];

function btn(name, value) {
  return `<button class="${value?'on':'off'}" onclick="toggle('${name}', ${!value})">${name}: ${value?'ON':'OFF'}</button>`;
}

async function refresh() {
  const r = await fetch("/api/status");
  const j = await r.json();
  const s = j.status;
  document.getElementById("state").textContent = "state: " + s.state;
  document.getElementById("status").textContent = JSON.stringify(s, null, 2);
  document.getElementById("logs").textContent = j.logs.join("\n");
  document.getElementById("cheats").innerHTML = CHEAT_NAMES.map(n => btn(n, s.cheats[n])).join(" ");
  const t = s.target.split(":");
  const l = s.listen.split(":");
  document.getElementById("target_ip").value = t[0];
  document.getElementById("target_port").value = t[1];
  document.getElementById("listen_host").value = l[0];
  document.getElementById("listen_port").value = l[1];
}

async function toggle(name, value) {
  await fetch("/api/cheat", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({name, value})});
  refresh();
}

async function saveConfig() {
  const body = {
    target_ip: document.getElementById("target_ip").value,
    target_port: document.getElementById("target_port").value,
    listen_host: document.getElementById("listen_host").value,
    listen_port: document.getElementById("listen_port").value,
  };
  await fetch("/api/config", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(body)});
  refresh();
}

async function startProxy() { await fetch("/api/start", {method:"POST"}); refresh(); }
async function stopProxy()  { await fetch("/api/stop",  {method:"POST"}); refresh(); }

setInterval(refresh, 2000);
refresh();
