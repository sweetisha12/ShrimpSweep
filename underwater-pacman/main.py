import asyncio
import json
import random
import time

from game_content_v2 import LEVELS, LEVEL_MESSAGES, MAZES, MAZE_META, QUESTIONS
from settings_v2 import (
    LEADERBOARD_ENDPOINT,
    LEADERBOARD_LIMIT,
    USE_LOCAL_LEADERBOARD_FALLBACK,
)
from js import document, fetch, localStorage, setInterval, clearInterval, console
from pyodide.ffi import create_proxy, to_js


CELL_WALL = "#"
CELL_PATH = "."
PLANKTON_DOT = "•"
BOMB = "💣"
WORM = "🪱"
SHRIMP = "🦐"
SQUID = "🦑"
COD = "🐟"


class UnderwaterPacmanGame:
    def __init__(self):
        self.board_el = document.getElementById("board")
        self.score_el = document.getElementById("score-label")
        self.high_score_el = document.getElementById("high-score-label")
        self.level_el = document.getElementById("level-label")
        self.lives_el = document.getElementById("lives-label")
        self.lives_banner_el = document.getElementById("lives-banner")
        self.hud_level_el = document.getElementById("hud-level-label")
        self.hud_score_line_el = document.getElementById("hud-score-line")
        self.status_el = document.getElementById("status-text")
        self.message_el = document.getElementById("message-card")
        self.question_overlay_el = document.getElementById("question-overlay")
        self.question_prompt_el = document.getElementById("question-prompt")
        self.question_difficulty_el = document.getElementById("question-difficulty")
        self.question_progress_el = document.getElementById("question-progress")
        self.answer_options_el = document.getElementById("answer-options")
        self.name_el = document.getElementById("player-name")
        self.start_level_el = document.getElementById("start-level")
        self.fastest_list_el = document.getElementById("fastest-list")
        self.claws_list_el = document.getElementById("claws-list")
        self.survivor_list_el = document.getElementById("survivor-list")
        self.fastest_best_el = document.getElementById("fastest-best")
        self.claws_best_el = document.getElementById("claws-best")
        self.survivor_best_el = document.getElementById("survivor-best")
        self.catch_of_day_el = document.getElementById("catch-of-day")
        self.catch_of_day_body_el = document.getElementById("catch-of-day-body")
        self.leaderboard_note_el = document.getElementById("leaderboard-note")
        self.seed_leaderboard_btn = document.getElementById("seed-leaderboard-btn")
        self.start_btn = document.getElementById("start-btn")
        self.restart_btn = document.getElementById("restart-btn")

        self.high_score = int(localStorage.getItem("shrimp-high-score") or 0)
        self.leaderboard_key = "shrimpSweepLeaderboard"
        self.legacy_leaderboard_key = "shrimp-local-leaderboard"

        self.level_index = 0
        self.start_level_index = 0
        self.score = 0
        self.lives = 3
        self.game_active = False
        self.awaiting_questions = True
        self.question_streak = 0
        self.current_question = None
        self.used_question_indices = {key: [] for key in QUESTIONS}
        self.player_name = ""
        self.debug_bypass_questions = False

        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.last_nonzero_direction = (1, 0)
        self.player_pos = (1, 1)
        self.ghosts = []
        self.plankton = set()
        self.bombs = set()
        self.worms = set()
        self.path_cells = []
        self.ghost_pen_cells = set()
        self.no_spawn_cells = set()
        self.level_points = 0
        self.pellets_collected = 0

        self.player_interval = None
        self.ghost_interval = None
        self.slow_effect_version = 0
        self.pending_resume_after_question = False
        self.pending_resume_message = ""
        self.single_question_mode = False
        self.player_speed_multiplier = 1.0
        self.enemy_speed_multiplier = 1.0
        self.effect_mode = "normal"
        self.level_state_token = 0
        self.release_task_token = 0
        self.ghost_mode = "scatter"
        self.ghost_mode_elapsed_ms = 0
        self.spawn_protection_token = 0
        self.level_transition_token = 0
        self.last_input_at = time.monotonic()
        self.questions_answered = 0
        self.questions_correct = 0
        self.run_started_at = None
        self.best_zone_reached = 1
        self.leaderboard_filter = "all"

        initial_maze = MAZES[LEVELS[self.level_index]["maze_key"]]
        self.base_grid = [list(row) for row in initial_maze]
        self.height = len(self.base_grid)
        self.width = len(self.base_grid[0])
        self.cell_els = []

        self.proxies = []
        self.build_board()
        self.apply_level_theme()
        self.update_scoreboard()
        self.render_message("Custom messages after each level will appear here.")
        self.bind_controls()
        self.render_question_waiting()
        self.render_board()
        self.load_leaderboard()

    def build_board(self):
        self.board_el.innerHTML = ""
        self.board_el.style.gridTemplateColumns = f"repeat({self.width}, 1fr)"
        self.cell_els = []
        for _y in range(self.height):
            row_cells = []
            for _x in range(self.width):
                cell = document.createElement("div")
                cell.className = "cell water"
                self.board_el.appendChild(cell)
                row_cells.append(cell)
            self.cell_els.append(row_cells)

    def load_level_maze(self):
        maze_key = LEVELS[self.level_index]["maze_key"]
        maze_rows = MAZES[maze_key]
        self.base_grid = [list(row) for row in maze_rows]
        self.height = len(self.base_grid)
        self.width = len(self.base_grid[0])
        self.build_board()
        self.apply_level_theme()

    def apply_level_theme(self):
        for index in range(1, 4):
            self.board_el.classList.remove(f"zone-{index}")
        zone_number = self.level_index + 1
        current_level = LEVELS[self.level_index]["name"]
        background_color = self.get_background_color(current_level)
        self.board_el.classList.add(f"zone-{zone_number}")
        self.board_el.style.backgroundColor = background_color
        self.board_el.style.backgroundImage = "none"
        console.log("Current Level:", current_level)

    def get_background_color(self, level):
        if level == "pH-resh and cool":
            return "#7ec8e3"
        if level == "CO₂ncerning pH":
            return "#3a7ca5"
        if level == "Naked and Acidi-fied":
            return "#0b1e2d"
        return "#7ec8e3"

    def bind_controls(self):
        start_proxy = create_proxy(lambda event: self.start_run())
        restart_proxy = create_proxy(lambda event: self.reset_to_easy(manual=True))
        key_proxy = create_proxy(self.on_keydown)
        self.start_btn.addEventListener("click", start_proxy)
        self.restart_btn.addEventListener("click", restart_proxy)
        document.addEventListener("keydown", key_proxy)
        self.proxies.extend([start_proxy, restart_proxy, key_proxy])
        if self.seed_leaderboard_btn:
            seed_proxy = create_proxy(lambda event: self.add_test_leaderboard_data())
            self.seed_leaderboard_btn.addEventListener("click", seed_proxy)
            self.proxies.append(seed_proxy)

        buttons = document.querySelectorAll(".mobile-controls button")
        for button in buttons:
            direction = button.getAttribute("data-dir")
            proxy = create_proxy(lambda event, d=direction: self.set_direction(d))
            button.addEventListener("click", proxy)
            self.proxies.append(proxy)

        filter_buttons = document.querySelectorAll(".leaderboard-filter")
        for button in filter_buttons:
            filter_value = button.getAttribute("data-filter")
            proxy = create_proxy(lambda event, f=filter_value: self.set_leaderboard_filter(f))
            button.addEventListener("click", proxy)
            self.proxies.append(proxy)

    def set_leaderboard_filter(self, filter_value):
        self.leaderboard_filter = filter_value
        for button in document.querySelectorAll(".leaderboard-filter"):
            button.classList.remove("active")
            if button.getAttribute("data-filter") == filter_value:
                button.classList.add("active")
        self.load_leaderboard()

    def on_keydown(self, event):
        key = event.key
        if key in ("ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"):
            event.preventDefault()
        if key == "ArrowUp":
            self.set_direction("up")
        elif key == "ArrowDown":
            self.set_direction("down")
        elif key == "ArrowLeft":
            self.set_direction("left")
        elif key == "ArrowRight":
            self.set_direction("right")

    def set_direction(self, direction):
        mapping = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        self.next_direction = mapping[direction]
        self.last_input_at = time.monotonic()

    def start_run(self):
        name = self.name_el.value.strip()
        if not name:
            self.set_status("Enter a player name before starting the run.")
            return
        try:
            self.start_level_index = int(self.start_level_el.value or "0")
        except Exception:
            self.start_level_index = 0
        self.start_level_index = min(max(self.start_level_index, 0), len(LEVELS) - 1)
        self.player_name = name
        self.debug_bypass_questions = name.lower() == "test"
        self.score = 0
        self.lives = 3
        self.level_index = self.start_level_index
        self.question_streak = 0
        self.questions_answered = 0
        self.questions_correct = 0
        self.run_started_at = time.monotonic()
        self.best_zone_reached = self.level_index + 1
        self.used_question_indices = {key: [] for key in QUESTIONS}
        self.stop_loops()
        self.update_scoreboard()
        if self.debug_bypass_questions:
            self.set_status("Test mode active. Question gates are bypassed.")
            self.launch_level()
            return
        self.set_status(f"{LEVELS[self.level_index]['name']} question gate active. Answer 3 in a row to enter.")
        self.ask_question_for_current_level()

    def stop_loops(self):
        if self.player_interval is not None:
            clearInterval(self.player_interval)
            self.player_interval = None
        if self.ghost_interval is not None:
            clearInterval(self.ghost_interval)
            self.ghost_interval = None

    def reset_to_easy(self, manual=False):
        self.stop_loops()
        self.game_active = False
        self.awaiting_questions = True
        self.level_index = 0
        self.lives = 3
        self.score = 0
        self.question_streak = 0
        self.slow_effect_version += 1
        self.single_question_mode = False
        self.pending_resume_after_question = False
        self.pending_resume_message = ""
        self.current_question = None
        self.debug_bypass_questions = False
        self.used_question_indices = {key: [] for key in QUESTIONS}
        self.player_pos = (1, 1)
        self.ghosts = []
        self.plankton = set()
        self.bombs = set()
        self.worms = set()
        self.path_cells = []
        self.level_points = 0
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.last_nonzero_direction = (1, 0)
        self.last_input_at = time.monotonic()
        self.board_el.classList.remove("slow-mode")
        self.board_el.parentElement.classList.remove("slow-mode")
        self.player_speed_multiplier = 1.0
        self.enemy_speed_multiplier = 1.0
        self.effect_mode = "normal"
        self.level_state_token += 1
        self.release_task_token += 1
        self.load_level_maze()
        self.update_scoreboard()
        self.render_board()
        self.render_question_waiting()
        if manual:
            self.set_status("Run reset. Press start to take the easy question gate again.")
            self.render_message("The reef has reset. Your next dive begins from easy.")
        else:
            self.set_status("You were sent back to easy. Press start to begin again.")
            self.render_message("A wrong answer or defeat reset the dive. The reef sends everyone back to easy.")

    def ask_question_for_current_level(self):
        if self.debug_bypass_questions:
            self.question_streak = 0
            if self.single_question_mode or self.pending_resume_after_question:
                self.single_question_mode = False
                self.resume_after_caught_question()
            else:
                self.launch_level()
            return
        self.awaiting_questions = True
        self.game_active = False
        self.stop_loops()
        self.toggle_question_overlay(True)
        difficulty = LEVELS[self.level_index]["difficulty_key"]
        pool = QUESTIONS[difficulty]
        if len(self.used_question_indices[difficulty]) >= len(pool):
            self.used_question_indices[difficulty] = []
        available = [idx for idx in range(len(pool)) if idx not in self.used_question_indices[difficulty]]
        selected_index = random.choice(available)
        self.used_question_indices[difficulty].append(selected_index)
        self.current_question = pool[selected_index]
        self.question_difficulty_el.innerText = difficulty
        self.question_prompt_el.innerText = self.current_question["prompt"]
        self.question_progress_el.innerText = f"Streak: {self.question_streak} / 3"
        if self.single_question_mode:
            self.question_progress_el.innerText = "Recovery question: 1 correct answer needed"
        self.answer_options_el.innerHTML = ""

        for option in self.current_question["options"]:
            button = document.createElement("button")
            button.className = "answer-btn"
            button.innerText = option
            proxy = create_proxy(lambda event, guess=option: self.submit_answer(guess))
            button.addEventListener("click", proxy)
            self.proxies.append(proxy)
            self.answer_options_el.appendChild(button)

    def submit_answer(self, guess):
        if not self.current_question:
            return
        self.questions_answered += 1
        if guess == self.current_question["answer"]:
            self.questions_correct += 1
        self.save_progress_snapshot()
        self.load_leaderboard()
        if guess == self.current_question["answer"]:
            if self.single_question_mode:
                self.single_question_mode = False
                self.resume_after_caught_question()
                return
            self.question_streak += 1
            if self.question_streak >= 3:
                self.question_streak = 0
                if self.pending_resume_after_question:
                    self.resume_after_caught_question()
                else:
                    self.launch_level()
            else:
                remaining = 3 - self.question_streak
                self.set_status(
                    f"Correct. {remaining} more correct answer(s) in a row needed for {LEVELS[self.level_index]['name']}."
                )
                self.ask_question_for_current_level()
        else:
            if self.single_question_mode:
                self.single_question_mode = False
                self.render_question_waiting("Wrong answer. The reef resets you to easy.")
                self.render_message("Missing the recovery question sends the run back to easy.")
                self.reset_to_easy(manual=False)
                return
            self.render_question_waiting("Wrong answer. The reef resets you to easy.")
            self.render_message("Three in a row is required. Missing one restarts the full run from easy.")
            self.reset_to_easy(manual=False)

    def render_question_waiting(self, prompt="Press start to begin the easy question gate."):
        self.question_difficulty_el.innerText = "Waiting"
        self.question_prompt_el.innerText = prompt
        self.question_progress_el.innerText = "Streak: 0 / 3"
        self.answer_options_el.innerHTML = ""
        self.toggle_question_overlay(True)

    def launch_level(self):
        self.awaiting_questions = False
        self.game_active = True
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.slow_effect_version += 1
        self.pending_resume_after_question = False
        self.pending_resume_message = ""
        self.load_level_maze()
        self.setup_level_state()
        config = LEVELS[self.level_index]
        self.level_el.innerText = config["name"]
        self.best_zone_reached = max(self.best_zone_reached, self.level_index + 1)
        self.set_status(
            f"{config['name']} reef live. Reach {config['target_points']} level points with plankton, carbon dioxide, and worms."
        )
        self.render_message(f"Entering {config['name']}. {LEVEL_MESSAGES.get(config['id'], '')}")
        self.toggle_question_overlay(False)
        self.render_board()
        self.start_spawn_protection()
        self.start_loops()

    def setup_level_state(self):
        config = LEVELS[self.level_index]
        maze_key = config["maze_key"]
        player_start = MAZE_META[maze_key]["player_start"]
        self.player_pos = player_start
        self.plankton = set()
        self.bombs = set()
        self.worms = set()
        self.level_points = 0
        self.pellets_collected = 0
        self.last_nonzero_direction = (1, 0)
        self.player_speed_multiplier = 1.0
        self.enemy_speed_multiplier = 1.0
        self.effect_mode = "normal"
        self.level_state_token += 1
        self.release_task_token += 1
        self.ghost_mode = "scatter"
        self.ghost_mode_elapsed_ms = 0
        path_cells = []
        ghost_home = MAZE_META[maze_key]["ghost_home"]
        if config["id"] == 3:
            pen_slots = self.find_pressure_spawn_slots(player_start, config["ghost_count"])
        else:
            pen_slots = self.find_pen_slots(ghost_home, config["ghost_count"])
        self.ghost_pen_cells = set(pen_slots)
        self.no_spawn_cells = set(pen_slots)
        plankton_candidates = []
        for y in range(self.height):
            for x in range(self.width):
                if self.base_grid[y][x] == CELL_PATH:
                    path_cells.append((x, y))
                    if (x, y) not in self.no_spawn_cells:
                        plankton_candidates.append((x, y))
        self.path_cells = path_cells
        plankton_multiplier = config.get("plankton_multiplier", 1.0)
        if 0 < plankton_multiplier < 1 and plankton_candidates:
            reduced_count = max(1, int(len(plankton_candidates) * plankton_multiplier))
            self.plankton = set(random.sample(plankton_candidates, reduced_count))
        else:
            self.plankton = set(plankton_candidates)
        self.plankton.discard(self.player_pos)

        open_cells = [cell for cell in path_cells if cell != self.player_pos and cell not in self.no_spawn_cells]
        random.shuffle(open_cells)
        for bomb_cell in open_cells[: config["bombs"]]:
            self.bombs.add(bomb_cell)
            self.plankton.discard(bomb_cell)
        remaining_cells = [cell for cell in open_cells if cell not in self.bombs]
        for worm_cell in remaining_cells[: config["worms"]]:
            self.worms.add(worm_cell)
            self.plankton.discard(worm_cell)

        self.ghosts = []
        for idx in range(config["ghost_count"]):
            spawn = pen_slots[idx]
            self.ghosts.append(
                {
                    "x": spawn[0],
                    "y": spawn[1],
                    "dir": random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)]),
                    "home": ghost_home,
                    "pen_slot": spawn,
                    "released": True,
                    "index": idx,
                }
            )

    def start_loops(self):
        self.stop_loops()
        config = LEVELS[self.level_index]
        player_proxy = create_proxy(lambda: self.tick_player())
        ghost_proxy = create_proxy(lambda: self.tick_ghosts())
        self.proxies.extend([player_proxy, ghost_proxy])
        self.player_interval = setInterval(player_proxy, max(80, int(config["shrimp_speed_ms"] * self.player_speed_multiplier)))
        self.ghost_interval = setInterval(ghost_proxy, max(80, int(config["ghost_speed_ms"] * self.enemy_speed_multiplier)))

    def find_release_target(self, home):
        home_x, home_y = home
        for offset in range(1, self.height):
            candidate_y = home_y - offset
            if self.can_move_to(home_x, candidate_y):
                return (home_x, candidate_y)
        return home

    def find_pen_slots(self, home, count):
        path_slots = []
        for y in range(self.height):
            for x in range(self.width):
                if self.base_grid[y][x] != CELL_PATH:
                    continue
                distance = abs(x - home[0]) + abs(y - home[1])
                path_slots.append((distance, y, x))
        path_slots.sort()
        slots = []
        for _, y, x in path_slots:
            if (x, y) not in slots:
                slots.append((x, y))
            if len(slots) == count:
                break
        return slots

    def find_pressure_spawn_slots(self, player_start, count):
        candidate_slots = []
        for y in range(self.height):
            for x in range(self.width):
                if self.base_grid[y][x] != CELL_PATH:
                    continue
                if (x, y) == player_start:
                    continue
                distance = abs(x - player_start[0]) + abs(y - player_start[1])
                if distance < 4:
                    continue
                candidate_slots.append((distance, abs(y - player_start[1]), y, x))
        candidate_slots.sort()
        slots = []
        for _, _, y, x in candidate_slots:
            cell = (x, y)
            if any(abs(x - slot_x) + abs(y - slot_y) < 2 for slot_x, slot_y in slots):
                continue
            slots.append(cell)
            if len(slots) == count:
                break
        if len(slots) < count:
            return self.find_pen_slots(player_start, count)
        return slots

    def can_move_to(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height and self.base_grid[y][x] != CELL_WALL

    def move_position(self, pos, direction):
        nx = pos[0] + direction[0]
        ny = pos[1] + direction[1]
        if self.can_move_to(nx, ny):
            return (nx, ny)
        return pos

    def tick_player(self):
        if not self.game_active:
            return
        if time.monotonic() - self.last_input_at > 8:
            self.direction = (0, 0)
            return
        if self.next_direction != (0, 0):
            candidate = self.move_position(self.player_pos, self.next_direction)
            if candidate != self.player_pos:
                self.direction = self.next_direction
        if self.direction != (0, 0):
            self.player_pos = self.move_position(self.player_pos, self.direction)
            self.last_nonzero_direction = self.direction
        self.collect_items()
        self.check_collisions()
        self.render_board()
        self.check_level_complete()

    def tick_ghosts(self):
        if not self.game_active:
            return
        if time.monotonic() - self.last_input_at > 8:
            self.set_status(f"{LEVELS[self.level_index]['name']} paused while shrimp is idle.")
            return
        self.update_ghost_mode()
        current_positions = {(ghost["x"], ghost["y"]) for ghost in self.ghosts if ghost["released"]}
        next_positions = set()
        for ghost in self.ghosts:
            blocked_positions = (current_positions - {(ghost["x"], ghost["y"])}) | next_positions
            chosen = self.choose_predator_step(ghost, blocked_positions)
            if not chosen:
                next_positions.add((ghost["x"], ghost["y"]))
                continue
            ghost["dir"] = chosen[2]
            ghost["x"] = chosen[3]
            ghost["y"] = chosen[4]
            next_positions.add((ghost["x"], ghost["y"]))
        self.check_collisions()
        self.render_board()

    def update_ghost_mode(self):
        config = LEVELS[self.level_index]
        tick_ms = max(80, int(config["ghost_speed_ms"] * self.enemy_speed_multiplier))
        self.ghost_mode_elapsed_ms += tick_ms
        threshold = 7000 if self.ghost_mode == "scatter" else 20000
        if self.ghost_mode_elapsed_ms >= threshold:
            self.ghost_mode = "chase" if self.ghost_mode == "scatter" else "scatter"
            self.ghost_mode_elapsed_ms = 0

    def schedule_ghost_releases(self):
        return

    def release_ghost(self, ghost):
        ghost["released"] = True

    def choose_predator_step(self, ghost, blocked_positions):
        # Classic Pac-Man style priority at ties: up, left, down, right.
        direction_order = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        reverse_dir = (-ghost["dir"][0], -ghost["dir"][1])
        frightened = self.effect_mode == "boost"
        options = []
        for order_index, direction in enumerate(direction_order):
            nx = ghost["x"] + direction[0]
            ny = ghost["y"] + direction[1]
            if not self.can_move_to(nx, ny) or (nx, ny) in blocked_positions:
                continue
            if not frightened and ghost["dir"] != (0, 0) and direction == reverse_dir:
                continue
            options.append((order_index, direction, nx, ny))

        if not options and ghost["dir"] != (0, 0):
            nx = ghost["x"] + reverse_dir[0]
            ny = ghost["y"] + reverse_dir[1]
            if self.can_move_to(nx, ny) and (nx, ny) not in blocked_positions:
                options.append((4, reverse_dir, nx, ny))

        if not options:
            return None

        if frightened:
            choice = random.choice(options)
            return (0, 0, choice[1], choice[2], choice[3])

        target_x, target_y = self.get_predator_target(ghost)
        ranked = []
        for order_index, direction, nx, ny in options:
            distance = ((nx - target_x) ** 2 + (ny - target_y) ** 2) ** 0.5
            ranked.append((distance, order_index, direction, nx, ny))
        ranked.sort(key=lambda item: (item[0], item[1]))
        return ranked[0]

    def get_predator_target(self, ghost):
        if self.effect_mode == "boost":
            return ghost["home"]

        if self.ghost_mode == "scatter" and self.effect_mode != "danger":
            scatter_targets = [
                (self.width - 2, 1),
                (1, 1),
                (self.width - 2, self.height - 2),
                (1, self.height - 2),
            ]
            return scatter_targets[ghost["index"] % len(scatter_targets)]
        pac_dir = self.last_nonzero_direction if self.last_nonzero_direction != (0, 0) else (1, 0)
        pac_x, pac_y = self.player_pos
        blinky = self.ghosts[0] if self.ghosts else None

        # Blinky
        if ghost["index"] == 0 or self.effect_mode == "danger":
            return (pac_x, pac_y)

        # Pinky: 4 tiles ahead of Pac-Man.
        if ghost["index"] == 1:
            return self.clamp_target((pac_x + pac_dir[0] * 4, pac_y + pac_dir[1] * 4))

        # Inky: vector from Blinky to 2 tiles ahead of Pac-Man, doubled.
        if ghost["index"] == 2 and blinky is not None:
            ahead = (pac_x + pac_dir[0] * 2, pac_y + pac_dir[1] * 2)
            vector_x = ahead[0] - blinky["x"]
            vector_y = ahead[1] - blinky["y"]
            return self.clamp_target((ahead[0] + vector_x, ahead[1] + vector_y))

        # Clyde: chase when far, retreat when close.
        distance_to_player = abs(ghost["x"] - pac_x) + abs(ghost["y"] - pac_y)
        if distance_to_player <= 4:
            return (1, self.height - 2)
        return (pac_x, pac_y)

    def clamp_target(self, target):
        return (
            min(max(target[0], 1), self.width - 2),
            min(max(target[1], 1), self.height - 2),
        )

    def collect_items(self):
        if self.player_pos in self.plankton:
            self.plankton.remove(self.player_pos)
            self.score += 10
            self.level_points += 10
            self.pellets_collected += 1
            self.update_high_score()
            self.schedule_respawn("plankton", 4.5)
        if self.player_pos in self.bombs:
            self.bombs.remove(self.player_pos)
            self.score += 75
            self.level_points += 75
            self.update_high_score()
            self.schedule_respawn("bomb", 7.5, exclude={self.player_pos})
            self.apply_carbon_dioxide_effect()
        if self.player_pos in self.worms:
            self.worms.remove(self.player_pos)
            self.score += 45
            self.level_points += 45
            self.update_high_score()
            self.schedule_respawn("worm", 8.5, exclude={self.player_pos})
            self.apply_worm_effect()
        self.update_scoreboard()

    def apply_carbon_dioxide_effect(self):
        self.slow_effect_version += 1
        effect_version = self.slow_effect_version
        self.effect_mode = "danger"
        self.player_speed_multiplier = 1.15
        self.enemy_speed_multiplier = 0.55
        self.set_status("Carbon dioxide collected. The squid turn into fast cod and the reef flips.")
        self.board_el.classList.add("slow-mode")
        self.board_el.parentElement.classList.add("slow-mode")
        self.start_loops()

        async def _restore():
            await asyncio.sleep(60)
            if (
                self.game_active
                and not self.awaiting_questions
                and effect_version == self.slow_effect_version
            ):
                self.clear_effect_mode()

        asyncio.create_task(_restore())

    def apply_worm_effect(self):
        self.slow_effect_version += 1
        effect_version = self.slow_effect_version
        self.effect_mode = "boost"
        self.player_speed_multiplier = 0.72
        self.enemy_speed_multiplier = 1.5
        self.set_status("Worm collected. The shrimp speeds up while the predators slow down.")
        self.board_el.classList.remove("slow-mode")
        self.board_el.parentElement.classList.remove("slow-mode")
        self.start_loops()

        async def _restore():
            await asyncio.sleep(4.5)
            if (
                self.game_active
                and not self.awaiting_questions
                and effect_version == self.slow_effect_version
            ):
                self.clear_effect_mode()

        asyncio.create_task(_restore())

    def clear_effect_mode(self):
        self.effect_mode = "normal"
        self.player_speed_multiplier = 1.0
        self.enemy_speed_multiplier = 1.0
        self.board_el.classList.remove("slow-mode")
        self.board_el.parentElement.classList.remove("slow-mode")
        self.start_loops()
        self.set_status(
            f"{LEVELS[self.level_index]['name']} reef live. Reach {LEVELS[self.level_index]['target_points']} level points with plankton, carbon dioxide, and worms."
        )

    def schedule_respawn(self, item_type, delay_seconds, exclude=None):
        level_token = self.level_state_token
        excluded_cells = set(exclude or set())

        async def _respawn():
            await asyncio.sleep(delay_seconds)
            if level_token != self.level_state_token:
                return
            spawn = self.find_spawn_cell(excluded_cells)
            if not spawn:
                return
            if item_type == "plankton":
                self.plankton.add(spawn)
            elif item_type == "bomb":
                self.bombs.add(spawn)
                self.plankton.discard(spawn)
            elif item_type == "worm":
                self.worms.add(spawn)
                self.plankton.discard(spawn)
            self.render_board()

        asyncio.create_task(_respawn())

    def find_spawn_cell(self, excluded_cells=None):
        blocked = set(excluded_cells or set())
        blocked.add(self.player_pos)
        blocked |= self.no_spawn_cells
        for ghost in self.ghosts:
            blocked.add((ghost["x"], ghost["y"]))
        blocked |= self.plankton
        blocked |= self.bombs
        blocked |= self.worms
        choices = [cell for cell in self.path_cells if cell not in blocked]
        if not choices:
            return None
        return random.choice(choices)

    def check_collisions(self):
        if self.board_el.classList.contains("spawn-safe"):
            return
        for ghost in self.ghosts:
            if (ghost["x"], ghost["y"]) == self.player_pos:
                self.lives -= 1
                self.update_scoreboard()
                if self.lives <= 0:
                    self.end_run("The squid closed in. Your run is over.")
                else:
                    self.handle_caught_by_squid()
                break

    def handle_caught_by_squid(self):
        self.stop_loops()
        maze_key = LEVELS[self.level_index]["maze_key"]
        self.player_pos = MAZE_META[maze_key]["player_start"]
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.question_streak = 0
        self.board_el.classList.remove("slow-mode")
        self.board_el.parentElement.classList.remove("slow-mode")
        self.slow_effect_version += 1
        self.effect_mode = "normal"
        self.player_speed_multiplier = 1.0
        self.enemy_speed_multiplier = 1.0
        self.release_task_token += 1
        self.ghost_mode = "scatter"
        self.ghost_mode_elapsed_ms = 0
        if self.debug_bypass_questions:
            self.game_active = True
            self.awaiting_questions = False
            self.pending_resume_after_question = False
            self.pending_resume_message = ""
            self.single_question_mode = False
            self.toggle_question_overlay(False)
            self.set_status(f"A squid caught you. Respawning shrimp. {self.lives} lives remaining.")
            self.render_message("The shrimp was caught and respawned at the maze start.")
            self.render_board()
            self.start_spawn_protection()
            self.start_loops()
            return

        self.game_active = False
        self.awaiting_questions = True
        self.pending_resume_after_question = True
        self.pending_resume_message = f"You survived the squid. {self.lives} lives remaining."
        self.single_question_mode = True
        self.set_status("A squid caught you. Answer 1 question correctly to keep playing.")
        self.render_message("A squid caught the shrimp. Answer the recovery question to reopen the maze.")
        self.ask_question_for_current_level()

    def resume_after_caught_question(self):
        self.awaiting_questions = False
        self.game_active = True
        self.pending_resume_after_question = False
        self.single_question_mode = False
        self.toggle_question_overlay(False)
        self.set_status(self.pending_resume_message or "Back in the maze.")
        self.pending_resume_message = ""
        self.render_board()
        self.start_spawn_protection()
        self.start_loops()

    def start_spawn_protection(self):
        self.spawn_protection_token += 1
        protection_token = self.spawn_protection_token
        self.board_el.classList.add("spawn-safe")

        async def _clear():
            await asyncio.sleep(2.2)
            if protection_token == self.spawn_protection_token:
                self.board_el.classList.remove("spawn-safe")

        asyncio.create_task(_clear())

    def check_level_complete(self):
        if self.level_points >= LEVELS[self.level_index]["target_points"]:
            self.stop_loops()
            self.level_state_token += 1
            self.level_transition_token += 1
            current_level_id = LEVELS[self.level_index]["id"]
            self.render_message(LEVEL_MESSAGES.get(current_level_id, "Level clear."))
            if self.level_index == len(LEVELS) - 1:
                self.end_run("You cleared all 3 underwater levels and conquered the reef!")
                return
            self.level_index += 1
            self.update_scoreboard()
            next_name = LEVELS[self.level_index]["name"]
            self.set_status(f"Level complete. Preparing {next_name}.")
            self.show_level_transition(next_name, LEVEL_MESSAGES.get(current_level_id, ""))

    def show_level_transition(self, next_name, flavor_text):
        transition_token = self.level_transition_token
        self.game_active = False
        self.awaiting_questions = False
        self.toggle_question_overlay(True)
        self.question_difficulty_el.innerText = "Level Clear"
        self.question_prompt_el.innerText = f"Next stop: {next_name}"
        self.question_progress_el.innerText = flavor_text or "Catch your breath before the next dive."
        self.answer_options_el.innerHTML = ""
        console.log("Level transition started")

        async def _advance():
            await asyncio.sleep(2.5)
            if transition_token != self.level_transition_token:
                return
            console.log("Starting next level:", next_name)
            self.start_next_level_after_transition()

        asyncio.create_task(_advance())

    def start_next_level_after_transition(self):
        self.toggle_question_overlay(False)
        self.pending_resume_after_question = False
        self.pending_resume_message = ""
        self.single_question_mode = False
        self.current_question = None
        self.load_level_maze()
        self.setup_level_state()
        self.game_active = True
        self.awaiting_questions = False
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        config = LEVELS[self.level_index]
        self.level_el.innerText = config["name"]
        self.hud_level_el.innerText = config["name"]
        self.set_status(
            f"{config['name']} reef live. Reach {config['target_points']} level points with plankton, carbon dioxide, and worms."
        )
        self.render_message(f"Entering {config['name']}. {LEVEL_MESSAGES.get(config['id'], '')}")
        self.render_board()
        self.start_spawn_protection()
        self.start_loops()

    def end_run(self, message):
        self.stop_loops()
        self.game_active = False
        self.awaiting_questions = True
        self.pending_resume_after_question = False
        self.pending_resume_message = ""
        self.board_el.classList.remove("slow-mode")
        self.board_el.parentElement.classList.remove("slow-mode")
        self.effect_mode = "normal"
        self.player_speed_multiplier = 1.0
        self.enemy_speed_multiplier = 1.0
        self.level_state_token += 1
        self.release_task_token += 1
        self.ghost_mode = "scatter"
        self.ghost_mode_elapsed_ms = 0
        self.set_status(message)
        self.render_message(message)
        self.render_question_waiting("Run complete. Press start to challenge the reef again.")
        self.toggle_question_overlay(True)
        self.submit_score()

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            localStorage.setItem("shrimp-high-score", str(self.high_score))
        self.update_scoreboard()

    def update_scoreboard(self):
        self.score_el.innerText = str(self.score)
        self.high_score_el.innerText = str(self.high_score)
        self.level_el.innerText = LEVELS[self.level_index]["name"]
        shrimp_icons = " ".join([SHRIMP] * self.lives) if self.lives > 0 else "0"
        self.lives_el.innerText = shrimp_icons
        self.lives_banner_el.innerText = shrimp_icons
        self.hud_level_el.innerText = LEVELS[self.level_index]["name"]
        self.hud_score_line_el.innerText = f"{self.score} | High {self.high_score}"

    def set_status(self, message):
        self.status_el.innerText = message

    def render_message(self, message):
        self.message_el.innerHTML = ""
        paragraph = document.createElement("p")
        paragraph.innerText = message
        self.message_el.appendChild(paragraph)

    def toggle_question_overlay(self, visible):
        if visible:
            self.question_overlay_el.classList.remove("hidden")
        else:
            self.question_overlay_el.classList.add("hidden")

    def render_board(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.cell_els[y][x]
                cell.innerText = ""
                cell.style.cssText = ""
                if self.base_grid[y][x] == CELL_WALL:
                    cell.className = "cell wall"
                    cell.style.cssText = self.wall_inline_style(x, y)
                else:
                    cell.className = "cell water"
                    if (x, y) in self.plankton:
                        cell.innerText = PLANKTON_DOT
                        cell.classList.add("pellet")
                    elif (x, y) in self.bombs:
                        cell.innerText = BOMB
                        cell.classList.add("bomb", "glow")
        px, py = self.player_pos
        self.cell_els[py][px].innerHTML = f'<span class="actor-emoji">{SHRIMP}</span>'
        self.cell_els[py][px].classList.add("actor", "glow")
        for ghost in self.ghosts:
            cell = self.cell_els[ghost["y"]][ghost["x"]]
            if self.effect_mode == "danger":
                cell.innerHTML = f'<span class="actor-emoji fish-actor">{COD}</span>'
                cell.classList.add("actor")
            else:
                squid_classes = ["squid-yellow", "squid-pink", "squid-cyan", "squid-orange"]
                extra_class = squid_classes[ghost["index"] % len(squid_classes)]
                cell.innerHTML = f'<span class="actor-emoji {extra_class}">{SQUID}</span>'
                cell.classList.add("actor")
        for worm_x, worm_y in self.worms:
            worm_cell = self.cell_els[worm_y][worm_x]
            worm_cell.innerText = WORM
            worm_cell.classList.add("bomb", "glow")

    def wall_inline_style(self, x, y):
        up = y > 0 and self.base_grid[y - 1][x] == CELL_WALL
        down = y < self.height - 1 and self.base_grid[y + 1][x] == CELL_WALL
        left = x > 0 and self.base_grid[y][x - 1] == CELL_WALL
        right = x < self.width - 1 and self.base_grid[y][x + 1] == CELL_WALL
        top = "0px" if up else "3px"
        right_inset = "0px" if right else "3px"
        bottom = "0px" if down else "3px"
        left_inset = "0px" if left else "3px"
        radius_tl = "8px" if not up and not left else "0"
        radius_tr = "8px" if not up and not right else "0"
        radius_br = "8px" if not down and not right else "0"
        radius_bl = "8px" if not down and not left else "0"
        return (
            "background: linear-gradient(180deg, #2b64ff, #1237ca);"
            f"clip-path: inset({top} {right_inset} {bottom} {left_inset} round {radius_tl} {radius_tr} {radius_br} {radius_bl});"
        )

    def local_leaderboard(self):
        raw = localStorage.getItem(self.leaderboard_key)
        if not raw:
            raw = localStorage.getItem(self.legacy_leaderboard_key)
            if raw:
                try:
                    migrated_entries = [self.normalize_saved_entry(entry) for entry in json.loads(raw)]
                    self.save_local_leaderboard(migrated_entries)
                    localStorage.removeItem(self.legacy_leaderboard_key)
                    return migrated_entries
                except Exception:
                    return []
        if not raw:
            return []
        try:
            entries = json.loads(raw)
            return [self.normalize_saved_entry(entry) for entry in entries]
        except Exception:
            return []

    def save_local_leaderboard(self, entries):
        localStorage.setItem(self.leaderboard_key, json.dumps(entries))

    def submit_score(self):
        if not self.player_name:
            return
        entry = self.build_leaderboard_entry()
        if LEADERBOARD_ENDPOINT:
            self.post_remote_score(entry)
        elif USE_LOCAL_LEADERBOARD_FALLBACK:
            entries = self.local_leaderboard()
            entries.append(entry)
            self.save_local_leaderboard(entries)
            self.render_leaderboard(entries)

    def save_progress_snapshot(self):
        if not self.player_name or not USE_LOCAL_LEADERBOARD_FALLBACK or LEADERBOARD_ENDPOINT:
            return
        entry = self.build_leaderboard_entry()
        if not self.entry_has_valid_stat(entry):
            return
        entries = self.local_leaderboard()
        entries.append(entry)
        self.save_local_leaderboard(entries)
        self.render_leaderboard(entries)

    def build_leaderboard_entry(self):
        elapsed = 0
        if self.run_started_at is not None:
            elapsed = round(time.monotonic() - self.run_started_at, 1)
        accuracy = None
        if self.questions_answered > 0:
            accuracy = round((self.questions_correct / self.questions_answered) * 100)
        completed_run = None
        if self.level_index == len(LEVELS) - 1 and self.level_points >= LEVELS[self.level_index]["target_points"]:
            completed_run = elapsed
        return self.normalize_saved_entry(
            {
                "playerName": self.player_name,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
                "fullRunTime": completed_run,
                "quizAccuracy": accuracy,
                "correctAnswers": self.questions_correct,
                "totalQuestions": self.questions_answered,
                "survivalTime": elapsed,
                "deepestLevel": self.zone_depth_name(self.best_zone_reached),
                "score": self.score,
            }
        )

    def load_leaderboard(self):
        if LEADERBOARD_ENDPOINT:
            self.fetch_remote_leaderboard()
        elif USE_LOCAL_LEADERBOARD_FALLBACK:
            self.render_leaderboard(self.local_leaderboard())
        else:
            self.render_leaderboard([])

    def render_leaderboard(self, entries):
        self.render_catch_of_day(entries)
        filtered = self.filter_leaderboard_entries(entries)
        aggregated = self.aggregate_leaderboard_profiles(filtered)
        fastest = sorted(
            [entry for entry in aggregated if isinstance(entry.get("fullRunTime"), (int, float))],
            key=lambda item: (item["fullRunTime"], item["playerName"].lower()),
        )[:LEADERBOARD_LIMIT]
        claws = sorted(
            [entry for entry in aggregated if isinstance(entry.get("quizAccuracy"), (int, float))],
            key=lambda item: (-item.get("quizAccuracy", 0), -item.get("totalQuestions", 0), -item.get("updatedAt", 0), item["playerName"].lower()),
        )[:LEADERBOARD_LIMIT]
        survivor = sorted(
            [entry for entry in aggregated if isinstance(entry.get("survivalTime"), (int, float))],
            key=lambda item: (-item.get("survivalTime", 0), -self.level_rank(item.get("deepestLevel")), item["playerName"].lower()),
        )[:LEADERBOARD_LIMIT]

        console.log("Raw leaderboard entries:", json.dumps(entries))
        console.log("Fastest entries:", json.dumps(fastest))
        console.log("Quiz entries:", json.dumps(claws))
        console.log("Survival entries:", json.dumps(survivor))

        self.render_leaderboard_category(
            self.fastest_list_el,
            fastest,
            "No full-depth runs yet—dive deeper.",
            "fastest",
            lambda item: f"{item['fullRunTime']:.1f}s",
        )
        self.render_leaderboard_category(
            self.claws_list_el,
            claws,
            "No quiz data yet—time to sharpen up.",
            "claws",
            lambda item: f"{round(item.get('quizAccuracy', 0))}%",
        )
        self.render_leaderboard_category(
            self.survivor_list_el,
            survivor,
            "No survivors yet—stay alive longer.",
            "survivor",
            lambda item: f"{item.get('survivalTime', 0):.1f}s • {item.get('deepestLevel', self.zone_depth_name(1))}",
        )
        self.render_personal_bests(aggregated)

    def render_catch_of_day(self, entries):
        winner = self.compute_catch_of_day_winner(self.aggregate_leaderboard_profiles(entries))
        current_name = self.player_name.strip().lower()
        self.catch_of_day_el.classList.remove("winner-highlight")
        self.catch_of_day_body_el.innerHTML = ""
        if not winner:
            paragraph = document.createElement("p")
            paragraph.innerText = "No saved runs yet—be the first to make waves."
            self.catch_of_day_body_el.appendChild(paragraph)
            return

        if winner["playerName"].strip().lower() == current_name and current_name:
            self.catch_of_day_el.classList.add("winner-highlight")

        title = document.createElement("p")
        title.className = "catch-winner"
        title.innerText = f"🏆 {winner['playerName']} — Top Shrimp"

        fastest = document.createElement("p")
        fastest.className = "catch-stat"
        completed_run = winner.get("fullRunTime")
        fastest.innerText = f"⏱ Fastest Run: {completed_run:.1f}s" if isinstance(completed_run, (int, float)) else "⏱ Fastest Run: Not recorded"

        accuracy = document.createElement("p")
        accuracy.className = "catch-stat"
        winner_accuracy = winner.get("quizAccuracy")
        accuracy.innerText = f"🧠 Accuracy: {round(winner_accuracy)}%" if self.safe_number(winner.get("totalQuestions"), 0) > 0 and isinstance(winner_accuracy, (int, float)) else "🧠 Accuracy: Not recorded"

        survival = document.createElement("p")
        survival.className = "catch-stat"
        survival_seconds = self.safe_number(winner.get("survivalTime"), 0)
        survival.innerText = f"🌊 Survival: {survival_seconds:.1f}s • {winner.get('deepestLevel', self.zone_depth_name(1))}" if survival_seconds > 0 else "🌊 Survival: Not recorded"

        self.catch_of_day_body_el.appendChild(title)
        self.catch_of_day_body_el.appendChild(fastest)
        self.catch_of_day_body_el.appendChild(accuracy)
        self.catch_of_day_body_el.appendChild(survival)

    def compute_catch_of_day_winner(self, entries):
        eligible = [
            entry for entry in entries
            if entry.get("fullRunTime") is not None
            or (entry.get("quizAccuracy") is not None and self.safe_number(entry.get("totalQuestions"), 0) > 0)
            or self.safe_number(entry.get("survivalTime"), 0) > 0
            or entry.get("deepestLevel") is not None
        ]
        if not eligible:
            return None
        scored = []
        for entry in eligible:
            completed_run = entry.get("fullRunTime")
            speed_score = 0
            if isinstance(completed_run, (int, float)) and completed_run > 0:
                speed_score = 1000 / completed_run

            accuracy_value = entry.get("quizAccuracy")
            accuracy_score = 0
            if isinstance(accuracy_value, (int, float)):
                accuracy_score = accuracy_value

            survival_seconds = self.safe_number(entry.get("survivalTime"), 0)
            survival_score = survival_seconds / 10 if survival_seconds > 0 else 0

            level_score = {
                "pH-resh and cool": 10,
                "CO₂ncerning pH": 20,
                "Naked and Acidi-fied": 30,
            }.get(entry.get("deepestLevel"), 10)

            overall = speed_score + accuracy_score + survival_score + level_score
            scored.append((overall, entry))

        scored.sort(
            key=lambda item: (
                -self.safe_number(item[0], 0),
                item[1].get("fullRunTime") if isinstance(item[1].get("fullRunTime"), (int, float)) else float("inf"),
                -self.safe_number(item[1].get("quizAccuracy"), 0),
                -self.level_rank(item[1].get("deepestLevel")),
                item[1]["playerName"].lower(),
            )
        )
        return scored[0][1]

    def safe_number(self, value, default=0):
        return value if isinstance(value, (int, float)) else default

    def normalized_inverse(self, value, min_value, max_value):
        if value is None or min_value is None or max_value is None:
            return None
        if max_value == min_value:
            return 1.0
        return (max_value - value) / (max_value - min_value)

    def normalized_value(self, value, min_value, max_value):
        if value is None:
            return None
        if max_value == min_value:
            return 1.0 if max_value > 0 else 0.0
        return (value - min_value) / (max_value - min_value)

    def render_leaderboard_category(self, target_el, entries, empty_text, category_key, stat_builder):
        target_el.innerHTML = ""
        if not entries:
            item = document.createElement("li")
            item.className = "leaderboard-empty"
            item.innerText = empty_text
            target_el.appendChild(item)
            return
        current_name = self.player_name.strip().lower()
        for index, entry in enumerate(entries, start=1):
            item = document.createElement("li")
            classes = ["leaderboard-entry"]
            if entry["playerName"].strip().lower() == current_name and current_name:
                classes.append("current-player")
            item.className = " ".join(classes)

            label = document.createElement("span")
            label.className = "leaderboard-line"
            label.innerText = (
                f"{self.rank_title(category_key, index)} — "
                f"{entry['playerName']} — "
                f"{stat_builder(entry)}"
            )
            item.appendChild(label)

            target_el.appendChild(item)

    def normalize_saved_entry(self, entry):
        normalized = dict(entry)
        player_name = normalized.get("playerName") or normalized.get("name") or "Anonymous"
        timestamp = normalized.get("timestamp")
        if not timestamp:
            updated_at = normalized.get("updated_at")
            if isinstance(updated_at, (int, float)) and updated_at > 0:
                timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(updated_at))
            else:
                timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())

        total_questions = (
            normalized.get("totalQuestions")
            or normalized.get("quiz_attempts")
            or normalized.get("quizResults", {}).get("totalQuestions", 0)
            or normalized.get("runs", [{}])[-1].get("quiz", {}).get("totalQuestions", 0)
            or 0
        )
        correct_answers = (
            normalized.get("correctAnswers")
            or normalized.get("questions_correct")
            or normalized.get("quizResults", {}).get("correctAnswers", 0)
            or normalized.get("runs", [{}])[-1].get("quiz", {}).get("correctAnswers", 0)
            or 0
        )
        quiz_accuracy = normalized.get("quizAccuracy")
        if quiz_accuracy is None:
            quiz_accuracy = normalized.get("accuracy")
        if quiz_accuracy is None:
            quiz_accuracy = normalized.get("quizScore")
        if isinstance(quiz_accuracy, (int, float)) and 0 <= quiz_accuracy <= 1:
            quiz_accuracy = quiz_accuracy * 100
        if quiz_accuracy is None and total_questions > 0:
            quiz_accuracy = (correct_answers / total_questions) * 100

        deepest_level = normalized.get("deepestLevel")
        if deepest_level is None:
            deepest_level = self.zone_depth_name(normalized.get("zone_reached", 1))

        updated_at = self.parse_timestamp(timestamp)
        return {
            "playerName": player_name,
            "timestamp": timestamp,
            "updatedAt": updated_at,
            "fullRunTime": self.safe_number(normalized.get("fullRunTime", normalized.get("completed_run_seconds")), None),
            "quizAccuracy": quiz_accuracy if isinstance(quiz_accuracy, (int, float)) else None,
            "correctAnswers": int(correct_answers or 0),
            "totalQuestions": int(total_questions or 0),
            "survivalTime": self.safe_number(normalized.get("survivalTime", normalized.get("survival_seconds")), None),
            "deepestLevel": deepest_level,
            "score": self.safe_number(normalized.get("score"), 0),
        }

    def aggregate_leaderboard_profiles(self, entries):
        profiles = {}
        for entry in entries:
            normalized = self.normalize_saved_entry(entry)
            if not self.entry_has_valid_stat(normalized):
                continue
            key = normalized["playerName"].strip().lower()
            existing = profiles.get(key)
            if existing is None:
                profiles[key] = dict(normalized)
                continue
            existing["playerName"] = normalized["playerName"]
            existing["score"] = max(existing.get("score", 0), normalized.get("score", 0))
            if self.level_rank(normalized.get("deepestLevel")) >= self.level_rank(existing.get("deepestLevel")):
                existing["deepestLevel"] = normalized.get("deepestLevel")
            if isinstance(normalized.get("survivalTime"), (int, float)):
                old_survival = existing.get("survivalTime")
                if not isinstance(old_survival, (int, float)) or normalized["survivalTime"] > old_survival:
                    existing["survivalTime"] = normalized["survivalTime"]
            if isinstance(normalized.get("fullRunTime"), (int, float)):
                old_time = existing.get("fullRunTime")
                if not isinstance(old_time, (int, float)) or normalized["fullRunTime"] < old_time:
                    existing["fullRunTime"] = normalized["fullRunTime"]
            if isinstance(normalized.get("quizAccuracy"), (int, float)):
                old_accuracy = existing.get("quizAccuracy")
                replace_accuracy = False
                if not isinstance(old_accuracy, (int, float)) or normalized["quizAccuracy"] > old_accuracy:
                    replace_accuracy = True
                elif normalized["quizAccuracy"] == old_accuracy and normalized.get("totalQuestions", 0) >= existing.get("totalQuestions", 0):
                    replace_accuracy = True
                if replace_accuracy:
                    existing["quizAccuracy"] = normalized["quizAccuracy"]
                    existing["correctAnswers"] = normalized.get("correctAnswers", 0)
                    existing["totalQuestions"] = normalized.get("totalQuestions", 0)
            existing["updatedAt"] = max(existing.get("updatedAt", 0), normalized.get("updatedAt", 0))
            existing["timestamp"] = normalized["timestamp"]
        return list(profiles.values())

    def filter_leaderboard_entries(self, entries):
        return self.filter_entries_for_period(entries, self.leaderboard_filter)

    def filter_entries_for_period(self, entries, filter_value):
        if filter_value == "all":
            return list(entries)
        now = time.time()
        cutoff = now - (86400 if filter_value == "daily" else 7 * 86400)
        filtered = []
        for entry in entries:
            normalized = self.normalize_saved_entry(entry)
            if normalized.get("updatedAt", 0) >= cutoff:
                filtered.append(normalized)
        return filtered

    def parse_timestamp(self, timestamp):
        if not timestamp:
            return time.time()
        for pattern in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"):
            try:
                return time.mktime(time.strptime(timestamp, pattern))
            except Exception:
                continue
        return time.time()

    def level_rank(self, level_name):
        mapping = {
            "pH-resh and cool": 1,
            "CO₂ncerning pH": 2,
            "Naked and Acidi-fied": 3,
        }
        return mapping.get(level_name, 1)

    def entry_has_valid_stat(self, entry):
        return any(
            [
                isinstance(entry.get("fullRunTime"), (int, float)),
                isinstance(entry.get("quizAccuracy"), (int, float)),
                isinstance(entry.get("survivalTime"), (int, float)),
                self.safe_number(entry.get("score"), 0) > 0,
            ]
        )

    def zone_name(self, zone_number):
        mapping = {
            1: "pH-resh and cool",
            2: "CO₂ncerning pH",
            3: "Naked and Acidi-fied",
        }
        return mapping.get(zone_number, "pH-resh and cool")

    def zone_depth_name(self, zone_number):
        mapping = {
            1: "pH-resh and cool",
            2: "CO₂ncerning pH",
            3: "Naked and Acidi-fied",
        }
        return mapping.get(zone_number, "pH-resh and cool")

    def rank_title(self, category_key, rank):
        titles = {
            "fastest": ["🥇 pHantom of the Ocean", "🥈 CO2mmander", "🥉 Acid Survivor"],
            "claws": ["🥇 Shrimp Supreme", "🥈 Prawn Star", "🥉 Krill Seeker"],
            "survivor": ["🥇 Calcifier Champion", "🥈 Carbon Tracker", "🥉 Buffer Beginner"],
        }
        category_titles = titles.get(category_key, [])
        if 1 <= rank <= len(category_titles):
            return category_titles[rank - 1]
        return f"#{rank} Reef Runner"

    def render_personal_bests(self, entries):
        current_name = self.player_name.strip().lower()
        entry = None
        for item in entries:
            if item["playerName"].strip().lower() == current_name and current_name:
                entry = item
                break
        if not entry:
            self.fastest_best_el.innerText = "Your Best: --"
            self.claws_best_el.innerText = "Your Accuracy: --"
            self.survivor_best_el.innerText = "Your Survival: --"
            return
        fastest = entry.get("fullRunTime")
        self.fastest_best_el.innerText = f"Your Best: {fastest:.1f}s" if fastest is not None else "Your Best: --"
        accuracy = entry.get("quizAccuracy")
        if entry.get("totalQuestions", 0) > 0 and accuracy is not None:
            self.claws_best_el.innerText = f"Your Accuracy: {round(accuracy)}%"
        else:
            self.claws_best_el.innerText = "Your Accuracy: --"
        if isinstance(entry.get("survivalTime"), (int, float)):
            self.survivor_best_el.innerText = f"Your Survival: {entry.get('survivalTime', 0):.1f}s • {entry.get('deepestLevel', self.zone_depth_name(1))}"
        else:
            self.survivor_best_el.innerText = "Your Survival: --"

    def add_test_leaderboard_data(self):
        entries = self.local_leaderboard()
        entries.extend(
            [
                self.normalize_saved_entry(
                    {
                        "playerName": "isha",
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
                        "fullRunTime": 92.4,
                        "quizAccuracy": 87,
                        "survivalTime": 119.8,
                        "deepestLevel": "Naked and Acidi-fied",
                        "score": 2330,
                    }
                ),
                self.normalize_saved_entry(
                    {
                        "playerName": "Ellie",
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
                        "fullRunTime": 104.2,
                        "quizAccuracy": 74,
                        "survivalTime": 88.3,
                        "deepestLevel": "CO₂ncerning pH",
                        "score": 1800,
                    }
                ),
            ]
        )
        self.save_local_leaderboard(entries)
        self.render_leaderboard(entries)

    def post_remote_score(self, entry):
        async def _post():
            options = to_js(
                {
                    "method": "POST",
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps(entry),
                }
            )
            await fetch(LEADERBOARD_ENDPOINT, options)
            await self.fetch_remote_leaderboard()

        asyncio.create_task(_post())

    def fetch_remote_leaderboard(self):
        async def _load():
            response = await fetch(LEADERBOARD_ENDPOINT)
            data = await response.json()
            self.render_leaderboard(data)
            self.leaderboard_note_el.innerText = "Shared leaderboard is live through Google Apps Script."

        return asyncio.create_task(_load())


UnderwaterPacmanGame()
