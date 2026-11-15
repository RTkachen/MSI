import tkinter as tk
from tkinter import ttk
from typing import List
from models import Maze, Point, SearchResult


class MazeGUI:
    """
    Okienkowy interfejs graficzny (GUI) oparty na wbudowanej bibliotece tkinter.
    Automatycznie dopasowuje rozmiar pól labiryntu do okna i pozwala
    przełączać wyniki wszystkich algorytmów jednym kliknięciem.
    """
    # Paleta kolorów nowoczesnego ciemnego motywu
    COLOR_BG = "#1e1e2e"         # Tło aplikacji
    COLOR_EMPTY = "#2b2b3c"      # Wolne pole '0'
    COLOR_WALL = "#11111b"       # Przeszkoda '1'
    COLOR_VISITED = "#3b82f6"    # Odwiedzone pole '.' (niebieski)
    COLOR_PATH = "#facc15"       # Ścieżka agenta '*' (jasnożółty)
    COLOR_START = "#22c55e"      # Punkt startowy 'S' (zielony)
    COLOR_GOAL = "#ef4444"       # Punkt docelowy 'G' (czerwony)
    COLOR_GRID = "#181825"       # Delikatne obramowanie kafelków

    def __init__(self, maze: Maze, results: List[SearchResult]) -> None:
        self.maze = maze
        self.results = results
        self.current_result = results[0] if results else None

        # Inicjalizacja głównego okna
        self.root = tk.Tk()
        self.root.title("Inteligentny agent w środowisku labiryntu - Wizualizacja GUI")
        self.root.geometry("1150x780")
        self.root.configure(bg=self.COLOR_BG)

        self._build_layout()

    def _build_layout(self) -> None:
        """Buduje panel boczny z wyborem algorytmu oraz płótno (Canvas) z mapą."""
        # Lewy panel ze spisem uruchomionych algorytmów i statystykami
        sidebar = tk.Frame(self.root, bg=self.COLOR_BG, width=360, padx=12, pady=12)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        title_lbl = tk.Label(
            sidebar,
            text="Wybierz konfigurację algorytmu:",
            fg="#ffffff",
            bg=self.COLOR_BG,
            font=("Segoe UI", 11, "bold"),
        )
        title_lbl.pack(anchor="w", pady=(0, 6))

        # Lista (Listbox) ze wszystkimi wynikami z tabeli eksperymentalnej
        self.listbox = tk.Listbox(
            sidebar,
            bg="#2b2b3c",
            fg="#ffffff",
            selectbackground="#3b82f6",
            font=("Consolas", 10),
            width=42,
            height=18,
            borderwidth=0,
            highlightthickness=1,
        )
        self.listbox.pack(fill=tk.X, pady=(0, 12))

        for res in self.results:
            self.listbox.insert(tk.END, f" {res.algorithm_name}")

        # Podpięcie zdarzenia kliknięcia na liście do funkcji odświeżającej mapę
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

        # Ramka ze szczegółowymi statystykami wybranego przebiegu
        self.stats_label = tk.Label(
            sidebar,
            text="",
            fg="#e2e8f0",
            bg="#2b2b3c",
            font=("Consolas", 10),
            justify=tk.LEFT,
            padx=10,
            pady=10,
        )
        self.stats_label.pack(fill=tk.X, pady=(0, 12))

        # Legenda kolorów w oknie
        legend_frame = tk.LabelFrame(
            sidebar,
            text=" Legenda ",
            fg="#ffffff",
            bg=self.COLOR_BG,
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=8,
        )
        legend_frame.pack(fill=tk.X)

        legend_items = [
            ("Punkt startowy (S)", self.COLOR_START),
            ("Punkt docelowy (G)", self.COLOR_GOAL),
            ("Ścieżka agenta (*)", self.COLOR_PATH),
            ("Odwiedzone pole (.)", self.COLOR_VISITED),
            ("Wolne pole (0)", self.COLOR_EMPTY),
            ("Przeszkoda / ściana (1)", self.COLOR_WALL),
        ]
        for label_text, color in legend_items:
            row = tk.Frame(legend_frame, bg=self.COLOR_BG, pady=2)
            row.pack(fill=tk.X)
            swatch = tk.Canvas(row, width=18, height=18, bg=color, highlightthickness=1)
            swatch.pack(side=tk.LEFT, padx=(0, 8))
            tk.Label(row, text=label_text, fg="#cbd5e1", bg=self.COLOR_BG, font=("Segoe UI", 9)).pack(side=tk.LEFT)

        # Prawa część okna: Płótno (Canvas), które automatycznie skaluje labirynt przy zmianie rozmiaru okna
        self.canvas = tk.Canvas(self.root, bg=self.COLOR_BG, highlightthickness=0)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=12, pady=12)
        self.canvas.bind("<Configure>", lambda event: self._draw_maze())

        # Domyślne zaznaczenie pierwszego wyniku na liście
        if self.results:
            self.listbox.selection_set(0)
            self._update_stats()

    def _on_select(self, event: object) -> None:
        """Obsługuje zmianę wybranego algorytmu na liście."""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.current_result = self.results[index]
            self._update_stats()
            self._draw_maze()

    def _update_stats(self) -> None:
        """Aktualizuje panel tekstowy z metrykami dla wybranego algorytmu."""
        if not self.current_result:
            return
        r = self.current_result
        status = "Znaleziono cel" if r.found else "Brak ścieżki"
        text = (
            f"Konfiguracja:\n  {r.algorithm_name}\n\n"
            f"Status:            {status}\n"
            f"Koszt ścieżki:     {r.cost} kroków\n"
            f"Odwiedzone stany:  {len(r.visited)}\n"
            f"Czas wykonania:    {r.execution_time_ms:.3f} ms"
        )
        self.stats_label.config(text=text)

    def _draw_maze(self) -> None:
        """Rysuje siatkę labiryntu na płótnie, automatycznie wyliczając rozmiar pojedynczej komórki."""
        self.canvas.delete("all")
        if not self.current_result:
            return

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        if canvas_w < 10 or canvas_h < 10:
            return

        # Wyliczenie rozmiaru kafelka tak, aby cała plansza zmieściła się w oknie z zachowaniem proporcji kwadratu
        cell_w = canvas_w / self.maze.cols
        cell_h = canvas_h / self.maze.rows
        cell_size = min(cell_w, cell_h)

        # Wyśrodkowanie planszy na płótnie
        offset_x = (canvas_w - (cell_size * self.maze.cols)) / 2
        offset_y = (canvas_h - (cell_size * self.maze.rows)) / 2

        path_set = set(self.current_result.path)
        visited_set = self.current_result.visited

        for r in range(self.maze.rows):
            for c in range(self.maze.cols):
                pos = Point(r, c)
                cell = self.maze.grid[r][c]

                # Ustalenie koloru kafelka
                if cell == "S":
                    fill_color = self.COLOR_START
                elif cell == "G":
                    fill_color = self.COLOR_GOAL
                elif pos in path_set:
                    fill_color = self.COLOR_PATH
                elif pos in visited_set:
                    fill_color = self.COLOR_VISITED
                elif cell == "1":
                    fill_color = self.COLOR_WALL
                else:
                    fill_color = self.COLOR_EMPTY

                x1 = offset_x + c * cell_size
                y1 = offset_y + r * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                # Narysowanie pojedynczego pola na płótnie
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=fill_color,
                    outline=self.COLOR_GRID if cell_size > 6 else "",
                )

                # Wpisanie liter S oraz G w środek ich pól, jeśli kafelki są wystarczająco duże
                if cell in ("S", "G") and cell_size >= 12:
                    font_size = max(8, int(cell_size * 0.45))
                    self.canvas.create_text(
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        text=cell,
                        fill="#ffffff",
                        font=("Segoe UI", font_size, "bold"),
                    )

    def run(self) -> None:
        """Uruchamia główną pętlę zdarzeń okienka."""
        self.root.mainloop()
