import tkinter as tk


class RasterAlgorithmApp:
    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=400, height=400)
        self.canvas.pack(side="left", padx=10, pady=10)
        self.draw_frame = tk.Frame(self.window)
        self.draw_frame.pack(side="right", padx=10, pady=10)
        self.scale_entry = tk.Entry(self.draw_frame)
        self.scale_entry.insert(0, "20")
        self.scale_entry.pack()
        self.draw_scale_button = tk.Button(self.draw_frame, text="Change Scale", command=self.change_scale)
        self.draw_scale_button.pack(pady=5)
        self.scale = int(self.scale_entry.get())
        self.draw_step_button = tk.Button(self.draw_frame, text="Draw Step Algorithm", command=self.draw_step_algorithm)
        self.draw_step_button.pack(pady=5)
        self.draw_bresenham_button = tk.Button(self.draw_frame, text="Draw Bresenham Algorithm", command=self.draw_bresenham_algorithm)
        self.draw_bresenham_button.pack(pady=5)


        self.x0_label = tk.Label(self.draw_frame, text="x0:")
        self.x0_label.pack()
        self.x0_entry = tk.Entry(self.draw_frame)
        self.x0_entry.insert(0, "0")
        self.x0_entry.pack()

        self.y0_label = tk.Label(self.draw_frame, text="y0:")
        self.y0_label.pack()
        self.y0_entry = tk.Entry(self.draw_frame)
        self.y0_entry.insert(0, "0")
        self.y0_entry.pack()

        self.x1_label = tk.Label(self.draw_frame, text="x1:")
        self.x1_label.pack()
        self.x1_entry = tk.Entry(self.draw_frame)
        self.x1_entry.insert(0, "1")
        self.x1_entry.pack()

        self.y1_label = tk.Label(self.draw_frame, text="y1:")
        self.y1_label.pack()
        self.y1_entry = tk.Entry(self.draw_frame)
        self.y1_entry.insert(0, "1")
        self.y1_entry.pack()


        self.window.update()
        self.draw_grid()
        self.draw_axes()
        self.window.mainloop()

    def change_scale(self):
        self.scale = self.scale = int(self.scale_entry.get())
        self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), fill="white")
        self.draw_grid()
        self.draw_axes()

    def draw_step_algorithm(self):
        self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), fill="white")
        self.draw_grid()
        self.draw_axes()
        x0 = int(self.x0_entry.get())
        y0 = int(self.y0_entry.get())
        x1 = int(self.x1_entry.get())
        y1 = int(self.y1_entry.get())
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        steps = max(dx, dy)
        x_increment = (x1 - x0) / steps
        y_increment = (y1 - y0) / steps

        for i in range(int(steps) + 1):
            x = round(x0 + i * x_increment)
            y = round(y0 + i * y_increment)
            self.paint_rectangle(x, y, "red")

        self.canvas.create_line(self.to_canvas_coords(x0, y0), self.to_canvas_coords(x1, y1))

    def draw_bresenham_algorithm(self):
        self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), fill="white")
        self.draw_grid()
        self.draw_axes()
        x0 = int(self.x0_entry.get())
        y0 = int(self.y0_entry.get())
        x1 = int(self.x1_entry.get())
        y1 = int(self.y1_entry.get())
        start_x, start_y = x0, y0
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            x = x0
            y = y0
            self.paint_rectangle(x, y, "blue")

            if x0 == x1 and y0 == y1:
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

        self.canvas.create_line(self.to_canvas_coords(start_x, start_y), self.to_canvas_coords(x1, y1))

    def draw_grid(self):
        for x in range(self.canvas.winfo_width() // 2, 0, -self.scale):
            self.canvas.create_line(x, 0, x, self.canvas.winfo_height(), fill="lightgray")
        for x in range(self.canvas.winfo_width() // 2, self.canvas.winfo_width(), self.scale):
            self.canvas.create_line(x, 0, x, self.canvas.winfo_height(), fill="lightgray")
        for y in range(self.canvas.winfo_height() // 2, 0, -self.scale):
            self.canvas.create_line(0, y, self.canvas.winfo_width(), y, fill="lightgray")
        for y in range(self.canvas.winfo_height() // 2, self.canvas.winfo_height(), self.scale):
            self.canvas.create_line(0, y, self.canvas.winfo_width(), y, fill="lightgray")

    def draw_axes(self):
        self.canvas.create_line(0, self.canvas.winfo_height() // 2, self.canvas.winfo_width(),
                                self.canvas.winfo_height() // 2, fill="black", width=2)
        self.canvas.create_line(self.canvas.winfo_width() // 2, 0, self.canvas.winfo_width() // 2,
                                self.canvas.winfo_height(), fill="black", width=2)

        for x in range(0, self.canvas.winfo_width() // self.scale + 1,
                       max(1, 20 // self.scale)):
            canvas_x = self.to_canvas_coords(x, 0)[0]
            self.canvas.create_text(canvas_x, self.canvas.winfo_height() // 2 + 10, text=str(x))
        for x in range(0, -self.canvas.winfo_width() // self.scale + 1,
                       -max(1, 20 // self.scale)):
            canvas_x = self.to_canvas_coords(x, 0)[0]
            self.canvas.create_text(canvas_x, self.canvas.winfo_height() // 2 + 10, text=str(x))

        for y in range(0, self.canvas.winfo_height() // self.scale + 1,
                       max(1, 20 // self.scale)):
            canvas_y = self.to_canvas_coords(0, y)[1]
            self.canvas.create_text(self.canvas.winfo_width() // 2 - 10, canvas_y, text=str(y))
        for y in range(0, -self.canvas.winfo_height() // self.scale + 1,
                       -max(1, 20 // self.scale)):
            canvas_y = self.to_canvas_coords(0, y)[1]
            self.canvas.create_text(self.canvas.winfo_width() // 2 - 10, canvas_y, text=str(y))

    def to_canvas_coords(self, x, y):
        canvas_x = self.canvas.winfo_width() // 2 + x * self.scale
        canvas_y = self.canvas.winfo_height() // 2 - y * self.scale
        return canvas_x, canvas_y

    def paint_rectangle(self, x, y, color):
        x = self.canvas.winfo_width() // 2 + x * self.scale
        y = self.canvas.winfo_height() // 2 - y * self.scale
        self.canvas.create_rectangle(x, y, x + self.scale, y - self.scale, outline=color, fill=color)


if __name__ == "__main__":
    app = RasterAlgorithmApp()
