import init, { Game } from "../core/pkg/othello_wasm.js"; // after wasm-pack this path is typical

async function main() {
  await init();
  const game = new Game();
  const boardEl = document.getElementById("board");
  const infoTurn = document.getElementById("turn");
  const scoreEl = document.getElementById("score");
  const resetBtn = document.getElementById("reset");

  // build table
  for (let r=0;r<8;r++){
    const tr = document.createElement("tr");
    for (let c=0;c<8;c++){
      const td = document.createElement("td");
      td.dataset.idx = (r*8 + c).toString();
      td.addEventListener("click", onCellClick);
      tr.appendChild(td);
    }
    boardEl.appendChild(tr);
  }

  function render() {
    const arr = game.get_board(); // Uint8Array-like
    for (let i=0;i<64;i++){
      const td = boardEl.querySelector(`td[data-idx='${i}']`);
      td.innerHTML = "";
      if (arr[i] === 1) {
        const d = document.createElement("div");
        d.className = "cell-inner black";
        td.appendChild(d);
      } else if (arr[i] === 2) {
        const d = document.createElement("div");
        d.className = "cell-inner white";
        td.appendChild(d);
      } else {
        // show hint if legal for current player
        const turn = game.get_turn();
        // check if legal
        // We can't see legal_moves from wasm directly; try to play on a copy? Simpler: ask user to click — we'll show nothing.
      }
    }
    const turn = game.get_turn();
    infoTurn.textContent = `Turn: ${turn === 1 ? "Black (you)" : "White (AI)"}`
    const counts = game.counts();
    scoreEl.textContent = `Black: ${counts[0]}  White: ${counts[1]}`;
  }

  function onCellClick(e) {
    const idx = Number(e.currentTarget.dataset.idx);
    if (game.get_turn() !== 1) return; // only allow human when black
    const ok = game.play(idx);
    if (!ok) {
      // illegal
      return;
    }
    render();
    // after human move, if AI has turn, call ai_move
    if (game.get_turn() === 2) {
      setTimeout(() => {
        const aiIdx = game.ai_move();
        // aiIdx == 255 means pass
        render();
      }, 150); // small delay for UX
    }
  }

  resetBtn.addEventListener("click", () => {
    game.reset();
    render();
  });

  render();
}

main();
