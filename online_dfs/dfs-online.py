import tkinter as tk

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("House Game")
        self.create_widgets()

    def create_widgets(self):
        label1 = tk.Label(self.root, text="Enter the value of n:")
        label1.pack()

        self.n_entry = tk.Entry(self.root)
        self.n_entry.pack()

        start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        start_button.pack()

    def start_game(self):
        n = int(self.n_entry.get())

        game_window = tk.Toplevel(self.root)
        game_window.title("Game Board")

        self.buttons = []
        for i in range(n):
            row = []
            for j in range(n):
                button = tk.Button(game_window, text=f"{i}-{j}", width=3, height=1)
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

        label2 = tk.Label(game_window, text="Enter the starting house (row, column):")
        label2.grid(row=n, columnspan=n)

        self.start_entry = tk.Entry(game_window)
        self.start_entry.grid(row=n+1, columnspan=n)

        label3 = tk.Label(game_window, text="Enter the ending house (row, column):")
        label3.grid(row=n+2, columnspan=n)

        self.end_entry = tk.Entry(game_window)
        self.end_entry.grid(row=n+3, columnspan=n)

        label4 = tk.Label(game_window, text="Enter blocked houses (row, column):")
        label4.grid(row=n+4, columnspan=n)

        self.blocked_entry = tk.Entry(game_window)
        self.blocked_entry.grid(row=n+5, columnspan=n)

        play_button = tk.Button(game_window, text="Play Game", command=self.play_game)
        play_button.grid(row=n+6, columnspan=n)

    def play_game(self):
        start = tuple(map(int, self.start_entry.get().split(',')))
        end = tuple(map(int, self.end_entry.get().split(',')))
        blocked = [tuple(map(int, pair.split(','))) for pair in self.blocked_entry.get().split(';')]
        
        self.online_dfs_agent(start, end, blocked)

    def get_next_move(self, current):
        end = tuple(map(int, self.end_entry.get().split(',')))
        if current[0] < end[0]:
            return (1, 0)  # Move down
        elif current[0] > end[0]:
            return (-1, 0)  # Move up
        elif current[1] < end[1]:
            return (0, 1)  # Move right
        elif current[1] > end[1]:
            return (0, -1)  # Move left
        else:
            return None  # Already at the goal

    def online_dfs_agent(self, start, end, blocked):
        visited = set()
        stack = [(start, [start])]

        while stack:
            current, path = stack.pop()
            if current == end:
                self.highlight_path(path)
                return
            if current not in visited:
                visited.add(current)
                self.buttons[current[0]][current[1]].config(bg="blue")
                next_move = self.get_next_move(current)
                if next_move is not None:
                    neighbor = (current[0] + next_move[0], current[1] + next_move[1])
                    if neighbor not in blocked:
                        stack.append((neighbor, path + [neighbor]))

    def highlight_path(self, path):
        for house in path:
            row, col = house
            self.buttons[row][col].config(bg="red")

root = tk.Tk()
game = GameGUI(root)
root.mainloop()