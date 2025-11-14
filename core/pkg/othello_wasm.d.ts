/* tslint:disable */
/* eslint-disable */
export class Game {
  free(): void;
  [Symbol.dispose](): void;
  constructor();
  /**
   * returns a copy of the board as a JS Uint8Array
   */
  get_board(): Uint8Array;
  /**
   * returns current turn: 1 or 2
   */
  get_turn(): number;
  /**
   * try to play at index (0..63) for current player.
   * returns true if move applied (legal). If legal and applied, toggles turn.
   * if idx == 255 -> pass
   */
  play(idx: number): boolean;
  /**
   * AI move for white (2). This chooses the move that maximizes evaluation:
   * eval = positional weight + 8 * flipped_count
   * It's a greedy best-move (局所評価の最善手).
   * returns chosen index (0..63) or 255 for pass.
   */
  ai_move(): number;
  /**
   * returns list of legal moves as Vec<usize>
   */
  legal_moves(player: number): Uint32Array;
  /**
   * helper: returns index counts for black/white
   */
  counts(): Uint8Array;
  /**
   * Reset
   */
  reset(): void;
}

export type InitInput = RequestInfo | URL | Response | BufferSource | WebAssembly.Module;

export interface InitOutput {
  readonly memory: WebAssembly.Memory;
  readonly __wbg_game_free: (a: number, b: number) => void;
  readonly game_new: () => number;
  readonly game_get_board: (a: number) => [number, number];
  readonly game_get_turn: (a: number) => number;
  readonly game_play: (a: number, b: number) => number;
  readonly game_ai_move: (a: number) => number;
  readonly game_legal_moves: (a: number, b: number) => [number, number];
  readonly game_counts: (a: number) => [number, number];
  readonly game_reset: (a: number) => void;
  readonly __wbindgen_externrefs: WebAssembly.Table;
  readonly __wbindgen_free: (a: number, b: number, c: number) => void;
  readonly __wbindgen_start: () => void;
}

export type SyncInitInput = BufferSource | WebAssembly.Module;
/**
* Instantiates the given `module`, which can either be bytes or
* a precompiled `WebAssembly.Module`.
*
* @param {{ module: SyncInitInput }} module - Passing `SyncInitInput` directly is deprecated.
*
* @returns {InitOutput}
*/
export function initSync(module: { module: SyncInitInput } | SyncInitInput): InitOutput;

/**
* If `module_or_path` is {RequestInfo} or {URL}, makes a request and
* for everything else, calls `WebAssembly.instantiate` directly.
*
* @param {{ module_or_path: InitInput | Promise<InitInput> }} module_or_path - Passing `InitInput` directly is deprecated.
*
* @returns {Promise<InitOutput>}
*/
export default function __wbg_init (module_or_path?: { module_or_path: InitInput | Promise<InitInput> } | InitInput | Promise<InitInput>): Promise<InitOutput>;
