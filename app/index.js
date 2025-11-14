import init, { Game } from "../core/pkg/othello_wasm.js";

async function main() {
  await init();
  const game = new Game();
  const boardEl = document.getElementById("board");
  const infoTurn = document.getElementById("turn");
  const scoreEl = document.getElementById("score");
  const resetBtn = document.getElementById("reset");

  // --- Build Table ---
  for (let r=0;r<8;r++){
    const tr = document.createElement("tr");
    for (let c=0;c<8;c++){
      const td = document.createElement("td");
      td.dataset.idx = (r*8 + c).toString();
      tr.appendChild(td);
    }
    boardEl.appendChild(tr);
  }

  // --- Renderer ---
  function render() {
    const arr = game.get_board();
    for (let i=0;i<64;i++){
      const td = boardEl.querySelector(`td[data-idx='${i}']`);
      td.innerHTML = "";
      if (arr[i] === 0) continue;

      const d = document.createElement("div");
      d.className = "cell-inner " + (arr[i] === 1 ? "black" : "white");
      td.appendChild(d);
    }
    const counts = game.counts();
    scoreEl.textContent = ` Black: ${counts[0]}  White: ${counts[1]}`;
    infoTurn.textContent =
      `Turn: ${game.get_turn() === 1 ? "Black (AI)" : "White (AI)"}`;
  }

  // --- Black AI (JS側) : greedy evaluation ---
  // Rust の "best_move" は private → JS側で同じ評価で決定する
  function bestMoveBlack(boardArr) {
    const weights = [
      120,-20,20,5,5,20,-20,120,
      -20,-40,-5,-5,-5,-5,-40,-20,
      20,-5,15,3,3,15,-5,20,
      5,-5,3,3,3,3,-5,5,
      5,-5,3,3,3,3,-5,5,
      20,-5,15,3,3,15,-5,20,
      -20,-40,-5,-5,-5,-5,-40,-20,
      120,-20,20,5,5,20,-20,120
    ];

    function collectFlips(pos, player) {
      const DIRS = [
        [-1,-1],[-1,0],[-1,1],
        [0,-1],[0,1],
        [1,-1],[1,0],[1,1]
      ];
      let res = [];
      let row = Math.floor(pos/8), col = pos%8;
      let opp = 3 - player;
      for (let [dr,dc] of DIRS) {
        let r=row+dr, c=col+dc;
        let tmp = [];
        let foundOpp = false;
        while (r>=0 && r<8 && c>=0 && c<8) {
          let idx=r*8+c;
          let v = boardArr[idx];
          if (v===opp) { foundOpp=true; tmp.push(idx);}
          else if (v===player) {
            if (foundOpp) res.push(...tmp);
            break;
          } else break;
          r+=dr; c+=dc;
        }
      }
      return res;
    }

    let best = -999999;
    let bestIdx = null;

    for (let i=0;i<64;i++){
      if (boardArr[i] !== 0) continue;
      let flips = collectFlips(i,1);
      if (flips.length===0) continue;

      let score = weights[i] + flips.length * 8;
      if (score > best) {
        best = score;
        bestIdx = i;
      }
    }

    return bestIdx; // null → pass
  }

  // --- AI vs AI loop ---
  let running = false;

  function step() {
    if (!running) return;

    const turn = game.get_turn();

    // --- Black AI ---
    if (turn === 1) {
      const arr = game.get_board();
      const idx = bestMoveBlack(arr);
      if (idx === null) {
        game.play(255); // pass
      } else {
        game.play(idx);
      }
      render();
    }

    // --- White AI（Rust側の ai_move） ---
    if (running && game.get_turn() === 2) {
      game.ai_move();
      render();
    }

    // --- End check ---
    const movesBlack =
      game.legal_moves ? game.legal_moves(1) : []; // (wasm exposes? if not skip)
    const movesWhite =
      game.legal_moves ? game.legal_moves(2) : [];

    if (movesBlack.length === 0 && movesWhite.length === 0) {
      running = false;
      infoTurn.textContent += " — Finished";
      return;
    }

    setTimeout(step, 200);
  }

  // --- Start automatically ---
  running = true;
  render();
  setTimeout(step, 200);

  // --- Reset ---
  resetBtn.addEventListener("click", () => {
    game.reset();
    running = true;
    render();
    setTimeout(step, 200);
  });
}

main();
