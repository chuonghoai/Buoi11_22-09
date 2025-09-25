import tkinter as tk
from PIL import Image, ImageTk
import random
import math

class node:
    def __init__(self, n=8):
        self.n = n
        self.state = []
        self.cost = 0
        
    def random(self):
        self.state = [random.randint(0, self.n-1) for _ in range(self.n)]

    def cost_conflict(self, state=None):
        if state == None:
            state = self.state
        cnt = 0
        for i in range(self.n):
            for j in range(i + 1, len(state)):
                if state[i] == state[j]:
                    cnt += 1
        return cnt

    def create_child_random(self):
        child = node()
        child.state = self.state[:]
        col = random.randint(0, self.n - 1)
        row = random.randint(0, self.n - 1)
        
        while child.state[row] == col:
            col = random.randint(0, self.n - 1)

        child.state[row] = col
        return child
    
class Image_X:
    def __init__(self):
        self.white = ImageTk.PhotoImage(Image.open("./whiteX.png").resize((60, 60)))
        self.black = ImageTk.PhotoImage(Image.open("./blackX.png").resize((60, 60)))
        self.null = tk.PhotoImage(width=1, height=1)
        
class board:
    def __init__(self, root):  #n: số lượng quân xe (defult = 8)
        self.root = root
        root.title("Simulated Anneling")
        root.config(bg="lightgray")
        self.image = Image_X()
        self.n = node().n
        
        self.frame_path = self.draw_frame(0, 0)
        self.frame_left = self.draw_frame(0, 1)
        self.text_path = tk.Text(self.frame_path, width=25, height=31)
        self.text_path.pack(anchor="nw", padx=5, pady=5)
        
        self.frame_right = self.draw_frame(0, 2)
        self.board_left = self.create_board(self.frame_left)
        self.board_right = self.create_board(self.frame_right)
        self.draw_button()
        
    def draw_frame(self, row, col, background="white", rl="solid", border=1, HLthickness=1):
        frame = tk.Frame(self.root, bg=background, relief=rl, bd=border, highlightthickness=HLthickness)
        frame.grid(column=col, row=row, padx=10, pady=10)
        return frame
    
    def create_board(self, frame):
        buttons = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                color = "white" if (i + j) % 2 == 0 else "black"
                img = self.image.null                
                btn = tk.Button(frame, image=img, width=60, height=60, bg=color,
                                relief="flat", borderwidth=0, highlightthickness=0)
                btn.grid(row = i, column = j, padx=1, pady=1)
                row.append(btn)
            buttons.append(row)
        return buttons

    def draw_button(self):
        _pady = 5
        _padx = 10
        _width = 15
        
        frame_button_left = self.draw_frame(1, 1, "lightgray", "flat", 0, 0)
        frame_button_right = self.draw_frame(1, 2, "lightgray", "flat", 0, 0)
        
        self.HC_btn = tk.Button(frame_button_right, text="Hill - Climbing", width=_width)
        self.HC_btn.grid(row=1, column=1, pady=_pady, padx=_padx)
        self.SA_btn = tk.Button(frame_button_right, text="Simulated Anneling", width=_width)
        self.SA_btn.grid(row=2, column=1, pady=_pady, padx=_padx)
        self.Beam_btn = tk.Button(frame_button_right, text="Local beam search", width=_width)
        self.Beam_btn.grid(row=1, column=2, pady=_pady, padx=_padx)
        self.GNT_btn = tk.Button(frame_button_right, text="Genetic algorithms", width=_width)
        self.GNT_btn.grid(row=2, column=2, pady=_pady, padx=_padx)
        
        self.reset_btn = tk.Button(frame_button_left, text="Reset", bg="red", fg="white")
        self.reset_btn.grid(row=1, column=1, pady=_pady, padx=_padx)
        self.path_btn = tk.Button(frame_button_left, text="Path")
        self.path_btn.grid(row=1, column=0, pady=_pady, padx=_padx)

    def draw_xa(self,  buttons, state=[]):
        for i in range(self.n):
            for j in range(self.n):
                buttons[i][j].config(image=self.image.null)
        
        for row, col in enumerate(state):
            color = "white" if (row + col) % 2 == 0 else "black"
            img = self.image.white if color == "black" else self.image.black
            buttons[row][col].config(image=img)

class algorithm(board):
    def __init__(self, root):
        super().__init__(root)
        self.SA_btn.config(command=self.SA_btn_algorithm)
        self.HC_btn.config(command=self.HC_btn_algorithm)
        self.Beam_btn.config(command=self.Beam_btn_algorithm)
        self.GNT_btn.config(command=self.GNT_btn_algorithm)
        self.path_btn.config(command=self.path)
        self.reset_btn.config(command=self.reset)
        
        #linh tinh khác
        self.setting_xa = True
        self.nd = node()
        
        #dùng cho SA
        self.path_state = []
        self.state = node()
        self.T = 100
        self.T_min = 1e-6
        self.alpha = 0.99
        
        #dùng cho beam
        self.k = 5
        self.max_loop = 1000
        
        #dùng cho genetic
        self.limit_child = 100
        self.limit_generation = 1000
        self.mutate_rate = 0.1
        
    #1. Simulated Anealing
    def SimulatedAnnealing(self):
        state = self.state
        state.random()
        state.cost = state.cost_conflict()
        self.path_state = []
        
        while self.T > self.T_min:
            self.path_state.append(state.state[:])
            
            if state.cost == 0:
                return state.state
            
            state_child = state.create_child_random()
            state_child.cost = state_child.cost_conflict()
            delta = state_child.cost - state.cost
            
            if delta <= 0:
                state = state_child
            else:
                p = math.exp(-delta / self.T)
                if random.random() < p:
                    state = state_child
            self.T *= self.alpha
        return None

    def SA_btn_algorithm(self):
        self.draw_xa(self.board_left)
        self.draw_xa(self.board_right)
        self.state = node()
        self.T = 100
        
        state = None
        while state is None:
            state = self.SimulatedAnnealing()
        
        self.draw_xa(self.board_right, state)

    #2. Hill climbing
    def HillClimbing(self):
        state = node()
        state.state = []
        self.path_state = []
        
        for row in range(state.n):
            child_col = None
            child_cost = 9999
            child = node()

            for col in range(state.n):
                child.state = state.state[:] + [col]
                child.cost = child.cost_conflict()

                if child.cost <= child_cost:
                    child_cost = child.cost
                    child_col = col

            state.state.append(child_col)
            self.path_state.append(state.state[:])

        return state.state

    def HC_btn_algorithm(self):
        self.draw_xa(self.board_left)
        self.draw_xa(self.board_right)
        self.state = node()
        
        state = None
        while state is None:
            state = self.HillClimbing()
        self.draw_xa(self.board_right, state)

    #3. Local beam sarch
    def Beam(self):
        k = random.randint(1, self.k)
        max_loop = self.max_loop
        nd = self.nd

        beam = []
        self.path_state = []
        for _ in range(k):
            nd.random()
            beam.append((nd.state[:], nd.cost_conflict()))

        for _ in range(max_loop):
            beam.sort(key=lambda x: x[1])
            best_state = beam[0][0][:]
            self.path_state.append(best_state[:])

            if beam[0][1] == 0:
                return beam[0][0]

            neighbor = []
            for state, _ in beam:
                for row in range(self.n):
                    for col in range(self.n):
                        if state[row] == col:
                            continue
                        ns = state[:]
                        ns[row] = col
                        
                        neighbor.append((ns, nd.cost_conflict(ns)))

            neighbor.sort(key=lambda x: x[1])
            beam = neighbor[:k]

        return None
    
    def Beam_btn_algorithm(self):
        self.draw_xa(self.board_left)
        self.draw_xa(self.board_right)
        state = None
        while state is None:
            state = self.Beam()
        self.draw_xa(self.board_right, state)

    #4. Genetic algorithm
    def create_first_generation(self, pop_size):
        pop = []
        for _ in range(pop_size):
            nd = node(self.n)
            nd.random()                  # sinh state ngẫu nhiên
            pop.append(nd)               # lưu nguyên node thay vì list
        return pop

    def select_parent(self, population, k=3):
        participants = random.sample(population, k)
        participants.sort(key=lambda nd: nd.cost_conflict())
        return participants[0]           # trả về node tốt nhất

    def grafting(self, parent1, parent2):
        # one-point crossover
        point = random.randint(1, self.n - 1)
        child1 = node(self.n)
        child1.state = parent1.state[:point] + parent2.state[point:]
        child2 = node(self.n)
        child2.state = parent2.state[:point] + parent1.state[point:]
        return child1, child2

    def mutate(self, nd, mutation_rate):
        for i in range(self.n):
            if random.random() < mutation_rate:
                nd.state[i] = random.randint(0, self.n - 1)

    def genetic_algorithm(self):
        child_size = self.limit_child
        generation = self.limit_generation
        mutate_rate = self.mutate_rate

        population = self.create_first_generation(child_size)
        self.path_state = []

        for gen in range(generation):
            # đánh giá và lưu best để hiển thị
            population.sort(key=lambda nd: nd.cost_conflict())
            best_nd = population[0]
            self.path_state.append(best_nd.state[:])

            if best_nd.cost_conflict() == 0:
                return best_nd.state

            # tạo thế hệ mới
            new_pop = []
            while len(new_pop) < child_size:
                p1 = self.select_parent(population)
                p2 = self.select_parent(population)
                c1, c2 = self.grafting(p1, p2)
                self.mutate(c1, mutate_rate)
                self.mutate(c2, mutate_rate)
                new_pop.append(c1)
                if len(new_pop) < child_size:
                    new_pop.append(c2)
            population = new_pop
        return None

    def GNT_btn_algorithm(self):
        self.draw_xa(self.board_left)
        self.draw_xa(self.board_right)
        solution = None
        while solution is None:
            solution = self.genetic_algorithm()
        self.draw_xa(self.board_right, solution)

    def reset(self):
        self.setting_xa = False
        self.text_path.delete("1.0", tk.END)
        self.draw_xa(self.board_left)
        self.draw_xa(self.board_right)

    def path(self):
        if not self.setting_xa:
            self.setting_xa = True
        self.text_path.delete("1.0", tk.END)
        for state in self.path_state:
            if not self.setting_xa:
                return
            self.draw_xa(self.board_left, state)
            self.text_path.insert(tk.END, str(state) + "\n")
            self.text_path.see(tk.END)
            self.frame_left.update()
            self.root.after(200)

def run_app():
    root = tk.Tk()
    app = algorithm(root)

    root.mainloop()

if __name__ == "__main__":
    run_app()