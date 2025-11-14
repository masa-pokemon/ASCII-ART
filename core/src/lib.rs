use wasm_bindgen::prelude::*;

/// Board representation:
/// 0 = empty, 1 = black, 2 = white
/// index = row * 8 + col, 0..63

const DIRS: [(i32,i32);8] = [
    (-1,-1), (-1,0), (-1,1),
    (0,-1),         (0,1),
    (1,-1),  (1,0), (1,1)
];

// positional weights (common Othello heuristics)
// corners very high, adjacent-to-corner very negative, edges positive, inner small
static WEIGHTS: [i32;64] = [
  120, -20,  20,  5,  5, 20, -20, 120,
  -20, -40,  -5, -5, -5, -5, -40, -20,
   20,  -5,  15,  3,  3, 15,  -5,  20,
    5,  -5,   3,  3,  3,  3,  -5,   5,
    5,  -5,   3,  3,  3,  3,  -5,   5,
   20,  -5,  15,  3,  3, 15,  -5,  20,
  -20, -40,  -5, -5, -5, -5, -40, -20,
  120, -20,  20,  5,  5, 20, -20, 120,
];

#[wasm_bindgen]
pub struct Game {
    board: [u8;64],
    turn: u8, // 1 black, 2 white
}

#[wasm_bindgen]
impl Game {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Game {
        let mut b = [0u8;64];
        // initial 4
        b[3 + 3*8] = 2; // d4 white
        b[4 + 4*8] = 2; // e5 white
        b[3 + 4*8] = 1; // d5 black
        b[4 + 3*8] = 1; // e4 black
        Game { board: b, turn: 1 }
    }

    /// returns a copy of the board as a JS Uint8Array
    pub fn get_board(&self) -> Vec<u8> {
        self.board.to_vec()
    }

    /// returns current turn: 1 or 2
    pub fn get_turn(&self) -> u8 {
        self.turn
    }

    /// try to play at index (0..63) for current player.
    /// returns true if move applied (legal). If legal and applied, toggles turn.
    /// if idx == 255 -> pass
    pub fn play(&mut self, idx: u8) -> bool {
        if idx == 255 {
            // pass
            self.turn = 3 - self.turn;
            return true;
        }
        let pos = idx as usize;
        if pos >= 64 { return false; }
        if self.board[pos] != 0 { return false; }
        let flips = self.collect_flips(pos, self.turn);
        if flips.is_empty() { return false; }
        // apply flips and place
        self.board[pos] = self.turn;
        for p in flips { self.board[p] = self.turn; }
        self.turn = 3 - self.turn;
        true
    }

    /// AI move for white (2). This chooses the move that maximizes evaluation:
    /// eval = positional weight + 8 * flipped_count
    /// It's a greedy best-move (局所評価の最善手).
    /// returns chosen index (0..63) or 255 for pass.
    pub fn ai_move(&mut self) -> u8 {
        let player = 2u8;
        if self.turn != player {
            // if not AI's turn, do nothing
            return 254;
        }
        let (best_idx, _best_score) = self.best_move_for(player);
        match best_idx {
            Some(i) => {
                let _ = self.play(i as u8);
                i as u8
            },
            None => {
                // pass
                let _ = self.play(255);
                255
            }
        }
    }

    /// returns list of legal moves as Vec<usize>
    pub fn legal_moves(&self, player: u8) -> Vec<usize> {
        let mut moves = Vec::new();
        for pos in 0..64 {
            if self.board[pos] != 0 { continue; }
            let flips = self.collect_flips(pos, player);
            if !flips.is_empty() {
                moves.push(pos);
            }
        }
        moves
    }

    /// helper: returns index counts for black/white
    pub fn counts(&self) -> Vec<u8> {
        let mut b=0; let mut w=0;
        for &c in &self.board {
            if c==1 { b+=1; }
            if c==2 { w+=1; }
        }
        vec![b,w]
    }

    /// Reset
    pub fn reset(&mut self) {
        *self = Game::new();
    }

    // ---------- internal helpers ----------

    fn best_move_for(&self, player: u8) -> (Option<usize>, i32) {
        let mut best_score = i32::MIN;
        let mut best_idx: Option<usize> = None;
        for pos in 0..64 {
            if self.board[pos] != 0 { continue; }
            let flips = self.collect_flips(pos, player);
            if flips.is_empty() { continue; }
            let flip_count = flips.len() as i32;
            let score = WEIGHTS[pos] + flip_count * 8; // weight + flips factor
            if score > best_score {
                best_score = score;
                best_idx = Some(pos);
            }
        }
        (best_idx, best_score)
    }

    fn collect_flips(&self, pos: usize, player: u8) -> Vec<usize> {
        let mut res = Vec::new();
        let row = (pos / 8) as i32;
        let col = (pos % 8) as i32;
        let opponent = 3 - player;
        for (dr, dc) in &DIRS {
            let mut r = row + dr;
            let mut c = col + dc;
            let mut flips_line = Vec::new();
            let mut found_opponent = false;
            while r >= 0 && r < 8 && c >= 0 && c < 8 {
                let idx = (r * 8 + c) as usize;
                let v = self.board[idx];
                if v == opponent {
                    found_opponent = true;
                    flips_line.push(idx);
                } else if v == player {
                    if found_opponent {
                        // this direction yields flips
                        res.extend(flips_line.iter());
                    }
                    break;
                } else {
                    // empty
                    break;
                }
                r += dr; c += dc;
            }
        }
        res
    }
}
