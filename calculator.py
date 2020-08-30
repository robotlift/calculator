import functools as ft
import numexpr as ne
import tkinter as tk
import tkinter.ttk as ttk


class Display(ttk.LabelFrame):
    """Display portion of the calculator, contains 2 displays. Top display shows the evaluated expression, bottom display shows the unevaluated expression."""
    
    def __init__(self, master):
        super().__init__(master=master, text='DISPLAY')
        # Anchor must be e/w (east/west) in order for the text in the displays to be flushed right/left respectively.
        self.top_display = ttk.Label(anchor='e', master=self, relief='solid')
        self.bottom_display = ttk.Label(anchor='w', master=self, relief='solid')
        # Evenly distribute the free space to the displays.
        self.top_display.pack(expand=True, fill='both', pady=1)
        self.bottom_display.pack(expand=True, fill='both', pady=1)


class Keypad(ttk.LabelFrame):
    """The keypad portion of the calculator."""
    
    NUM_ROWS = 6
    NUM_COLS = 4
    LAYOUT = [
        ['Delete', '(', ')', 'Backspace'],
        ['j', 'e', '_', '%'],
        ['7', '8', '9', '/'],
        ['4', '5', '6', '*'],
        ['1', '2', '3', '-'],
        ['0', '.', '=', '+']
    ]
    
    def __init__(self, master, display):
        super().__init__(master=master, text='KEYPAD')
        self.display = display
        # Create the keypad using the layout.
        for ii, row in enumerate(iterable=self.LAYOUT):
            for jj, notation in enumerate(iterable=row):
                if notation == 'Delete':
                    command = self.delete
                elif notation == 'Backspace':
                    command = self.backspace
                elif notation == '=':
                    command = self.evaluate
                else:
                    command = ft.partial(self.append, notation)
                key = ttk.Button(command=command, master=self, text=notation)
                # Sticky must be nsew (north south east west) in order for the keys to accept the free space from all directions.
                key.grid(column=jj, row=ii, sticky='nsew')
        # Evenly distribute the free vertical space to the keys.
        for index in range(self.NUM_ROWS):
            self.grid_rowconfigure(index=index, weight=1)
        # Evenly distribute the free horizontal space to the keys.
        for index in range(self.NUM_COLS):
            self.grid_columnconfigure(index=index, weight=1)
    
    def append(self, notation):
        """Append a notation to the text in the bottom display."""
        text = self.display.bottom_display.cget(key='text') + notation
        self.display.bottom_display.configure(text=text)
    
    def backspace(self):
        """Delete the last notation from the text in the bottom display."""
        text = self.display.bottom_display.cget(key='text')
        if text:
            self.display.bottom_display.configure(text=text[:-1])
    
    def delete(self):
        """Delete all nontations from the text in the bottom display."""
        self.display.bottom_display.configure(text='')
    
    def evaluate(self):
        """Evaluate the expression in the bottom display."""
        expression = self.display.bottom_display.cget(key='text')
        try:
            text = ne.evaluate(ex=expression)
        except Exception as exception:
            text = str(object=exception.__class__)[8:-2]
        self.display.top_display.configure(text=text)


class Calculator(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.display = Display(master=self)
        self.keypad = Keypad(display=self.display, master=self)
        # Sticky must be nsew (north south east west) in order for display and keypad to accept the free space from all directions.
        self.display.grid(column=0, row=0, sticky='nsew')
        self.keypad.grid(column=0, row=1, sticky='nsew')
        # distribute all free vertical space to the display and keypad in a ratio of 1:3
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=1, weight=3)
        # evenly distribute all free horizontal space to the display and keypad
        self.grid_columnconfigure(index=0, weight=1)


def main():
    root = tk.Tk()
    calculator = Calculator(master=root)
    root.title(string='Calculator')
    # Evenly distribute the free space to the calculator.
    calculator.pack(expand=True, fill='both')
    # Create a minimum size for calculator, must do it after packing calculator.
    root.update()
    root.minsize(height=root.winfo_height(), width=root.winfo_width())
    root.mainloop()


if __name__ == '__main__':
    main()
