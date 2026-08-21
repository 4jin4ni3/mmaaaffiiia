# -*- coding: utf-8 -*-
INDEX_HTML = r'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>🕵️ 마피아 게임</title>
<style>
  :root {
    --bg: #f5f6f8; --panel: #ffffff; --line: #e5e8eb; --soft: #f1f3f5;
    --text: #222528; --dim: #8b94a1; --green: #03c75a; --green-dark: #02b050;
    --green-soft: #e6f9ee; --red: #e5484d; --red-soft: #ffecec;
    --blue: #3182f6; --blue-soft: #eaf2fe; --gold: #b8860b; --gold-soft: #fff7e0;
    --purple: #7c4dcc; --purple-soft: #f3ecfd;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: var(--bg); color: var(--text); height: 100dvh;
    font-family: "Segoe UI", "Malgun Gothic", "Apple SD Gothic Neo", sans-serif; overflow: hidden;
  }
  button { font-family: inherit; }

  /* ---------- 입장 화면 ---------- */
  #joinScreen {
    height: 100%; display: flex; align-items: center; justify-content: center; padding: 20px;
  }
  .joinCard {
    background: var(--panel); border: 1px solid var(--line); border-radius: 20px;
    padding: 44px 40px; display: flex; flex-direction: column; align-items: center; gap: 16px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.06); width: 360px; max-width: 92vw;
  }
  .joinCard h1 { font-size: 30px; }
  .joinCard p { color: var(--dim); text-align: center; line-height: 1.7; font-size: 14px; }
  .joinCard input {
    width: 100%; padding: 13px 16px; font-size: 16px; border-radius: 12px;
    border: 1.5px solid var(--line); background: var(--panel); color: var(--text);
    outline: none; text-align: center;
  }
  .joinCard input:focus { border-color: var(--green); }
  #joinBtn {
    width: 100%; padding: 13px; font-size: 16px; font-weight: 700;
    border: none; border-radius: 12px; background: var(--green); color: #fff; cursor: pointer;
  }
  #joinBtn:hover { background: var(--green-dark); }
  #joinErr { color: var(--red); min-height: 18px; font-size: 13px; }

  /* ---------- 게임 화면 ---------- */
  #gameScreen { height: 100%; display: none; flex-direction: column; }

  header {
    display: flex; align-items: center; gap: 12px; padding: 12px 18px;
    background: var(--panel); border-bottom: 1px solid var(--line); flex-wrap: wrap;
  }
  #roomTitle { font-weight: 800; font-size: 16px; }
  #phaseBadge {
    font-size: 14px; font-weight: 700; padding: 5px 13px; border-radius: 20px;
    background: var(--soft); color: var(--text);
  }
  #phaseBadge.night { background: #e8ecff; color: #4655b8; }
  #phaseBadge.day { background: var(--gold-soft); color: #8a6a10; }
  #phaseBadge.vote { background: var(--red-soft); color: #c23238; }
  #timerBox { font-size: 18px; font-weight: 800; font-variant-numeric: tabular-nums; min-width: 48px; color: var(--text); }
  #timerBox.low { color: var(--red); }
  #hint { color: var(--dim); font-size: 13px; flex: 1; min-width: 150px; }
  header button {
    padding: 8px 18px; border: none; border-radius: 20px; font-weight: 700;
    background: var(--green); color: #fff; cursor: pointer; font-size: 14px;
  }
  header button:hover { background: var(--green-dark); }
  header button:disabled { background: var(--soft); color: var(--dim); cursor: not-allowed; }

  .main { flex: 1; display: flex; min-height: 0; }

  /* 왼쪽: 참가자 목록 + 내 직업 */
  aside {
    width: 240px; background: var(--panel); border-right: 1px solid var(--line);
    display: flex; flex-direction: column; padding: 12px; gap: 8px; overflow-y: auto;
  }
  #roleCard {
    border-radius: 14px; padding: 12px 14px; font-size: 13px; line-height: 1.55;
    border: 1px solid var(--line);
  }
  #roleCard .rname { font-size: 17px; font-weight: 800; }
  #roleCard.mafia   { background: var(--red-soft); }    #roleCard.mafia .rname   { color: var(--red); }
  #roleCard.doctor  { background: var(--green-soft); }  #roleCard.doctor .rname  { color: #029a46; }
  #roleCard.police  { background: var(--blue-soft); }   #roleCard.police .rname  { color: var(--blue); }
  #roleCard.citizen { background: var(--gold-soft); }   #roleCard.citizen .rname { color: var(--gold); }
  #roleCard .rdesc { color: #5b626b; }
  .listTitle { font-size: 12px; color: var(--dim); margin-top: 4px; font-weight: 700; }
  .pcard {
    display: flex; align-items: center; gap: 8px; padding: 10px 12px;
    border-radius: 12px; background: var(--panel); border: 1.5px solid var(--line);
    font-size: 14px; font-weight: 600;
  }
  .pcard .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--green); flex: none; }
  .pcard.off .dot { background: #c6ccd4; }
  .pcard.dead { opacity: 0.4; text-decoration: line-through; background: var(--soft); }
  .pcard.me { border-color: var(--green); background: var(--green-soft); }
  .pcard .tag { margin-left: auto; font-size: 11px; color: var(--dim); }
  .pcard .tag.mate { color: var(--red); font-weight: 800; }
  .pcard.targetable { cursor: pointer; }
  .pcard.targetable:hover { border-color: var(--red); background: var(--red-soft); }
  .pcard.picked { border-color: var(--red); background: var(--red-soft); }
  .pcard.picked::after { content: "🎯"; margin-left: auto; }
  #skipBtn {
    padding: 10px; border-radius: 12px; border: 1.5px dashed var(--line);
    background: transparent; color: var(--dim); cursor: pointer; font-size: 13px; display: none; font-weight: 600;
  }
  #skipBtn:hover { color: var(--text); border-color: var(--dim); }

  /* 오른쪽: 채팅 */
  .chatWrap { flex: 1; display: flex; flex-direction: column; min-width: 0; background: var(--bg); }
  #log { flex: 1; overflow-y: auto; padding: 16px 18px; display: flex; flex-direction: column; gap: 4px; }

  .mrow { display: flex; flex-direction: column; align-items: flex-start; margin: 3px 0; }
  .mrow.mine { align-items: flex-end; }
  .mnick { font-size: 12px; color: #6b7280; margin: 0 4px 3px; font-weight: 700; }
  .bline { display: flex; align-items: flex-end; gap: 6px; max-width: 78%; }
  .mrow.mine .bline { flex-direction: row-reverse; }
  .bubble {
    background: var(--panel); border: 1px solid var(--line); padding: 9px 13px;
    border-radius: 16px; font-size: 14.5px; line-height: 1.5; word-break: break-word;
  }
  .mrow.mine .bubble { background: var(--green-soft); border-color: #bfe9d0; }
  .mrow.mafia .bubble { background: var(--red-soft); border-color: #f5c6c8; }
  .mrow.mafia .mnick { color: var(--red); }
  .mrow.dead .bubble { background: var(--soft); color: var(--dim); font-style: italic; }
  .mrow.dead .mnick { color: var(--dim); }
  .mtime { font-size: 11px; color: #a8afb8; flex: none; padding-bottom: 2px; }

  .sysline { font-size: 13px; color: var(--dim); text-align: center; padding: 3px 0; }
  .sysline.big {
    color: var(--text); background: var(--panel); border: 1px solid var(--line);
    border-radius: 20px; padding: 8px 16px; margin: 6px auto; font-weight: 600; font-size: 13.5px;
    max-width: 90%;
  }
  .sysline.err { color: var(--red); }
  .sysline.private { color: #029a46; font-weight: 600; }
  .sysline.police {
    color: var(--purple); font-weight: 700; background: var(--purple-soft);
    border-radius: 20px; padding: 8px 16px; margin: 4px auto; max-width: 90%;
  }
  .sysline.mafia { color: var(--red); }
  .sysline.over {
    text-align: center; font-size: 18px; font-weight: 800; padding: 14px;
    border-radius: 14px; margin: 8px 0;
  }
  .sysline.over.mafia-win { background: var(--red-soft); border: 1px solid #f0b6b9; color: #c0272d; }
  .sysline.over.citizen-win { background: var(--green-soft); border: 1px solid #b5e6c8; color: #028a3f; }

  #chatForm { display: flex; gap: 8px; padding: 12px 14px; border-top: 1px solid var(--line); background: var(--panel); }
  #chatInput {
    flex: 1; padding: 12px 16px; border-radius: 22px; font-size: 15px;
    border: 1.5px solid var(--line); background: var(--panel); color: var(--text); outline: none;
  }
  #chatInput:focus { border-color: var(--green); }
  #sendBtn {
    padding: 0 24px; border: none; border-radius: 22px; background: var(--green);
    color: #fff; font-weight: 700; font-size: 15px; cursor: pointer;
  }
  #sendBtn:hover { background: var(--green-dark); }

  @media (max-width: 640px) {
    .main { flex-direction: column; }
    aside {
      width: 100%; max-height: 44%; border-right: none;
      border-bottom: 1px solid var(--line); flex-direction: row; flex-wrap: wrap;
    }
    #roleCard { width: 100%; }
    .pcard { flex: 1 1 45%; font-size: 13px; padding: 8px; }
    .bline { max-width: 92%; }
  }
</style>
</head>
<body>

<div id="joinScreen">
  <div class="joinCard">
    <h1>🕵️ 마피아 게임</h1>
    <p>6~8명이 함께하는 채팅 마피아<br>마피아 2 · 의사 1 · 경찰 1 · 나머지 시민</p>
    <input id="nickInput" maxlength="12" placeholder="닉네임 입력" autocomplete="off">
    <button id="joinBtn">입장하기</button>
    <div id="joinErr"></div>
  </div>
</div>

<div id="gameScreen">
  <header>
    <span id="roomTitle">🕵️ 마피아 게임</span>
    <span id="phaseBadge">대기실</span>
    <span id="timerBox"></span>
    <span id="hint"></span>
    <button id="startBtn" style="display:none">게임 시작</button>
    <button id="restartBtn" style="display:none">다시 하기</button>
  </header>
  <div class="main">
    <aside>
      <div id="roleCard" style="display:none"></div>
      <div class="listTitle" id="listTitle">참가자</div>
      <div id="playerList"></div>
      <button id="skipBtn">🙅 투표 기권</button>
    </aside>
    <div class="chatWrap">
      <div id="log"></div>
      <form id="chatForm">
        <input id="chatInput" maxlength="300" placeholder="메시지 입력..." autocomplete="off">
        <button id="sendBtn" type="submit">전송</button>
      </form>
    </div>
  </div>
</div>

<script>
"use strict";
const $ = id => document.getElementById(id);
let pid = sessionStorage.getItem("mafia_pid") || null;
let es = null, state = null, myRole = null, myMates = [], myPick = null;
let localDeadline = 0, checking = false;

const ROLE_DESC = {
  mafia:   "밤마다 동료와 함께 죽일 사람을 지목하세요. 밤에는 마피아끼리만 채팅할 수 있습니다.",
  doctor:  "밤마다 살릴 사람을 지목하세요. 마피아의 표적과 일치하면 그 사람이 살아납니다.",
  police:  "밤마다 한 명을 조사해 직업을 확인하세요. 결과는 당신에게만 보입니다.",
  citizen: "특별한 능력은 없습니다. 낮 토론과 투표로 마피아를 찾아내세요!"
};
const ROLE_KR = { mafia: "마피아 🔪", doctor: "의사 💉", police: "경찰 🚨", citizen: "시민 👤" };
const PHASE_KR = { lobby: "🏠 대기실", night: "🌙 밤", day_discuss: "☀️ 낮 · 토론", day_vote: "🗳️ 투표", ended: "🏁 게임 종료" };

async function api(body) {
  const r = await fetch("/api", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify(Object.assign({ pid }, body))
  });
  return r.json();
}

// ---------- 입장 ----------
async function join() {
  const nick = $("nickInput").value.trim();
  if (!nick) { $("joinErr").textContent = "닉네임을 입력하세요."; return; }
  const res = await api({ action: "join", nick });
  if (!res.ok) { $("joinErr").textContent = res.error; return; }
  pid = res.pid;
  sessionStorage.setItem("mafia_pid", pid);
  connect();
}
$("joinBtn").onclick = join;
$("nickInput").onkeydown = e => { if (e.key === "Enter") join(); };

function showJoin() {
  sessionStorage.removeItem("mafia_pid");
  pid = null; myRole = null; myMates = []; state = null;
  if (es) { es.close(); es = null; }
  $("gameScreen").style.display = "none";
  $("joinScreen").style.display = "flex";
}

function connect() {
  $("joinScreen").style.display = "none";
  $("gameScreen").style.display = "flex";
  if (es) es.close();
  es = new EventSource("/events?pid=" + pid);
  es.onmessage = e => handle(JSON.parse(e.data));
  es.onerror = async () => {
    if (checking) return;
    checking = true;
    setTimeout(async () => {
      checking = false;
      try {
        const r = await api({ action: "ping" });
        if (!r.ok) { addSys("서버와의 연결이 끊어졌습니다. 다시 입장해주세요.", "err"); showJoin(); }
      } catch (_) { /* 서버 꺼짐 - EventSource가 알아서 재시도 */ }
    }, 3000);
  };
}

// ---------- 이벤트 처리 ----------
function handle(ev) {
  switch (ev.type) {
    case "state": {
      const prevPhase = state && state.phase;
      state = ev;
      if (prevPhase !== ev.phase) myPick = null;
      localDeadline = ev.remain > 0 ? Date.now() + ev.remain * 1000 : 0;
      render();
      break;
    }
    case "role":
      myRole = ev.role; myMates = ev.mates || [];
      addSys(`당신의 직업은 [${ROLE_KR[ev.role]}] 입니다. ${ROLE_DESC[ev.role]}`, "private");
      render();
      break;
    case "chat": addChat(ev); break;
    case "sys": addSys(ev.text, ev.cls); break;
    case "police": addSys(`🔍 조사 결과: ${ev.nick}님의 직업은 [${ev.roleKr}] 입니다. (당신에게만 보입니다)`, "police"); break;
    case "ack": myPick = ev.target; render(); break;
    case "over": {
      const div = document.createElement("div");
      div.className = "sysline over " + (ev.winner === "mafia" ? "mafia-win" : "citizen-win");
      div.textContent = ev.winner === "mafia" ? "🔪 마피아의 승리!" : "🎉 시민의 승리!";
      $("log").appendChild(div);
      addSys("직업 공개 — " + ev.roles.map(r => `${r.nick}: ${r.roleKr}${r.alive ? "" : " (사망)"}`).join(" / "), "big");
      scrollLog();
      break;
    }
  }
}

// ---------- 채팅 로그 ----------
function nowTime() {
  const d = new Date();
  const h = d.getHours(), m = String(d.getMinutes()).padStart(2, "0");
  return (h < 12 ? "오전 " : "오후 ") + (h % 12 || 12) + ":" + m;
}
function addChat(ev) {
  const me = state && state.players.find(p => p.pid === pid);
  const isMine = me && ev.nick === me.nick;
  const row = document.createElement("div");
  row.className = "mrow" + (isMine ? " mine" : "") + (ev.ch === "mafia" ? " mafia" : "") + (ev.ch === "dead" ? " dead" : "");

  if (!isMine) {
    const nk = document.createElement("div");
    nk.className = "mnick";
    nk.textContent = (ev.ch === "mafia" ? "🔪 " : ev.ch === "dead" ? "👻 " : "") + ev.nick;
    row.appendChild(nk);
  }
  const line = document.createElement("div");
  line.className = "bline";
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = ev.text;
  const time = document.createElement("span");
  time.className = "mtime";
  time.textContent = nowTime();
  line.append(bubble, time);
  row.appendChild(line);
  $("log").appendChild(row);
  scrollLog();
}
function addSys(text, cls) {
  const div = document.createElement("div");
  div.className = "sysline " + (cls || "sys");
  div.textContent = text;
  $("log").appendChild(div);
  scrollLog();
}
function scrollLog() {
  const log = $("log");
  log.scrollTop = log.scrollHeight;
  while (log.children.length > 400) log.removeChild(log.firstChild);
}

$("chatForm").onsubmit = async e => {
  e.preventDefault();
  const text = $("chatInput").value.trim();
  if (!text) return;
  $("chatInput").value = "";
  const res = await api({ action: "chat", text });
  if (!res.ok) addSys(res.error, "err");
};

// ---------- 렌더링 ----------
function render() {
  if (!state) return;
  const me = state.players.find(p => p.pid === pid);
  const meAlive = me && me.alive;
  const badge = $("phaseBadge");
  badge.textContent = PHASE_KR[state.phase] + (state.day > 0 && state.phase !== "ended" ? ` · ${state.day}일차` : "");
  badge.className = state.phase === "night" ? "night"
                  : state.phase === "day_discuss" ? "day"
                  : state.phase === "day_vote" ? "vote" : "";

  const isHost = state.host === pid;
  $("startBtn").style.display = (state.phase === "lobby" && isHost) ? "" : "none";
  $("startBtn").disabled = state.players.length < state.minPlayers;
  $("restartBtn").style.display = (state.phase === "ended" && isHost) ? "" : "none";

  // 안내문
  let hint = "";
  if (state.phase === "lobby") {
    hint = `${state.players.length}/${state.maxPlayers}명 대기 중` +
           (state.players.length < state.minPlayers ? ` (최소 ${state.minPlayers}명 필요)` : " — 시작 가능!");
    if (!isHost) hint += " · 방장이 시작하면 게임이 열립니다";
  } else if (state.phase === "night") {
    hint = !meAlive ? "당신은 사망했습니다. 관전 중..." :
           myRole === "citizen" ? "시민은 밤에 할 일이 없습니다. 아침을 기다리세요." :
           myPick ? "지목 완료. 마감 전까지 다시 눌러 변경할 수 있습니다." :
           "왼쪽 목록에서 대상을 클릭하세요!";
  } else if (state.phase === "day_discuss") {
    hint = meAlive ? "채팅으로 마피아를 추리하세요." : "당신은 사망했습니다. 관전 중...";
  } else if (state.phase === "day_vote") {
    hint = !meAlive ? "사망자는 투표할 수 없습니다." :
           myPick ? "투표 완료. 다시 눌러 변경할 수 있습니다." : "처형할 사람을 클릭하세요!";
  }
  $("hint").textContent = hint;

  // 기권 버튼
  $("skipBtn").style.display = (state.phase === "day_vote" && meAlive) ? "" : "none";

  // 내 직업 카드
  const rc = $("roleCard");
  if (myRole && state.phase !== "lobby") {
    rc.style.display = "";
    rc.className = myRole;
    rc.innerHTML = "";
    const rname = document.createElement("div");
    rname.className = "rname";
    rname.textContent = ROLE_KR[myRole];
    const rdesc = document.createElement("div");
    rdesc.className = "rdesc";
    rdesc.textContent = ROLE_DESC[myRole] + (myMates.length ? ` 동료: ${myMates.join(", ")}` : "");
    rc.append(rname, rdesc);
  } else rc.style.display = "none";

  // 플레이어 목록
  $("listTitle").textContent = `참가자 (${state.players.filter(p => p.alive).length}명 생존)`;
  const list = $("playerList");
  list.innerHTML = "";
  const canNightAct = state.phase === "night" && meAlive && ["mafia", "doctor", "police"].includes(myRole);
  const canVote = state.phase === "day_vote" && meAlive;

  for (const p of state.players) {
    const card = document.createElement("div");
    card.className = "pcard";
    if (!p.connected) card.classList.add("off");
    if (!p.alive) card.classList.add("dead");
    if (p.pid === pid) card.classList.add("me");

    const dot = document.createElement("span"); dot.className = "dot";
    const name = document.createElement("span");
    name.textContent = (state.host === p.pid ? "👑 " : "") + p.nick + (p.pid === pid ? " (나)" : "");
    card.append(dot, name);

    if (myRole === "mafia" && myMates.includes(p.nick)) {
      const tag = document.createElement("span"); tag.className = "tag mate"; tag.textContent = "동료";
      card.appendChild(tag);
    }
    if (myPick === p.pid) card.classList.add("picked");

    let targetable = false;
    if (p.alive && p.pid !== pid) {
      if (canNightAct) {
        targetable = !(myRole === "mafia" && myMates.includes(p.nick));
      } else if (canVote) targetable = true;
    }
    if (canNightAct && myRole === "doctor" && p.pid === pid && p.alive) targetable = true; // 의사는 자가치료 가능
    if (targetable) {
      card.classList.add("targetable");
      card.onclick = async () => {
        const res = await api({ action: state.phase === "night" ? "act" : "vote", target: p.pid });
        if (!res.ok) addSys(res.error, "err");
      };
    }
    list.appendChild(card);
  }
}

$("startBtn").onclick = async () => {
  const res = await api({ action: "start" });
  if (!res.ok) addSys(res.error, "err");
};
$("restartBtn").onclick = async () => {
  const res = await api({ action: "restart" });
  if (!res.ok) addSys(res.error, "err");
};
$("skipBtn").onclick = async () => {
  const res = await api({ action: "vote", target: "skip" });
  if (!res.ok) addSys(res.error, "err");
};

// 타이머 표시
setInterval(() => {
  const box = $("timerBox");
  if (!localDeadline) { box.textContent = ""; return; }
  const s = Math.max(0, Math.ceil((localDeadline - Date.now()) / 1000));
  box.textContent = s > 0 ? `⏱ ${s}` : "";
  box.className = s <= 10 && s > 0 ? "low" : "";
}, 300);

// 새로고침 시 자동 재입장
(async () => {
  if (!pid) return;
  try {
    const r = await api({ action: "ping" });
    if (r.ok) connect(); else showJoin();
  } catch (_) { showJoin(); }
})();
</script>
</body>
</html>
'''

"""
마피아 게임 서버 (표준 라이브러리만 사용, Python 3.8+)

실행:  python server.py
접속:  브라우저에서 http://<이 PC의 IP>:8000

규칙:
  - 최소 6명 ~ 최대 8명
  - 직업: 마피아 2, 의사 1, 경찰 1, 나머지 시민
  - 밤: 마피아 2명이 투표로 1명 지목(의견이 갈리면 랜덤 선택), 의사는 1명 치료,
        경찰은 1명 조사(직업을 본인만 확인)
  - 아침: 사망자 공지. 의사가 살렸으면 "의사가 살렸다"만 공지(대상은 비공개)
  - 낮: 자유 토론 후 투표로 1명 처형(동점이면 처형 없음)
  - 승리: 마피아 전멸 → 시민 승 / 마피아 수 >= 나머지 수 → 마피아 승
"""
import json
import os
import queue
import random
import socket
import sys
import threading
import time
import uuid
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = int(os.environ.get("PORT") or os.environ.get("MAFIA_PORT") or "8000")
MIN_PLAYERS = 6
MAX_PLAYERS = 8
NIGHT_SECONDS = int(os.environ.get("MAFIA_NIGHT_SECONDS", "60"))
DISCUSS_SECONDS = int(os.environ.get("MAFIA_DISCUSS_SECONDS", "120"))
VOTE_SECONDS = int(os.environ.get("MAFIA_VOTE_SECONDS", "40"))

ROLE_KR = {"mafia": "마피아", "doctor": "의사", "police": "경찰", "citizen": "시민"}
ROOT = os.path.dirname(os.path.abspath(__file__))


class Player:
    def __init__(self, nick):
        self.pid = uuid.uuid4().hex
        self.nick = nick
        self.role = None
        self.alive = True
        self.connected = True
        self.gen = 0            # SSE 재접속 세대 번호
        self.q = queue.Queue()


class Game:
    def __init__(self):
        self.lock = threading.RLock()
        self.players = {}       # pid -> Player
        self.order = []         # 입장 순서(pid)
        self.phase = "lobby"    # lobby / night / day_discuss / day_vote / ended
        self.day = 0
        self.deadline = 0.0
        self.timer = None
        self.token = 0
        self.mafia_votes = {}
        self.doctor_target = None
        self.police_done = False
        self.day_votes = {}

    # ---------- 전송 ----------
    def send(self, p, ev):
        p.q.put(json.dumps(ev, ensure_ascii=False))

    def broadcast(self, ev, only=None):
        for p in self.players.values():
            if only is None or only(p):
                self.send(p, ev)

    def sysmsg(self, text, cls="sys", only=None):
        self.broadcast({"type": "sys", "text": text, "cls": cls}, only)

    def host_pid(self):
        for pid in self.order:
            if pid in self.players:
                return pid
        return None

    def state_ev(self):
        return {
            "type": "state",
            "phase": self.phase,
            "day": self.day,
            "remain": max(0, round(self.deadline - time.time())) if self.phase in ("night", "day_discuss", "day_vote") else 0,
            "host": self.host_pid(),
            "minPlayers": MIN_PLAYERS,
            "maxPlayers": MAX_PLAYERS,
            "players": [
                {"pid": p.pid, "nick": p.nick, "alive": p.alive, "connected": p.connected}
                for pid in self.order if (p := self.players.get(pid))
            ],
        }

    def push_state(self):
        self.broadcast(self.state_ev())

    def snapshot_for(self, p):
        """SSE (재)접속 시 해당 플레이어에게 현재 상황 전체를 보냄."""
        self.send(p, {"type": "hello", "pid": p.pid})
        self.send(p, {"type": "sys", "cls": "private",
                      "text": f"✅ {p.nick}님, 접속했습니다. "
                              f"{MIN_PLAYERS}명 이상 모이면 방장(👑)이 게임을 시작할 수 있습니다."})
        self.send(p, self.state_ev())
        if p.role:
            self.send(p, self.role_ev(p))
        if self.phase == "ended":
            self.send(p, self.over_ev())

    def role_ev(self, p):
        ev = {"type": "role", "role": p.role, "roleKr": ROLE_KR[p.role]}
        if p.role == "mafia":
            ev["mates"] = [q.nick for q in self.players.values()
                           if q.role == "mafia" and q.pid != p.pid]
        return ev

    # ---------- 타이머 ----------
    def _set_timer(self, seconds, fn):
        if self.timer:
            self.timer.cancel()
        self.token += 1
        tok = self.token
        self.deadline = time.time() + seconds

        def fire():
            with self.lock:
                if tok == self.token:
                    fn()

        t = threading.Timer(seconds, fire)
        t.daemon = True
        t.start()
        self.timer = t

    def _advance(self, fn):
        """조건이 일찍 충족됐을 때 타이머를 취소하고 즉시 다음 단계로."""
        if self.timer:
            self.timer.cancel()
        self.token += 1
        fn()

    # ---------- 로비 ----------
    def join(self, nick):
        nick = (nick or "").strip()[:12]
        if not nick:
            return {"ok": False, "error": "닉네임을 입력하세요."}
        if self.phase != "lobby":
            return {"ok": False, "error": "게임이 이미 진행 중입니다. 끝난 뒤에 들어와 주세요."}
        if len(self.players) >= MAX_PLAYERS:
            return {"ok": False, "error": f"정원({MAX_PLAYERS}명)이 가득 찼습니다."}
        if any(p.nick == nick for p in self.players.values()):
            return {"ok": False, "error": "이미 사용 중인 닉네임입니다."}
        p = Player(nick)
        self.players[p.pid] = p
        self.order.append(p.pid)
        self.sysmsg(f"👋 {nick}님이 입장했습니다. (현재 {len(self.players)}명)")
        self.push_state()
        return {"ok": True, "pid": p.pid}

    def remove_if_gone(self, pid, gen):
        """로비에서 연결이 끊긴 채 10초가 지나면 퇴장 처리."""
        p = self.players.get(pid)
        if p and not p.connected and p.gen == gen and self.phase == "lobby":
            del self.players[pid]
            self.order.remove(pid)
            self.sysmsg(f"🚪 {p.nick}님이 나갔습니다. (현재 {len(self.players)}명)")
            self.push_state()

    # ---------- 게임 시작 ----------
    def start(self, pid):
        if self.phase != "lobby":
            return {"ok": False, "error": "이미 게임 중입니다."}
        if pid != self.host_pid():
            return {"ok": False, "error": "방장만 시작할 수 있습니다."}
        n = len(self.players)
        if n < MIN_PLAYERS:
            return {"ok": False, "error": f"최소 {MIN_PLAYERS}명이 필요합니다. (현재 {n}명)"}

        pids = list(self.players.keys())
        random.shuffle(pids)
        roles = ["mafia", "mafia", "doctor", "police"] + ["citizen"] * (n - 4)
        for pid_, role in zip(pids, roles):
            self.players[pid_].role = role
        for p in self.players.values():
            p.alive = True
            self.send(p, self.role_ev(p))

        self.day = 0
        self.sysmsg(f"🎮 게임 시작! 참가자 {n}명 — 마피아 2, 의사 1, 경찰 1, 시민 {n - 4}", "big")
        self.start_night()
        return {"ok": True}

    # ---------- 밤 ----------
    def start_night(self):
        self.phase = "night"
        self.day += 1
        self.mafia_votes = {}
        self.doctor_target = None
        self.police_done = False
        self.sysmsg(f"🌙 {self.day}일차 밤이 되었습니다. 마피아·의사·경찰은 대상을 선택하세요. "
                    f"(제한시간 {NIGHT_SECONDS}초, 밤에는 마피아끼리만 대화할 수 있습니다)", "big")
        self._set_timer(NIGHT_SECONDS, self.resolve_night)
        self.push_state()

    def act(self, pid, target):
        p = self.players.get(pid)
        if not p or self.phase != "night":
            return {"ok": False, "error": "지금은 선택할 수 없습니다."}
        if not p.alive:
            return {"ok": False, "error": "사망한 플레이어는 행동할 수 없습니다."}
        t = self.players.get(target)
        if not t or not t.alive:
            return {"ok": False, "error": "살아있는 플레이어를 선택하세요."}

        if p.role == "mafia":
            if t.role == "mafia":
                return {"ok": False, "error": "동료 마피아는 지목할 수 없습니다."}
            self.mafia_votes[pid] = target
            self.sysmsg(f"🔪 {p.nick}님이 {t.nick}님을 지목했습니다.", "mafia",
                        only=lambda x: x.role == "mafia" and x.alive)
        elif p.role == "doctor":
            self.doctor_target = target
            self.send(p, {"type": "sys", "text": f"💉 {t.nick}님을 치료 대상으로 지정했습니다.", "cls": "private"})
        elif p.role == "police":
            if self.police_done:
                return {"ok": False, "error": "오늘 밤 조사는 이미 끝났습니다."}
            if t.pid == pid:
                return {"ok": False, "error": "자기 자신은 조사할 수 없습니다."}
            self.police_done = True
            self.send(p, {"type": "police", "nick": t.nick, "roleKr": ROLE_KR[t.role]})
        else:
            return {"ok": False, "error": "시민은 밤에 할 수 있는 행동이 없습니다."}

        self.broadcast({"type": "ack", "target": target if p.role != "police" else None},
                       only=lambda x: x.pid == pid)
        if self._night_done():
            self._advance(self.resolve_night)
        return {"ok": True}

    def _night_done(self):
        mafia_alive = [p for p in self.players.values() if p.role == "mafia" and p.alive]
        doctor_alive = [p for p in self.players.values() if p.role == "doctor" and p.alive]
        police_alive = [p for p in self.players.values() if p.role == "police" and p.alive]
        if any(m.pid not in self.mafia_votes for m in mafia_alive):
            return False
        if doctor_alive and self.doctor_target is None:
            return False
        if police_alive and not self.police_done:
            return False
        return True

    def resolve_night(self):
        votes = list(self.mafia_votes.values())
        kill = None
        if votes:
            counts = {}
            for v in votes:
                counts[v] = counts.get(v, 0) + 1
            top = max(counts.values())
            kill = random.choice([v for v, c in counts.items() if c == top])

        saved = kill is not None and self.doctor_target == kill
        if kill and not saved:
            victim = self.players[kill]
            victim.alive = False
            self.sysmsg(f"☀️ 아침이 밝았습니다. 지난 밤, {victim.nick}님이 살해당했습니다. 😵", "big")
        elif kill and saved:
            self.sysmsg("☀️ 아침이 밝았습니다. 마피아의 습격이 있었지만, 의사가 살려냈습니다! "
                        "아무도 죽지 않았습니다. 💉", "big")
        else:
            self.sysmsg("☀️ 아침이 밝았습니다. 지난 밤에는 아무 일도 일어나지 않았습니다.", "big")

        if not self.check_win():
            self.start_discuss()

    # ---------- 낮 ----------
    def start_discuss(self):
        self.phase = "day_discuss"
        self.sysmsg(f"💬 자유 토론 시간입니다. 누가 마피아인지 의견을 나누세요. "
                    f"({DISCUSS_SECONDS}초 후 투표가 시작됩니다)")
        self._set_timer(DISCUSS_SECONDS, self.start_vote)
        self.push_state()

    def start_vote(self):
        self.phase = "day_vote"
        self.day_votes = {}
        self.sysmsg(f"🗳️ 투표 시간입니다! 처형할 사람을 지목하세요. "
                    f"(제한시간 {VOTE_SECONDS}초, 최다 득표자 처형 / 동점이면 처형 없음)", "big")
        self._set_timer(VOTE_SECONDS, self.resolve_vote)
        self.push_state()

    def vote(self, pid, target):
        p = self.players.get(pid)
        if not p or self.phase != "day_vote":
            return {"ok": False, "error": "지금은 투표 시간이 아닙니다."}
        if not p.alive:
            return {"ok": False, "error": "사망한 플레이어는 투표할 수 없습니다."}
        if target != "skip":
            t = self.players.get(target)
            if not t or not t.alive:
                return {"ok": False, "error": "살아있는 플레이어를 선택하세요."}
            if target == pid:
                return {"ok": False, "error": "자기 자신에게는 투표할 수 없습니다."}
            self.sysmsg(f"🗳️ {p.nick} ➜ {t.nick} 지목")
        else:
            self.sysmsg(f"🗳️ {p.nick}님이 기권했습니다.")
        self.day_votes[pid] = target
        self.broadcast({"type": "ack", "target": target}, only=lambda x: x.pid == pid)

        alive = [q for q in self.players.values() if q.alive]
        if all(q.pid in self.day_votes for q in alive):
            self._advance(self.resolve_vote)
        return {"ok": True}

    def resolve_vote(self):
        counts = {}
        for v in self.day_votes.values():
            if v != "skip":
                counts[v] = counts.get(v, 0) + 1
        executed = None
        if counts:
            top = max(counts.values())
            leaders = [v for v, c in counts.items() if c == top]
            if len(leaders) == 1:
                executed = leaders[0]

        if executed:
            t = self.players[executed]
            t.alive = False
            self.sysmsg(f"⚖️ 투표 결과, {t.nick}님이 처형되었습니다. "
                        f"{t.nick}님의 직업은 [{ROLE_KR[t.role]}]였습니다.", "big")
        else:
            self.sysmsg("⚖️ 투표가 갈렸습니다. 이번에는 아무도 처형되지 않았습니다.", "big")

        if not self.check_win():
            self.start_night()

    # ---------- 승패 ----------
    def check_win(self):
        maf = sum(1 for p in self.players.values() if p.role == "mafia" and p.alive)
        oth = sum(1 for p in self.players.values() if p.role != "mafia" and p.alive)
        winner = None
        if maf == 0:
            winner = "citizen"
        elif maf >= oth:
            winner = "mafia"
        if winner:
            self.phase = "ended"
            if self.timer:
                self.timer.cancel()
            self.token += 1
            self.broadcast(self.over_ev(winner))
            self.push_state()
            return True
        return False

    def over_ev(self, winner=None):
        if winner is None:
            maf = sum(1 for p in self.players.values() if p.role == "mafia" and p.alive)
            winner = "citizen" if maf == 0 else "mafia"
        return {
            "type": "over",
            "winner": winner,
            "roles": [{"nick": p.nick, "roleKr": ROLE_KR[p.role], "alive": p.alive}
                      for pid in self.order if (p := self.players.get(pid)) and p.role],
        }

    def restart(self, pid):
        if self.phase != "ended":
            return {"ok": False, "error": "게임이 끝난 뒤에만 초기화할 수 있습니다."}
        if pid != self.host_pid():
            return {"ok": False, "error": "방장만 다시 시작할 수 있습니다."}
        for p in self.players.values():
            p.role = None
            p.alive = True
        self.phase = "lobby"
        self.day = 0
        self.mafia_votes = {}
        self.doctor_target = None
        self.day_votes = {}
        self.sysmsg("🔄 방장이 게임을 초기화했습니다. 대기실로 돌아갑니다.", "big")
        self.push_state()
        return {"ok": True}

    # ---------- 채팅 ----------
    def chat(self, pid, text):
        p = self.players.get(pid)
        text = (text or "").strip()[:300]
        if not p or not text:
            return {"ok": False, "error": "잘못된 요청입니다."}

        if not p.alive:
            self.broadcast({"type": "chat", "nick": p.nick, "text": text, "ch": "dead"},
                           only=lambda x: not x.alive)
            return {"ok": True}
        if self.phase == "night":
            if p.role == "mafia":
                self.broadcast({"type": "chat", "nick": p.nick, "text": text, "ch": "mafia"},
                               only=lambda x: x.role == "mafia")
                return {"ok": True}
            return {"ok": False, "error": "밤에는 대화할 수 없습니다. (마피아만 가능)"}
        self.broadcast({"type": "chat", "nick": p.nick, "text": text, "ch": "all"})
        return {"ok": True}


game = Game()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/" or url.path == "/index.html":
            body = INDEX_HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif url.path == "/events":
            self.handle_sse(parse_qs(url.query).get("pid", [""])[0])
        else:
            self.send_error(404)

    def handle_sse(self, pid):
        with game.lock:
            p = game.players.get(pid)
            if not p:
                self.send_error(404)
                return
            p.gen += 1
            gen = p.gen
            p.q = queue.Queue()
            was_disconnected = not p.connected
            p.connected = True
            game.snapshot_for(p)
            if was_disconnected:
                game.push_state()
            q = p.q

        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        try:
            while True:
                if p.gen != gen:
                    break
                try:
                    msg = q.get(timeout=15)
                    self.wfile.write(("data: " + msg + "\n\n").encode("utf-8"))
                except queue.Empty:
                    self.wfile.write(b": ping\n\n")
                self.wfile.flush()
        except (OSError, ValueError):
            pass
        finally:
            with game.lock:
                if p.gen == gen:
                    p.connected = False
                    game.push_state()
                    if game.phase == "lobby":
                        t = threading.Timer(10, lambda: _prune(pid, gen))
                        t.daemon = True
                        t.start()

    def do_POST(self):
        if urlparse(self.path).path != "/api":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, json.JSONDecodeError):
            self._json({"ok": False, "error": "잘못된 요청입니다."}, 400)
            return

        action = data.get("action")
        pid = data.get("pid", "")
        with game.lock:
            if action == "join":
                res = game.join(data.get("nick"))
            elif action == "ping":
                res = {"ok": pid in game.players}
            elif action == "start":
                res = game.start(pid)
            elif action == "restart":
                res = game.restart(pid)
            elif action == "chat":
                res = game.chat(pid, data.get("text"))
            elif action == "act":
                res = game.act(pid, data.get("target"))
            elif action == "vote":
                res = game.vote(pid, data.get("target"))
            else:
                res = {"ok": False, "error": "알 수 없는 요청입니다."}
        self._json(res)


def _prune(pid, gen):
    with game.lock:
        game.remove_if_gone(pid, gen)


def lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return "127.0.0.1"


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    server.daemon_threads = True
    print("=" * 52)
    print("  🕵️  마피아 게임 서버가 시작되었습니다!")
    print("=" * 52)
    print(f"  내 컴퓨터에서 접속:      http://localhost:{PORT}")
    print(f"  같은 와이파이 친구 접속:  http://{lan_ip()}:{PORT}")
    print("=" * 52)
    print("  종료하려면 Ctrl+C 를 누르세요.")
    server.serve_forever()


if __name__ == "__main__":
    main()
