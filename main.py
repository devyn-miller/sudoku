import tkinter as tk
from tkinter import messagebox
import random
import time

class Sudoku:
    def __init__(self, size=9, difficulty='easy'):
        self.size = size
        self.difficulty = difficulty
        self.board = [[0] * size for _ in range(size)]
        self.generate_board()

    def generate_board(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.size // 3)
        self.remove_digits()

    def fill_diagonal(self):
        for i in range(0, self.size, self.size // 3):
            self.fill_box(i, i)

    def fill_box(self, row, col):
        nums = list(range(1, self.size + 1))
        random.shuffle(nums)
        for i in range(self.size // 3):
            for j in range(self.size // 3):
                self.board[row + i][col + j] = nums.pop()

    def is_safe(self, row, col, num):
        for x in range(self.size):
            if self.board[row][x] == num or self.board[x][col] == num:
                return False
        start_row, start_col = row - row % (self.size // 3), col - col % (self.size // 3)
        for i in range(self.size // 3):
            for j in range(self.size // 3):
                if self.board[i + start_row][j + start_col] == num:
                    return False
        return True

    def fill_remaining(self, i, j):
        if j >= self.size and i < self.size - 1:
            i += 1
            j = 0
        if i >= self.size and j >= self.size:
            return True
        if i < self.size // 3:
            if j < self.size // 3:
                j = self.size // 3
        elif i < self.size - self.size // 3:
            if j == int(i / (self.size // 3)) * (self.size // 3):
                j += self.size // 3
        else:
            if j == self.size - self.size // 3:
                i += 1
                j = 0
                if i >= self.size:
                    return True
        for num in range(1, self.size + 1):
            if self.is_safe(i, j, num):
                self.board[i][j] = num
                if self.fill_remaining(i, j + 1):
                    return True
                self.board[i][j] = 0
        return False

    def remove_digits(self):
        count = self.size * self.size
        if self.difficulty == 'easy':
            count -= 40
        elif self.difficulty == 'medium':
            count -= 30
        elif self.difficulty == 'hard':
            count -= 20
        while count != 0:
            cell_id = random.randint(0, self.size * self.size - 1)
            i = cell_id // self.size
            j = cell_id % self.size
            if self.board[i][j] != 0:
                count -= 1
                self.board[i][j] = 0


class SudokuGUI:
    def __init__(self, root, size=9, difficulty='easy'):
        self.root = root
        self.size = size
        self.difficulty = difficulty
        self.sudoku = Sudoku(size, difficulty)
        self.board = self.sudoku.board
        self.entries = [[None] * size for _ in range(size)]
        self.start_time = time.time()
        self.hints_used = 0
        self.create_widgets()

    def create_widgets(self):
        self.root.title("Sudoku")
        self.root.geometry(f"{self.size * 50 + 20}x{self.size * 50 + 70}")
        self.canvas = tk.Canvas(self.root, width=self.size * 50, height=self.size * 50)
        self.canvas.pack()
        self.draw_grid()
        self.draw_numbers()
        self.create_buttons()

    def draw_grid(self):
        for i in range(self.size + 1):
            width = 2 if i % (self.size // 3) == 0 else 1
            self.canvas.create_line(10, 10 + i * 50, 10 + self.size * 50, 10 + i * 50, width=width)
            self.canvas.create_line(10 + i * 50, 10, 10 + i * 50, 10 + self.size * 50, width=width)

    def draw_numbers(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    self.entries[i][j] = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center')
                    self.entries[i][j].insert(0, self.board[i][j])
                    self.entries[i][j].config(state='disabled')
                    self.entries[i][j].place(x=10 + j * 50, y=10 + i * 50, width=50, height=50)
                else:
                    self.entries[i][j] = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center')
                    self.entries[i][j].place(x=10 + j * 50, y=10 + i * 50, width=50, height=50)

    def create_buttons(self):
        self.solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        self.solve_button.pack(side='left', padx=10, pady=10)
        self.check_button = tk.Button(self.root, text="Check", command=self.check)
        self.check_button.pack(side='left', padx=10, pady=10)
        self.hint_button = tk.Button(self.root, text="Hint", command=self.hint)
        self.hint_button.pack(side='left', padx=10, pady=10)
        self.time_label = tk.Label(self.root, text="Time: 0s")
        self.time_label.pack(side='right', padx=10, pady=10)
        self.hints_label = tk.Label(self.root, text="Hints: 0")
        self.hints_label.pack(side='right', padx=10, pady=10)
        self.update_time()

    def update_time(self):
        elapsed_time = int(time.time() - self.start_time)
        self.time_label.config(text=f"Time: {elapsed_time}s")
        self.root.after(1000, self.update_time)

    def solve(self):
        self.sudoku.fill_remaining(0, self.size // 3)
        self.board = self.sudoku.board
        self.draw_numbers()

    def check(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.entries[i][j].get() != '' and int(self.entries[i][j].get()) != self.board[i][j]:
                    messagebox.showinfo("Incorrect", "The solution is incorrect.")
                    return
        messagebox.showinfo("Correct", "Congratulations! The solution is correct.")

    def hint(self):
        self.hints_used += 1
        self.hints_label.config(text=f"Hints: {self.hints_used}")
        for i in range(self.size):
            for j in range(self.size):
                if self.entries[i][j].get() == '':
                    self.entries[i][j].insert(0, self.board[i][j])
                    return
                

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root, size=9, difficulty='medium')
    root.mainloop()