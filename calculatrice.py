import tkinter as tk
from tkinter import font
import math

#  MAIN  CLASS 
class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title(" Calculator ✨")
        self.root.geometry("420x700")
        self.root.configure(bg='#ffd1dc')  
        self.root.resizable(False, False)
        
        #  color scheme
        self.colors = {
            'bg': '#ffd1dc',            
            'display_bg': '#ffffff',    
            'display_fg': '#ff69b4',    
            'btn_bg': '#ffb6c1',        
            'btn_fg': '#8b008b',        
            'operator_bg': '#ff69b4',   
            'clear_bg': '#9370db',      
            'equals_bg': '#ba55d3',     
            'highlight': '#ff1493',     
            'accent': '#ffffff',        
            'border': '#ff69b4'         
        }
        
        # Cute fonts
        self.display_font = font.Font(family='Comic Sans MS', size=28, weight='bold')
        self.btn_font = font.Font(family='Comic Sans MS', size=16, weight='bold')
        self.mode_font = font.Font(family='Comic Sans MS', size=11, weight='bold')
        self.title_font = font.Font(family='Comic Sans MS', size=20, weight='bold')
        
        # Initialize navigation buttons list
        self.nav_buttons = []
        
        #  cute title
        self.create_title()
        
        # Create container for pages
        self.container = tk.Frame(self.root, bg=self.colors['bg'], highlightbackground=self.colors['border'], 
                                 highlightthickness=2, highlightcolor=self.colors['border'])
        self.container.pack(fill="both", expand=True, padx=15, pady=5)
        
        # Create navigation bar
        self.create_navigation()
        
        # Initialize pages
        self.pages = {}
        self.current_page = None
        
        # Create all pages
        self.create_pages()
        
        # Show the standard calculator by default
        self.show_page("Standard")
        
        #  Hello Kitty decoration
        self.add_decoration()
    
    def create_title(self):
        """Create cute title with Hello Kitty theme"""
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(fill="x", pady=(10, 0))
        
        title_label = tk.Label(
            title_frame,
            text="🌸  Calculator 🌸",
            font=self.title_font,
            bg=self.colors['bg'],
            fg='#ff1493',  
            pady=5
        )
        title_label.pack()
        
        # Add cute divider
        divider = tk.Frame(title_frame, height=2, bg='#ff69b4', relief='raised')
        divider.pack(fill='x', padx=30, pady=5)
    
    def add_decoration(self):
        """Add cute Hello Kitty decorations"""
        # Left decoration
        left_decoration = tk.Label(
            self.root,
            text="(>^ω^<)ﾉ",
            font=('Comic Sans MS', 12),
            bg=self.colors['bg'],
            fg='#ff69b4'
        )
        left_decoration.place(x=10, y=50)
        
        # Right decoration
        right_decoration = tk.Label(
            self.root,
            text="(◕‿◕✿)",
            font=('Comic Sans MS', 12),
            bg=self.colors['bg'],
            fg='#ff69b4'
        )
        right_decoration.place(x=350, y=50)
        
        # Bottom decoration
        bottom_decoration = tk.Label(
            self.root,
            text="✧･ﾟ: *✧･ﾟ:*  Magical Calculator  *:･ﾟ✧*:･ﾟ✧",
            font=('Comic Sans MS', 9),
            bg=self.colors['bg'],
            fg='#9370db'
        )
        bottom_decoration.place(x=50, y=670)
    
    def create_pages(self):
        """Create all calculator pages"""
        # Standard Calculator
        self.pages["Standard"] = StandardCalculator(self.container, self)
        
        # Scientific Calculator
        self.pages["Scientific"] = ScientificCalculator(self.container, self)
        
        # Programmer Calculator
        self.pages["Programmer"] = ProgrammerCalculator(self.container, self)
    
    def show_page(self, page_name):
        """Switch between different calculator pages"""
        if self.current_page:
            self.current_page.pack_forget()
        
        self.current_page = self.pages[page_name]
        self.current_page.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Update navigation highlighting
        for btn in self.nav_buttons:
            if btn["text"] == page_name:
                btn.configure(bg=self.colors['highlight'], fg=self.colors['accent'])
            else:
                btn.configure(bg=self.colors['btn_bg'], fg=self.colors['btn_fg'])
    
    def create_navigation(self):
        """Create cute navigation buttons"""
        nav_frame = tk.Frame(self.root, bg=self.colors['bg'], height=40)
        nav_frame.pack(fill="x", padx=20, pady=(5, 10))
        
        modes = ["🌸 Standard", "✨ Scientific", "🎀 Programmer"]
        
        for mode in modes:
            btn = tk.Button(
                nav_frame,
                text=mode,
                font=self.mode_font,
                bg=self.colors['btn_bg'],
                fg=self.colors['btn_fg'],
                activebackground=self.colors['highlight'],
                activeforeground=self.colors['accent'],
                relief='raised',
                borderwidth=2,
                padx=15,
                pady=3,
                cursor='heart',
                command=lambda m=mode.replace("🌸 ", "").replace("✨ ", "").replace("🎀 ", ""): self.show_page(m)
            )
            btn.pack(side='left', padx=5)
            self.nav_buttons.append(btn)


#  BASE CALCULATOR CLASS 
class BaseCalculator(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.colors['bg'], highlightbackground=app.colors['border'], 
                        highlightthickness=1, highlightcolor=app.colors['border'])
        self.app = app
        self.current_input = ""
        self.expression = ""
        self.create_widgets()
    
    def create_widgets(self):
        """To be overridden by child classes"""
        pass
    
    def update_display(self, value=None):
        """Update the display with current input"""
        if value is not None:
            self.display_var.set(value)
        else:
            # Truncate to 20 characters for display
            display_text = self.current_input[:20]
            self.display_var.set(display_text)
    
    def button_click(self, char):
        """Handle button clicks"""
        if char == 'C':
            self.current_input = ""
            self.expression = ""
        elif char == '⌫':
            self.current_input = self.current_input[:-1]
        elif char == '=':
            try:
                # Safely evaluate the expression
                self.expression = self.current_input
                # Replace visual operators with Python operators
                eval_expr = self.expression.replace('×', '*').replace('÷', '/')
                result = str(eval(eval_expr))
                self.current_input = result
                self.expression = ""
            except:
                self.current_input = "Error 💕"
        else:
            self.current_input += str(char)
        
        self.update_display()
    
    def create_button(self, parent, text, command=None, bg=None, fg=None, width=5, height=2):
        """Create a cute styled button"""
        if bg is None:
            bg = self.app.colors['btn_bg']
        if fg is None:
            fg = self.app.colors['btn_fg']
        
        btn = tk.Button(
            parent,
            text=text,
            font=self.app.btn_font,
            bg=bg,
            fg=fg,
            activebackground='#ffa6b9',
            activeforeground=fg,
            relief='raised',
            borderwidth=3,
            cursor='heart',
            width=width,
            height=height,
            command=command
        )
        return btn


#  STANDARD CALCULATOR 
class StandardCalculator(BaseCalculator):
    def create_widgets(self):
        # Create cute display frame
        display_frame = tk.Frame(self, bg=self.app.colors['accent'], highlightbackground=self.app.colors['border'], 
                                highlightthickness=2, highlightcolor=self.app.colors['border'])
        display_frame.pack(fill="x", padx=10, pady=10)
        
        # Add cute corner decorations
        corner_label = tk.Label(
            display_frame,
            text="◠◡◠",
            font=('Comic Sans MS', 8),
            bg=self.app.colors['accent'],
            fg=self.app.colors['border']
        )
        corner_label.pack(anchor='ne', padx=5, pady=2)
        
        self.display_var = tk.StringVar(value="0")
        display_label = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=self.app.display_font,
            bg=self.app.colors['display_bg'],
            fg=self.app.colors['display_fg'],
            anchor="e",
            padx=20,
            pady=15,
            relief='sunken',
            borderwidth=2
        )
        display_label.pack(fill="x", padx=10, pady=5)
        
        # Create cute buttons grid
        button_frame = tk.Frame(self, bg=self.app.colors['bg'])
        button_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Button layout
        buttons = [
            ['C', '⌫', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['00', '0', '.', '=']
        ]
        
        # Button colors and emojis
        button_style = {
            'C': {'bg': self.app.colors['clear_bg'], 'fg': self.app.colors['accent'], 'text': 'C 🗑️'},
            '⌫': {'bg': '#ffa6b9', 'fg': self.app.colors['btn_fg'], 'text': '⌫ ✨'},
            '%': {'bg': '#ffa6b9', 'fg': self.app.colors['btn_fg'], 'text': '% 🌟'},
            '÷': {'bg': self.app.colors['operator_bg'], 'fg': self.app.colors['accent'], 'text': '÷ 💖'},
            '×': {'bg': self.app.colors['operator_bg'], 'fg': self.app.colors['accent'], 'text': '× 💖'},
            '-': {'bg': self.app.colors['operator_bg'], 'fg': self.app.colors['accent'], 'text': '- 💖'},
            '+': {'bg': self.app.colors['operator_bg'], 'fg': self.app.colors['accent'], 'text': '+ 💖'},
            '=': {'bg': self.app.colors['equals_bg'], 'fg': self.app.colors['accent'], 'text': '= 💝'},
            '7': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '7'},
            '8': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '8'},
            '9': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '9'},
            '4': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '4'},
            '5': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '5'},
            '6': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '6'},
            '1': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '1'},
            '2': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '2'},
            '3': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '3'},
            '00': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '00'},
            '0': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '0'},
            '.': {'bg': '#ffa6b9', 'fg': self.app.colors['btn_fg'], 'text': '. 🌸'}
        }
        
        # Create cute buttons
        for i, row in enumerate(buttons):
            button_frame.rowconfigure(i, weight=1)
            for j, btn_key in enumerate(row):
                button_frame.columnconfigure(j, weight=1)
                
                style = button_style[btn_key]
                
                btn = self.create_button(
                    button_frame,
                    style['text'],
                    command=lambda t=btn_key: self.button_click(t),
                    bg=style['bg'],
                    fg=style['fg']
                )
                btn.grid(row=i, column=j, padx=3, pady=3, sticky="nsew")


#  SCIENTIFIC CALCULATOR 
class ScientificCalculator(BaseCalculator):
    def create_widgets(self):
        # Create cute display
        display_frame = tk.Frame(self, bg=self.app.colors['accent'], highlightbackground=self.app.colors['border'], 
                                highlightthickness=2, highlightcolor=self.app.colors['border'])
        display_frame.pack(fill="x", padx=10, pady=10)
        
        # Add cute corner
        corner_label = tk.Label(
            display_frame,
            text="☆.｡･:*:･ﾟ★",
            font=('Comic Sans MS', 8),
            bg=self.app.colors['accent'],
            fg=self.app.colors['border']
        )
        corner_label.pack(anchor='ne', padx=5, pady=2)
        
        self.display_var = tk.StringVar(value="0")
        display_label = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=self.app.display_font,
            bg=self.app.colors['display_bg'],
            fg=self.app.colors['display_fg'],
            anchor="e",
            padx=20,
            pady=15,
            relief='sunken',
            borderwidth=2
        )
        display_label.pack(fill="x", padx=10, pady=5)
        
        # Create cute buttons grid
        button_frame = tk.Frame(self, bg=self.app.colors['bg'])
        button_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scientific button layout
        buttons = [
            ['C', '⌫', '%', '÷', 'sin', 'cos'],
            ['7', '8', '9', '×', 'tan', 'log'],
            ['4', '5', '6', '-', '√', 'x²'],
            ['1', '2', '3', '+', 'π', 'e'],
            ['00', '0', '.', '=', '(', ')']
        ]
        
        # Scientific button styles with emojis
        sci_styles = {
            'C': {'bg': self.app.colors['clear_bg'], 'fg': self.app.colors['accent'], 'text': 'C 🗑️'},
            '⌫': {'bg': '#ffa6b9', 'fg': self.app.colors['btn_fg'], 'text': '⌫ ✨'},
            '%': {'bg': '#ffa6b9', 'fg': self.app.colors['btn_fg'], 'text': '% 🌟'},
            '÷': {'bg': self.app.colors['operator_bg'], 'fg': self.app.colors['accent'], 'text': '÷ 💖'},
            '×': {'bg': self.app.colors['operator_bg'], 'fg': self.app.colors['accent'], 'text': '× 💖'},
            '-': {'bg': self.app.colors['operator_bg'], 'fg': self.app.colors['accent'], 'text': '- 💖'},
            '+': {'bg': self.app.colors['operator_bg'], 'fg': self.app.colors['accent'], 'text': '+ 💖'},
            '=': {'bg': self.app.colors['equals_bg'], 'fg': self.app.colors['accent'], 'text': '= 💝'},
            'sin': {'bg': '#dda0dd', 'fg': self.app.colors['accent'], 'text': 'sin 🌈'},
            'cos': {'bg': '#dda0dd', 'fg': self.app.colors['accent'], 'text': 'cos 🌈'},
            'tan': {'bg': '#dda0dd', 'fg': self.app.colors['accent'], 'text': 'tan 🌈'},
            'log': {'bg': '#dda0dd', 'fg': self.app.colors['accent'], 'text': 'log 🌟'},
            '√': {'bg': '#dda0dd', 'fg': self.app.colors['accent'], 'text': '√ 🌸'},
            'x²': {'bg': '#dda0dd', 'fg': self.app.colors['accent'], 'text': 'x² 🌸'},
            'π': {'bg': '#b0e0e6', 'fg': self.app.colors['btn_fg'], 'text': 'π 🦄'},
            'e': {'bg': '#b0e0e6', 'fg': self.app.colors['btn_fg'], 'text': 'e 🦄'},
            '(': {'bg': '#b0e0e6', 'fg': self.app.colors['btn_fg'], 'text': '( 🎀'},
            ')': {'bg': '#b0e0e6', 'fg': self.app.colors['btn_fg'], 'text': ') 🎀'},
            '7': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '7'},
            '8': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '8'},
            '9': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '9'},
            '4': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '4'},
            '5': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '5'},
            '6': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '6'},
            '1': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '1'},
            '2': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '2'},
            '3': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '3'},
            '00': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '00'},
            '0': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '0'},
            '.': {'bg': '#ffa6b9', 'fg': self.app.colors['btn_fg'], 'text': '. 🌸'}
        }
        
        # Create cute scientific buttons
        for i, row in enumerate(buttons):
            button_frame.rowconfigure(i, weight=1)
            for j, btn_key in enumerate(row):
                button_frame.columnconfigure(j, weight=1)
                
                style = sci_styles[btn_key]
                
                btn = self.create_button(
                    button_frame,
                    style['text'],
                    command=lambda t=btn_key: self.scientific_button_click(t),
                    bg=style['bg'],
                    fg=style['fg'],
                    width=4
                )
                btn.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")
    
    def scientific_button_click(self, char):
        """Handle scientific calculator button clicks"""
        if char in ['sin', 'cos', 'tan', 'log', '√', 'x²']:
            try:
                value = float(self.current_input) if self.current_input else 0
                if char == 'sin':
                    result = math.sin(math.radians(value))
                elif char == 'cos':
                    result = math.cos(math.radians(value))
                elif char == 'tan':
                    result = math.tan(math.radians(value))
                elif char == 'log':
                    result = math.log10(value) if value > 0 else "Error 💔"
                elif char == '√':
                    result = math.sqrt(value) if value >= 0 else "Error 💔"
                elif char == 'x²':
                    result = value ** 2
                
                if result != "Error 💔":
                    self.current_input = str(round(result, 10))
                else:
                    self.current_input = result
            except:
                self.current_input = "Error 💔"
        elif char == 'π':
            self.current_input += str(math.pi)
        elif char == 'e':
            self.current_input += str(math.e)
        elif char == '(':
            self.current_input += '('
        elif char == ')':
            self.current_input += ')'
        else:
            self.button_click(char)
        
        self.update_display()


# PROGRAMMER CALCULATOR 
class ProgrammerCalculator(BaseCalculator):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.base = 10  # Default base (decimal)
    
    def create_widgets(self):
        # Create cute display with base indicator
        top_frame = tk.Frame(self, bg=self.app.colors['bg'])
        top_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        # Base selector with cute labels
        base_frame = tk.Frame(top_frame, bg=self.app.colors['bg'], highlightbackground=self.app.colors['border'], 
                             highlightthickness=1, highlightcolor=self.app.colors['border'])
        base_frame.pack(side='left')
        
        bases = [("HEX 🎀", 16), ("DEC 🌸", 10), ("OCT ✨", 8), ("BIN 🌟", 2)]
        self.base_var = tk.IntVar(value=10)
        
        for text, value in bases:
            rb = tk.Radiobutton(
                base_frame,
                text=text,
                variable=self.base_var,
                value=value,
                command=self.change_base,
                font=self.app.mode_font,
                bg=self.app.colors['bg'],
                fg=self.app.colors['btn_fg'],
                selectcolor=self.app.colors['highlight'],
                activebackground=self.app.colors['bg'],
                activeforeground=self.app.colors['btn_fg'],
                indicatoron=0,
                width=8,
                relief='raised',
                borderwidth=2
            )
            rb.pack(side='left', padx=2)
        
        # Display frame
        display_frame = tk.Frame(self, bg=self.app.colors['accent'], highlightbackground=self.app.colors['border'], 
                                highlightthickness=2, highlightcolor=self.app.colors['border'])
        display_frame.pack(fill="x", padx=10, pady=10)
        
        # Cute corner decoration
        corner_label = tk.Label(
            display_frame,
            text="(◕ᴗ◕✿)",
            font=('Comic Sans MS', 8),
            bg=self.app.colors['accent'],
            fg=self.app.colors['border']
        )
        corner_label.pack(anchor='ne', padx=5, pady=2)
        
        self.display_var = tk.StringVar(value="0")
        display_label = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=self.app.display_font,
            bg=self.app.colors['display_bg'],
            fg=self.app.colors['display_fg'],
            anchor="e",
            padx=20,
            pady=15,
            relief='sunken',
            borderwidth=2
        )
        display_label.pack(fill="x", padx=10, pady=5)
        
        # Bit display
        self.bit_var = tk.StringVar(value="")
        bit_label = tk.Label(
            display_frame,
            textvariable=self.bit_var,
            font=('Comic Sans MS', 9),
            bg=self.app.colors['accent'],
            fg='#9370db',
            anchor="e",
            padx=20
        )
        bit_label.pack(fill="x", padx=10)
        
        # Create cute buttons grid
        button_frame = tk.Frame(self, bg=self.app.colors['bg'])
        button_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Programmer button layout
        buttons = [
            ['C', '⌫', '<<', '>>', 'AND', 'OR'],
            ['A', 'B', 'C', 'D', 'XOR', 'NOT'],
            ['7', '8', '9', 'E', 'F', 'MOD'],
            ['4', '5', '6', '(', ')', '%'],
            ['1', '2', '3', '+', '-', '='],
            ['00', '0', '.', '×', '÷', '']
        ]
        
        # Programmer button styles
        prog_styles = {
            'C': {'bg': self.app.colors['clear_bg'], 'fg': self.app.colors['accent'], 'text': 'C 🗑️'},
            '⌫': {'bg': '#ffa6b9', 'fg': self.app.colors['btn_fg'], 'text': '⌫ ✨'},
            '<<': {'bg': '#ff69b4', 'fg': self.app.colors['accent'], 'text': '<< 🎯'},
            '>>': {'bg': '#ff69b4', 'fg': self.app.colors['accent'], 'text': '>> 🎯'},
            'AND': {'bg': '#ff69b4', 'fg': self.app.colors['accent'], 'text': 'AND 💝'},
            'OR': {'bg': '#ff69b4', 'fg': self.app.colors['accent'], 'text': 'OR 💝'},
            'XOR': {'bg': '#ff69b4', 'fg': self.app.colors['accent'], 'text': 'XOR 💝'},
            'NOT': {'bg': '#ff69b4', 'fg': self.app.colors['accent'], 'text': 'NOT 💝'},
            'MOD': {'bg': '#ff69b4', 'fg': self.app.colors['accent'], 'text': 'MOD ✨'},
            '=': {'bg': self.app.colors['equals_bg'], 'fg': self.app.colors['accent'], 'text': '= 💝'},
            'A': {'bg': '#dda0dd', 'fg': self.app.colors['accent'], 'text': 'A 💜'},
            'B': {'bg': '#dda0dd', 'fg': self.app.colors['accent'], 'text': 'B 💜'},
            'C': {'bg': '#dda0dd', 'fg': self.app.colors['accent'], 'text': 'C 💜'},
            'D': {'bg': '#dda0dd', 'fg': self.app.colors['accent'], 'text': 'D 💜'},
            'E': {'bg': '#dda0dd', 'fg': self.app.colors['accent'], 'text': 'E 💜'},
            'F': {'bg': '#dda0dd', 'fg': self.app.colors['accent'], 'text': 'F 💜'},
            '7': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '7'},
            '8': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '8'},
            '9': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '9'},
            '4': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '4'},
            '5': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '5'},
            '6': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '6'},
            '1': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '1'},
            '2': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '2'},
            '3': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '3'},
            '00': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '00'},
            '0': {'bg': '#ffc0cb', 'fg': self.app.colors['btn_fg'], 'text': '0'},
            '.': {'bg': '#ffa6b9', 'fg': self.app.colors['btn_fg'], 'text': '. 🌸'},
            '(': {'bg': '#b0e0e6', 'fg': self.app.colors['btn_fg'], 'text': '( 🎀'},
            ')': {'bg': '#b0e0e6', 'fg': self.app.colors['btn_fg'], 'text': ') 🎀'},
            '+': {'bg': self.app.colors['operator_bg'], 'fg': self.app.colors['accent'], 'text': '+ 💖'},
            '-': {'bg': self.app.colors['operator_bg'], 'fg': self.app.colors['accent'], 'text': '- 💖'},
            '×': {'bg': self.app.colors['operator_bg'], 'fg': self.app.colors['accent'], 'text': '× 💖'},
            '÷': {'bg': self.app.colors['operator_bg'], 'fg': self.app.colors['accent'], 'text': '÷ 💖'},
            '%': {'bg': '#ffa6b9', 'fg': self.app.colors['btn_fg'], 'text': '% 🌟'},
            '': {'bg': self.app.colors['bg'], 'fg': self.app.colors['bg'], 'text': ''}
        }
        
        # Create cute programmer buttons
        for i, row in enumerate(buttons):
            button_frame.rowconfigure(i, weight=1)
            for j, btn_key in enumerate(row):
                button_frame.columnconfigure(j, weight=1)
                
                style = prog_styles[btn_key]
                
                btn = self.create_button(
                    button_frame,
                    style['text'],
                    command=lambda t=btn_key: self.programmer_button_click(t),
                    bg=style['bg'],
                    fg=style['fg'],
                    width=4
                )
                btn.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")
    
    def change_base(self):
        """Change the number base (HEX, DEC, OCT, BIN)"""
        self.base = self.base_var.get()
        self.update_display_from_base()
    
    def update_display_from_base(self):
        """Update display based on current base"""
        try:
            if self.current_input:
                if self.base == 10:
                    # Already in decimal
                    self.update_display()
                elif self.base == 16:
                    # Convert to hex
                    dec_value = int(float(self.current_input))
                    hex_value = hex(dec_value)[2:].upper()
                    self.display_var.set(hex_value)
                elif self.base == 8:
                    # Convert to octal
                    dec_value = int(float(self.current_input))
                    oct_value = oct(dec_value)[2:]
                    self.display_var.set(oct_value)
                elif self.base == 2:
                    # Convert to binary
                    dec_value = int(float(self.current_input))
                    bin_value = bin(dec_value)[2:]
                    # Show only first 16 bits for display
                    if len(bin_value) > 16:
                        bin_value = bin_value[-16:]
                        self.bit_var.set(f"🎀 16-bit: {bin_value}")
                    else:
                        self.bit_var.set(f"🎀 16-bit: {bin_value:>16}")
                    self.display_var.set(bin_value)
        except:
            self.display_var.set("Error 💔")
    
    def programmer_button_click(self, char):
        """Handle programmer calculator button clicks"""
        if char in ['A', 'B', 'C', 'D', 'E', 'F']:
            if self.base == 16:
                self.current_input += char
        elif char in ['AND', 'OR', 'XOR', 'NOT', '<<', '>>', 'MOD']:
            self.current_input += f" {char} "
        else:
            self.button_click(char)
        
        self.update_display_from_base()


# MAIN EXECUTION 
if __name__ == "__main__":
    root = tk.Tk()
    
    # Add cute icon (if available)
    try:
        root.iconbitmap('kitty.ico')  # You can create a cute icon file
    except:
        pass
    
    app = CalculatorApp(root)
    root.mainloop()