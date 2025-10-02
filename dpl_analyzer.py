import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math
import os
import warnings
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 9
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['axes.edgecolor'] = '#000000'
plt.rcParams['xtick.color'] = '#000000'
plt.rcParams['ytick.color'] = '#000000'
plt.rcParams['figure.facecolor'] = '#FFFFFF'
plt.rcParams['axes.facecolor'] = '#FFFFFF'
class CustomMessageBox:
    @staticmethod
    def showerror(message, title="Błąd"):
        return messagebox.showerror(f"{title}", message)
    @staticmethod
    def showwarning(message, title="Uwaga"):
        return messagebox.showwarning(f"{title}", message)
    @staticmethod
    def showinfo(message, title="Informacja"):
        return messagebox.showinfo(f"{title}", message)
    @staticmethod
    def askyesno(message, title="Potwierdzenie"):
        return messagebox.askyesno(f"{title}", message)
    @staticmethod
    def showsuccess(message, title="Sukces"):
        return messagebox.showinfo(f"{title}", message)
class DPLAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizator DPL - Zagęszczenie gruntu v2.0")
        self.root.state('zoomed')
        self.colors = {
            'primary': '#2E3440',
            'secondary': '#3B4252',
            'accent': '#5E81AC',
            'success': '#A3BE8C',
            'warning': '#EBCB8B',
            'error': '#BF616A',
            'info': '#88C0D0',
            'background': '#111113',
            'surface': '#212225',
            'text_primary': '#E5E9F0',
            'text_secondary': '#D8DEE9',
            'border': '#2a2d32',
            'highlight': '#272a2d',
            'table_alt': '#1a1c1f',
            'button_background': '#212225',
            'button_border': '#43484e'
        }
        self._configure_modern_style()
        self.depth_validate = self.root.register(self._validate_depth_input)
        self.n10_validate = self.root.register(self._validate_n10_input)
        class DummyVar:
            def set(self, value): pass
            def get(self): return ""
        self.status_var = DummyVar()
        self.shortcuts_var = DummyVar()
        self.data_info_var = DummyVar()
        self.data = []
        self.next_order = 1
        self.profile_layers = []
        self.next_profile_id = 1
        self.sort_column = "Głęb. (m)"
        self.sort_reverse = False
        self.profile_sort_column = "Głęb. (m)"
        self.profile_sort_reverse = False
        self.ax = None
        self._setup_gui()
    def _configure_modern_style(self):
        self.root.configure(bg=self.colors['background'])
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except:
            pass
        style.configure('Modern.TButton',
                       background=self.colors['button_background'],
                       foreground='white',
                       borderwidth=1,
                       focuscolor='none',
                       relief='solid',
                       bordercolor=self.colors['button_border'],
                       padding=(12, 8),
                       font=('Segoe UI', 9, 'bold'))
        style.map('Modern.TButton',
                 background=[('active', '#272a2d'),
                           ('pressed', '#272a2d'),
                           ('focus', '#272a2d')],
                 foreground=[('active', 'white'),
                           ('pressed', 'white'),
                           ('focus', 'white')],
                 borderwidth=[('active', 0.5),
                            ('pressed', 0.5),
                            ('focus', 0.5)])
        style.configure('Modern.TLabelframe',
                       background=self.colors['background'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=self.colors['border'])
        style.configure('Modern.TLabelframe.Label',
                       background=self.colors['background'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 9, 'bold'))
        style.configure('Modern.TEntry',
                       background=self.colors['background'],
                       fieldbackground=self.colors['background'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor='#363a3f',
                       insertcolor=self.colors['text_primary'],
                       foreground=self.colors['text_primary'],
                       focuscolor='none',
                       highlightcolor='#363a3f',
                       selectbackground=self.colors['accent'],
                       selectforeground='white')
        style.map('Modern.TEntry',
                 bordercolor=[('active', '#363a3f'),
                            ('focus', '#363a3f')],
                 focuscolor=[('active', 'none'),
                           ('focus', 'none')])
        style.configure('Modern.Treeview',
                       background=self.colors['surface'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['surface'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=self.colors['border'],
                       rowheight=40)
        style.configure('Modern.Treeview.Heading',
                       background=self.colors['button_background'],
                       foreground='white',
                       relief='solid',
                       borderwidth=1,
                       bordercolor=self.colors['border'],
                       font=('Segoe UI', 9, 'bold'))
        style.map('Modern.Treeview.Heading',
                 background=[('active', self.colors['highlight']),
                           ('pressed', self.colors['highlight'])],
                 foreground=[('active', 'white'),
                           ('pressed', 'white')])
        style.map('Modern.Treeview',
                 background=[('selected', self.colors['highlight']),
                           ('focus', self.colors['secondary'])],
                 foreground=[('selected', 'white'),
                           ('focus', self.colors['text_primary'])])
        style.configure('Modern.TLabel',
                       background=self.colors['background'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 9))
        style.configure('Modern.TFrame',
                       background=self.colors['background'],
                       borderwidth=0)
        style.configure('Bordered.TFrame',
                       background=self.colors['background'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=self.colors['border'])
        style.configure('Modern.Vertical.TScrollbar',
                       background='#4a5568',
                       troughcolor='#1a202c',
                       borderwidth=2,
                       relief='solid',
                       bordercolor='#2d3748',
                       lightcolor='#4a5568',
                       darkcolor='#2d3748',
                       arrowcolor='#e2e8f0',
                       width=16)
        style.map('Modern.Vertical.TScrollbar',
                 background=[('active', '#718096'),
                           ('pressed', '#5e81ac')],
                 arrowcolor=[('active', '#ffffff'),
                           ('pressed', '#ffffff')],
                 bordercolor=[('active', '#4a5568'),
                            ('pressed', '#5e81ac')])
        style.configure('Modern.Horizontal.TScrollbar',
                       background='#4a5568',
                       troughcolor='#1a202c',
                       borderwidth=2,
                       relief='solid',
                       bordercolor='#2d3748',
                       lightcolor='#4a5568',
                       darkcolor='#2d3748',
                       arrowcolor='#e2e8f0',
                       width=16)
        style.map('Modern.Horizontal.TScrollbar',
                 background=[('active', '#718096'),
                           ('pressed', '#5e81ac')],
                 arrowcolor=[('active', '#ffffff'),
                           ('pressed', '#ffffff')],
                 bordercolor=[('active', '#4a5568'),
                            ('pressed', '#5e81ac')])
    def _setup_gui(self):
        main_frame = ttk.Frame(self.root, padding=2, style='Modern.TFrame')
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.configure(style='Modern.TFrame')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=0)
        main_frame.rowconfigure(2, weight=0)
        main_frame.rowconfigure(3, weight=1)
        self._create_input_section(main_frame)
        self._create_profile_section(main_frame)
        self._create_table_section(main_frame)
        self._create_plot_section(main_frame)
        self._setup_keyboard_shortcuts()
    def _create_input_section(self, parent):
        frame = ttk.LabelFrame(parent, text="", padding=5, style='Modern.TLabelframe')
        frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 0))
        frame.columnconfigure(0, weight=1)
        points_frame = ttk.Frame(frame, padding=5, style='Modern.TFrame')
        points_frame.grid(row=0, column=0, sticky="ew")
        points_frame.columnconfigure(0, weight=0, minsize=180)
        points_frame.columnconfigure(1, weight=0, minsize=180)
        points_frame.columnconfigure(2, weight=0, minsize=200)
        points_frame.columnconfigure(3, weight=0, minsize=120)
        points_frame.columnconfigure(4, weight=1, minsize=100)
        auto_frame = ttk.Frame(points_frame, style='Bordered.TFrame', padding=5)
        auto_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        auto_frame.columnconfigure(1, weight=1)
        auto_frame.columnconfigure(3, weight=1)
        ttk.Label(auto_frame, text="Głęb. (m) od:", style='Modern.TLabel').grid(row=1, column=0, sticky="w", padx=(0, 3))
        self.depth_from_var = tk.StringVar()
        self.depth_from_entry = ttk.Entry(auto_frame, textvariable=self.depth_from_var, width=8, style='Modern.TEntry',
                                          validate='key', validatecommand=(self.depth_validate, '%d', '%S', '%P'))
        self.depth_from_entry.grid(row=1, column=1, padx=(0, 8), sticky="ew")
        self.depth_from_entry.bind('<Return>', self.on_depth_from_enter)
        ttk.Label(auto_frame, text="Głęb. (m) do:", style='Modern.TLabel').grid(row=1, column=2, sticky="w", padx=(0, 3))
        self.depth_to_var = tk.StringVar()
        self.depth_to_entry = ttk.Entry(auto_frame, textvariable=self.depth_to_var, width=8, style='Modern.TEntry',
                                        validate='key', validatecommand=(self.depth_validate, '%d', '%S', '%P'))
        self.depth_to_entry.grid(row=1, column=3, sticky="ew")
        self.depth_to_entry.bind('<Return>', self.on_depth_to_enter)
        ttk.Button(auto_frame, text="Utwórz punkty", command=self.create_points_every_10cm, style='Modern.TButton').grid(row=2, column=0, columnspan=4, sticky="ew", pady=(3, 0))
        manual_frame = ttk.Frame(points_frame, style='Bordered.TFrame', padding=5)
        manual_frame.grid(row=0, column=1, sticky="nsew", padx=(4, 4))
        manual_frame.columnconfigure(1, weight=1)
        manual_frame.columnconfigure(3, weight=1)
        ttk.Label(manual_frame, text="Głęb. (m):", style='Modern.TLabel').grid(row=1, column=0, sticky="w", padx=(0, 3))
        self.depth_var = tk.StringVar()
        self.depth_entry = ttk.Entry(manual_frame, textvariable=self.depth_var, width=8, style='Modern.TEntry',
                                     validate='key', validatecommand=(self.depth_validate, '%d', '%S', '%P'))
        self.depth_entry.grid(row=1, column=1, padx=(0, 8), sticky="ew")
        self.depth_entry.bind('<Return>', lambda e: self.n10_entry.focus())
        ttk.Label(manual_frame, text="N₁₀:", style='Modern.TLabel').grid(row=1, column=2, sticky="w", padx=(0, 3))
        self.n10_var = tk.StringVar()
        self.n10_entry = ttk.Entry(manual_frame, textvariable=self.n10_var, width=8, style='Modern.TEntry',
                                   validate='key', validatecommand=(self.n10_validate, '%d', '%S', '%P'))
        self.n10_entry.grid(row=1, column=3, sticky="ew")
        self.n10_entry.bind('<Return>', self.add_point)
        ttk.Button(manual_frame, text="Utwórz punkt", command=self.add_point, style='Modern.TButton').grid(row=2, column=0, columnspan=4, sticky="ew", pady=(2, 0))
        add_layer_frame = ttk.Frame(points_frame, style='Bordered.TFrame', padding=5)
        add_layer_frame.grid(row=0, column=2, sticky="nsew", padx=(4, 4))
        add_layer_frame.columnconfigure(1, weight=1)
        add_layer_frame.columnconfigure(3, weight=1)
        ttk.Label(add_layer_frame, text="Głęb. (m) od:", style='Modern.TLabel').grid(row=0, column=0, sticky="w", padx=(0, 3))
        self.layer_from_var = tk.StringVar()
        self.layer_from_entry = ttk.Entry(add_layer_frame, textvariable=self.layer_from_var, width=8, style='Modern.TEntry',
                                          validate='key', validatecommand=(self.depth_validate, '%d', '%S', '%P'))
        self.layer_from_entry.grid(row=0, column=1, padx=(0, 8), sticky="ew")
        self.layer_from_entry.bind('<Return>', self.on_layer_from_enter)
        ttk.Label(add_layer_frame, text="Głęb. (m) do:", style='Modern.TLabel').grid(row=0, column=2, sticky="w", padx=(0, 3))
        self.layer_to_var = tk.StringVar()
        self.layer_to_entry = ttk.Entry(add_layer_frame, textvariable=self.layer_to_var, width=8, style='Modern.TEntry',
                                        validate='key', validatecommand=(self.depth_validate, '%d', '%S', '%P'))
        self.layer_to_entry.grid(row=0, column=3, sticky="ew")
        self.layer_to_entry.bind('<Return>', self.on_layer_to_enter)
        ttk.Label(add_layer_frame, text="Opis:", style='Modern.TLabel').grid(row=1, column=0, sticky="w", pady=(2, 0), padx=(0, 3))
        self.layer_description_var = tk.StringVar()
        self.layer_description_entry = ttk.Entry(add_layer_frame, textvariable=self.layer_description_var, style='Modern.TEntry')
        self.layer_description_entry.grid(row=1, column=1, columnspan=3, sticky="ew", pady=(2, 0))
        self.layer_description_entry.bind('<Return>', self.on_layer_description_enter)
        ttk.Button(add_layer_frame, text="Utwórz warstwę", command=self.add_profile_layer, style='Modern.TButton').grid(row=2, column=0, columnspan=4, sticky="ew", pady=(3, 0))
        action_frame = ttk.Frame(points_frame, style='Bordered.TFrame', padding=5)
        action_frame.grid(row=0, column=3, sticky="ns", padx=(8, 8))
        action_frame.columnconfigure(0, weight=1)
        action_frame.rowconfigure(0, weight=1)
        action_frame.rowconfigure(2, weight=1)
        ttk.Button(action_frame, text="Oblicz Id i Is", command=self.calculate_parameters, style='Modern.TButton').grid(row=1, column=0, sticky="ew")
        right_action_frame = ttk.Frame(points_frame, style='Modern.TFrame', padding=5)
        right_action_frame.grid(row=0, column=4, sticky="nse", padx=(8, 0))
        right_action_frame.columnconfigure(0, weight=1)
        ttk.Button(right_action_frame, text="Wyczyść wszystko", command=self.clear_all, style='Modern.TButton').grid(row=0, column=0, sticky="ne")
    def _create_profile_section(self, parent):
        """Tworzy panel z tabelą warstw geologicznych"""
        frame = ttk.LabelFrame(parent, text="", padding=5, style='Modern.TLabelframe')
        frame.grid(row=2, column=1, sticky="nsew", padx=(4, 0), pady=(0, 0))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        buttons_frame = ttk.Frame(frame, style='Modern.TFrame')
        buttons_frame.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        ttk.Button(buttons_frame, text="Usuń warstwę", command=self.remove_profile_layer, style='Modern.TButton').grid(row=0, column=0, padx=(0, 5))
        ttk.Button(buttons_frame, text="Wyczyść warstwy", command=self.clear_profile, style='Modern.TButton').grid(row=0, column=1)
        layers_frame = ttk.Frame(frame, style='Modern.TFrame')
        layers_frame.grid(row=1, column=0, sticky="nsew")
        layers_frame.columnconfigure(0, weight=1)
        layers_frame.columnconfigure(1, weight=0)
        layers_frame.rowconfigure(0, weight=1)
        profile_columns = ("lp.", "Głęb. (m)", "Opis")
        self.profile_tree = ttk.Treeview(layers_frame, columns=profile_columns, show='headings', style='Modern.Treeview', height=5)
        for col in profile_columns:
            self.profile_tree.heading(col, text=col, command=lambda c=col: self.sort_profile_by_column(c))
            if col == "lp.":
                width = 40
            elif col == "Głęb. (m)":
                width = 90
            else:
                width = 200
            self.profile_tree.column(col, width=width, anchor=tk.CENTER)
        self.profile_tree.tag_configure('alternate', background=self.colors['table_alt'], foreground=self.colors['text_primary'])
        self.profile_tree.grid(row=0, column=0, sticky="nsew")
        self.profile_scrollbar = ttk.Scrollbar(layers_frame, orient=tk.VERTICAL, command=self.profile_tree.yview, style='Modern.Vertical.TScrollbar')
        self.profile_tree.configure(yscrollcommand=self.profile_scrollbar.set)
        self.profile_scrollbar.grid(row=0, column=1, sticky="ns")
        self.profile_tree.bind('<Delete>', lambda e: self.remove_profile_layer())
        self.update_profile_scrollbar()
        self.update_profile_column_headers()
    def _create_table_section(self, parent):
        frame = ttk.LabelFrame(parent, text="", padding=5, style='Modern.TLabelframe')
        frame.grid(row=2, column=0, sticky="nsew", padx=(0, 4), pady=(0, 0))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        table_toolbar = ttk.Frame(frame, style='Modern.TFrame')
        table_toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        action_frame = ttk.Frame(table_toolbar, style='Modern.TFrame')
        action_frame.grid(row=0, column=0, sticky="w")
        ttk.Button(action_frame, text="Usuń punkt", command=self.remove_point, style='Modern.TButton').grid(row=0, column=0, padx=(0, 5))
        ttk.Button(action_frame, text="Wyczyść tabelę", command=self.clear_table, style='Modern.TButton').grid(row=0, column=1)
        columns = ("lp.", "Głęb. (m)", "N₁₀", "Id", "Is")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', style='Modern.Treeview', height=5)
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
            if col == "lp.":
                width = 50
            elif col == "Głęb. (m)":
                width = 90
            else:
                width = 100
            self.tree.column(col, width=width, anchor=tk.CENTER)
        self.tree.tag_configure('editing', background=self.colors['highlight'], foreground='white')
        self.tree.tag_configure('alternate', background=self.colors['table_alt'], foreground=self.colors['text_primary'])
        self.tree.grid(row=1, column=0, sticky="nsew")
        self.tree.bind('<Double-1>', self.start_inline_edit)
        self.tree.bind('<Button-1>', self.on_table_click)
        self.tree.bind('<Return>', self.start_inline_edit)
        self.tree.bind('<F2>', self.start_inline_edit)
        self.tree.bind('<MouseWheel>', self.on_tree_scroll)
        self.tree.bind('<Button-4>', self.on_tree_scroll)
        self.tree.bind('<Button-5>', self.on_tree_scroll)
        self.edit_var = tk.StringVar()
        self.edit_entry = ttk.Entry(self.tree, textvariable=self.edit_var, style='Modern.TEntry',
                                    validate='key', validatecommand=(self.n10_validate, '%d', '%S', '%P'))
        self.edit_entry.bind('<Return>', self.finish_edit_and_next)
        self.edit_entry.bind('<Shift-Return>', self.finish_edit_and_previous)
        self.edit_entry.bind('<Tab>', self.finish_edit_and_next)
        self.edit_entry.bind('<Shift-Tab>', self.finish_edit_and_previous)
        self.edit_entry.bind('<Control-d>', self.copy_from_previous)
        self.edit_entry.bind('<Escape>', self.cancel_edit)
        self.edit_entry.bind('<FocusOut>', self.finish_edit)
        self.editing_item = None
        self.editing_column = None
        self.cyclic_edit_mode = False
        self.table_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview, style='Modern.Vertical.TScrollbar')
        self.tree.configure(yscrollcommand=self.table_scrollbar.set)
        self.table_scrollbar.grid(row=1, column=1, sticky="ns")
        self.update_column_headers()
    def _create_plot_section(self, parent):
        frame = ttk.LabelFrame(parent, text="", padding=5, style='Modern.TLabelframe')
        frame.grid(row=3, column=0, columnspan=2, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        plot_toolbar = ttk.Frame(frame, style='Modern.TFrame')
        plot_toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        plot_toolbar.columnconfigure(0, weight=0)
        plot_toolbar.columnconfigure(1, weight=1)
        plot_toolbar.columnconfigure(2, weight=0)
        plot_actions_left = ttk.Frame(plot_toolbar, style='Modern.TFrame')
        plot_actions_left.grid(row=0, column=0, sticky="w")
        plot_actions_right = ttk.Frame(plot_toolbar, style='Modern.TFrame')
        plot_actions_right.grid(row=0, column=2, sticky="e")
        self.generate_plot_button = ttk.Button(plot_actions_left, text="Generuj wykres", command=self.generate_plot, style='Modern.TButton')
        self.generate_plot_button.grid(row=0, column=0, padx=(0, 5))
        ttk.Button(plot_actions_left, text="Wyczyść wykres", command=self.clear_plot, style='Modern.TButton').grid(row=0, column=1)
        ttk.Button(plot_actions_right, text="Zapisz wykres", command=self.save_plot_dialog, style='Modern.TButton').grid(row=0, column=0)
        self.scroll_canvas = tk.Canvas(frame, bg=self.colors['surface'], highlightthickness=2,
                                      borderwidth=0, relief='solid',
                                      highlightbackground=self.colors['border'],
                                      highlightcolor=self.colors['border'])
        self.scroll_canvas.grid(row=1, column=0, sticky="nsew")
        self.v_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.scroll_canvas.yview, style='Modern.Vertical.TScrollbar')
        self.v_scrollbar.grid(row=1, column=1, sticky="ns")
        self.h_scrollbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.scroll_canvas.xview, style='Modern.Horizontal.TScrollbar')
        self.h_scrollbar.grid(row=2, column=0, sticky="ew")
        self.scroll_canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        self.scrollable_frame = ttk.Frame(self.scroll_canvas, style='Modern.TFrame')
        self.scroll_window = self.scroll_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.fig = Figure(figsize=(15, 12), dpi=100, facecolor='#FFFFFF')
        self.canvas = FigureCanvasTkAgg(self.fig, self.scrollable_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.scrollable_frame.bind('<Configure>', self._configure_scroll_region)
        self.scroll_canvas.bind('<Configure>', self._resize_scrollable_frame)
        self._bind_mousewheel(self.scroll_canvas)
        self._bind_mousewheel(self.scrollable_frame)
        self._bind_mousewheel(frame)
        self.update_table_scrollbar()
        self.update_plot_scrollbars()
    def _bind_mousewheel(self, widget):
        widget.bind("<MouseWheel>", self._on_mousewheel)
        widget.bind("<Shift-MouseWheel>", self._on_shift_mousewheel)
    def _on_mousewheel(self, event):
        self.scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    def _on_shift_mousewheel(self, event):
        self.scroll_canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
    def _configure_scroll_region(self, event=None):
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
    def _resize_scrollable_frame(self, event=None):
        canvas_width = self.scroll_canvas.winfo_width()
        self.scroll_canvas.itemconfig(self.scroll_window, width=canvas_width)
    def _setup_keyboard_shortcuts(self):
        self.root.bind('<F5>', lambda e: self.update_table())
        self.root.bind('<Escape>', lambda e: self.cancel_edit() if self.editing_item else self.reset_sorting())
        self.root.bind('<Delete>', lambda e: self.remove_point())
        self.root.bind('<Control-d>', lambda e: self.remove_point())
        self.root.bind('<Control-s>', lambda e: self.save_plot_dialog() if self.ax is not None else None)
        self.root.bind('<F12>', lambda e: self.generate_plot())
        self.root.bind('<Control-g>', lambda e: self.generate_plot())
        self.root.bind('<Control-a>', lambda e: self.select_first_item())
        self.root.bind('<Control-r>', lambda e: self.reset_sorting())
        self.root.bind('<F2>', lambda e: self.start_inline_edit() if not self.editing_item else None)
        self.root.bind('<Control-e>', lambda e: self.start_continuous_edit())
        self.root.bind('<Control-Shift-e>', lambda e: self.start_cyclic_edit())
        self.tree.bind('<Up>', self.handle_tree_navigation)
        self.tree.bind('<Down>', self.handle_tree_navigation)
        self.tree.bind('<Prior>', self.handle_tree_navigation)
        self.tree.bind('<Next>', self.handle_tree_navigation)
    def _validate_depth_input(self, action, char, text_after):
        """Sprawdza poprawność wartości głębokości (0-10m, 1 miejsce po przecinku)"""
        if action == '0':
            return True
        if text_after == '':
            return True
        if not (char.isdigit() or char in '.,'):
            return False
        if char == ',':
            char = '.'
            test_text = text_after.replace(',', '.')
            if test_text.count('.') > 1:
                return False
        if char == '.' and text_after.count('.') > 1:
            return False
        test_text = text_after.replace(',', '.')
        if '.' in test_text:
            parts = test_text.split('.')
            if len(parts) == 2 and len(parts[1]) > 1:
                return False
        try:
            value = float(test_text)
            if value > 10.0:
                return False
        except ValueError:
            pass
        return True
    def _validate_n10_input(self, action, char, text_after):
        """Sprawdza poprawność wartości N₁₀ (0-100, tylko liczby całkowite)"""
        if action == '0':
            return True
        if text_after == '':
            return True
        if not char.isdigit():
            return False
        try:
            value = int(text_after)
            if value > 100:
                return False
        except ValueError:
            return False
        return True
    def select_first_item(self):
        children = self.tree.get_children()
        if children:
            self.tree.selection_set(children[0])
            self.tree.focus(children[0])
    def validate_number(self, value_str, field_name, min_val=None, max_val=None, decimal_places=None):
        if not value_str.strip():
            return None, f"Pole '{field_name}' jest puste"
        if 'głębokość' in field_name.lower() or 'głęb' in field_name.lower():
            clean_value = value_str.strip()
            clean_value = clean_value.replace(',', '.')
            if not clean_value.replace('.', '').isdigit():
                return None, f"Pole '{field_name}' może zawierać tylko liczby (cyfry 0-9 i jedną kropkę)"
            if clean_value.count('.') > 1:
                return None, f"Pole '{field_name}' może zawierać maksymalnie jedną kropkę dziesiętną"
            value_str = clean_value
        elif 'n₁₀' in field_name.lower() or 'n10' in field_name.lower():
            clean_value = value_str.strip()
            if not clean_value.isdigit():
                return None, f"Pole '{field_name}' może zawierać tylko liczby całkowite (bez kropek i przecinków)"
            value_str = clean_value
        else:
            value_str = value_str.replace(',', '.')
        try:
            if 'n₁₀' in field_name.lower() or 'n10' in field_name.lower():
                value = int(value_str)
            else:
                value = float(value_str)
            if decimal_places is not None and '.' in value_str:
                decimal_part = value_str.split('.')[1]
                if len(decimal_part) > decimal_places:
                    return None, f"Pole '{field_name}' może mieć maksymalnie {decimal_places} miejsc po przecinku"
            if min_val is not None and value < min_val:
                return None, f"Wartość '{field_name}' musi być >= {min_val}"
            if max_val is not None and value > max_val:
                return None, f"Wartość '{field_name}' musi być <= {max_val}"
            return value, None
        except ValueError:
            return None, f"'{value_str}' nie jest prawidłową liczbą dla pola '{field_name}'"
    def add_point(self, event=None):
        depth, err = self.validate_number(self.depth_var.get(), "Głębokość", 0, 10, decimal_places=1)
        if err:
            CustomMessageBox.showerror(err)
            self.depth_entry.focus()
            return
        n10, err = self.validate_number(self.n10_var.get(), "N₁₀", 0, 100)
        if err:
            CustomMessageBox.showerror(err)
            self.n10_entry.focus()
            return
        existing_point = None
        for item in self.data:
            if abs(item['depth'] - depth) < 0.01:
                existing_point = item
                break
        if existing_point:
            if existing_point['n10'] is None:
                existing_point['n10'] = int(n10)
                self.depth_var.set("")
                self.n10_var.set("")
                self.depth_entry.focus()
                self.update_table()
                self.update_column_headers()
                self.status_var.set(f"Zaktualizowano N₁₀ na głębokości {depth:.1f}m: {int(n10)}")
                return
            else:
                existing_n10_display = str(existing_point['n10']) if existing_point['n10'] is not None else "-"
                if not CustomMessageBox.askyesno(
                    f"Punkt o głębokości {depth:.1f}m już istnieje (N₁₀={existing_n10_display}).\n"
                    f"Czy zastąpić wartością N₁₀={int(n10)}?"):
                    return
                existing_point['n10'] = int(n10)
                self.depth_var.set("")
                self.n10_var.set("")
                self.depth_entry.focus()
                self.update_table()
                self.update_column_headers()
                self.status_var.set(f"Zaktualizowano N₁₀ na głębokości {depth:.1f}m: {int(n10)}")
                return
        self.data.append({
            'order': self.next_order,
            'depth': depth,
            'n10': int(n10),
            'ld': None,
            'ls': None
        })
        self.next_order += 1
        self.depth_var.set("")
        self.n10_var.set("")
        self.depth_entry.focus()
        self.update_table()
        self.update_column_headers()
        self.status_var.set(f"➕ Dodano punkt o głębokości {depth:.1f}m")
    def create_points_every_10cm(self):
        """Tworzy punkty co 10 cm w podanym zakresie"""
        depth_from, err = self.validate_number(self.depth_from_var.get(), "Głębokość od", 0, 10, decimal_places=1)
        if err:
            CustomMessageBox.showerror(err)
            self.depth_from_entry.focus()
            return
        depth_to, err = self.validate_number(self.depth_to_var.get(), "Głębokość do", 0, 10, decimal_places=1)
        if err:
            CustomMessageBox.showerror(err)
            self.depth_to_entry.focus()
            return
        if depth_from >= depth_to:
            CustomMessageBox.showerror("Głębokość 'od' musi być mniejsza niż głębokość 'do'")
            self.depth_from_entry.focus()
            return
        existing_points = [p for p in self.data if depth_from <= p['depth'] <= depth_to]
        if existing_points:
            existing_depths = [f"{p['depth']:.1f}m" for p in existing_points]
            message = f"W podanym zakresie istnieją już punkty na głębokościach: {', '.join(existing_depths)}\n\nCzy kontynuować? Istniejące punkty zostaną zachowane."
            if not CustomMessageBox.askyesno(message):
                return
        start_depth_cm = math.ceil(depth_from * 10) * 10
        end_depth_cm = math.floor((depth_to - 0.1) * 10) * 10
        if start_depth_cm > end_depth_cm:
            CustomMessageBox.showwarning(f"W zakresie {depth_from:.1f}m - {depth_to:.1f}m nie ma pełnych punktów co 10cm")
            return
        created_points = []
        existing_depths = [p['depth'] for p in self.data]
        for depth_cm in range(start_depth_cm, end_depth_cm + 1, 10):
            depth = depth_cm / 100.0
            point_exists = any(abs(existing_depth - depth) < 0.01 for existing_depth in existing_depths)
            if not point_exists:
                self.data.append({
                    'order': self.next_order,
                    'depth': depth,
                    'n10': None,
                    'ld': None,
                    'ls': None
                })
                self.next_order += 1
                created_points.append(depth)
        if created_points:
            self.depth_from_var.set("")
            self.depth_to_var.set("")
            self.update_table()
            self.update_column_headers()
            count = len(created_points)
            depth_range = f"{created_points[0]:.1f}m - {created_points[-1]:.1f}m"
            self.status_var.set(f"⚡ Utworzono {count} punktów co 10cm w zakresie {depth_range}")
            CustomMessageBox.showsuccess(
                f"Utworzono {count} punktów pomiarowych co 10cm.\n\n"
                f"Zakres: {depth_range}\n\n"
                "Wartości N₁₀ nie zostały ustawione (wyświetlane jako '-').\n"
                "Kliknij dwukrotnie na komórkę N₁₀ w tabeli lub wprowadź ręcznie głębokość i wartość N₁₀ aby uzupełnić dane.")
        else:
            self.status_var.set("Wszystkie punkty w podanym zakresie już istnieją")
    def remove_point(self, event=None):
        selection = self.tree.selection()
        if not selection:
            CustomMessageBox.showwarning("Wybierz punkt do usunięcia z tabeli")
            return
        item = self.tree.item(selection[0])
        try:
            order = int(item['values'][0])
            depth = float(item['values'][1])
            if CustomMessageBox.askyesno(f"Usunąć punkt lp. {order} (głębokość {depth}m)?"):
                self.data = [p for p in self.data if p['order'] != order]
                self.update_table()
                self.update_column_headers()
                self.status_var.set(f"❌ Usunięto punkt lp. {order}")
        except Exception as e:
            CustomMessageBox.showerror(f"Nie można usunąć punktu: {e}")
    def on_table_click(self, event):
        """Reaguje na kliknięcie w tabelę"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            if column == "#3":
                pass
    def start_inline_edit(self, event=None):
        """Włącza edycję wartości N₁₀"""
        selection = self.tree.selection()
        if not selection:
            return
        item_id = selection[0]
        if event and event.type == '4':
            region = self.tree.identify("region", event.x, event.y)
            if region != "cell":
                return
            column = self.tree.identify_column(event.x)
            if column != "#3":
                return
        self.start_edit_column(item_id, "#3")
    def start_edit_column(self, item_id, column):
        """Włącza edycję wybranej komórki"""
        if column != "#3":
            return
        if self.editing_item:
            self.cancel_edit()
        self.tree.see(item_id)
        item = self.tree.item(item_id)
        values = item['values']
        current_value = str(values[2])
        self.editing_item = item_id
        self.editing_column = column
        self.edit_var.set(current_value)
        def place_edit_widget():
            bbox = self.tree.bbox(item_id, column)
            if not bbox:
                self.root.after(10, place_edit_widget)
                return
            x, y, width, height = bbox
            self.edit_entry.place(x=x, y=y, width=width, height=height)
            self.edit_entry.focus()
            self.edit_entry.select_range(0, tk.END)
            depth_str = values[1]
            depth = float(depth_str.split('\n')[0]) if '\n' in depth_str else float(depth_str)
            self.status_var.set(f"Edycja N₁₀ na głębokości {depth:.2f}m (Enter→następny, Esc→anuluj)")
        self.root.after(10, place_edit_widget)
    def finish_edit(self, event=None):
        """Zapisuje zmienioną wartość"""
        if not self.editing_item:
            return
        new_value = self.edit_var.get().strip()
        if not new_value:
            self.cancel_edit()
            return
        new_n10, err = self.validate_number(new_value, "N₁₀", 0, 100)
        if err:
            self.status_var.set(f"Błąd: {err}")
            if event and event.type != '10':
                self.edit_entry.focus()
            return
        item = self.tree.item(self.editing_item)
        order = int(item['values'][0])
        point = next((p for p in self.data if p['order'] == order), None)
        if point:
            point['n10'] = int(new_n10)
            self.update_table()
            depth = point['depth']
            self.status_var.set(f"Zaktualizowano N₁₀ na głębokości {depth:.1f}m: {int(new_n10)}")
        self.edit_entry.place_forget()
        self.editing_item = None
        self.editing_column = None
    def finish_edit_and_next(self, event=None):
        """Zapisz i przejdź do następnej komórki"""
        if not self.editing_item:
            return
        current_item = self.editing_item
        new_value = self.edit_var.get().strip()
        if not new_value:
            self.cancel_edit()
            return
        new_n10, err = self.validate_number(new_value, "N₁₀", 0, 100)
        if err:
            self.status_var.set(f"Błąd: {err}")
            self.edit_entry.focus()
            return
        item = self.tree.item(current_item)
        order = int(item['values'][0])
        point = next((p for p in self.data if p['order'] == order), None)
        if point:
            point['n10'] = int(new_n10)
            depth = point['depth']
            self.status_var.set(f"Zapisano N₁₀={int(new_n10)} (głęb. {depth:.1f}m) → następna komórka")
        children = self.tree.get_children()
        next_order = None
        try:
            current_index = children.index(current_item)
            if current_index < len(children) - 1:
                next_item = children[current_index + 1]
                next_order = int(self.tree.item(next_item)['values'][0])
            else:
                if self.cyclic_edit_mode and children:
                    first_item = children[0]
                    next_order = int(self.tree.item(first_item)['values'][0])
                    self.status_var.set(f"Zapisano N₁₀={int(new_n10)} (głęb. {depth:.1f}m) → pierwszy punkt (tryb cykliczny)")
                else:
                    next_order = None
                    self.cyclic_edit_mode = False
                    self.status_var.set(f"Zapisano N₁₀={int(new_n10)} (głęb. {depth:.1f}m) - KONIEC (ostatni punkt)")
        except ValueError:
            pass
        self.edit_entry.place_forget()
        self.editing_item = None
        self.editing_column = None
        self.update_table()
        if next_order:
            for item_id in self.tree.get_children():
                item = self.tree.item(item_id)
                if int(item['values'][0]) == next_order:
                    self.tree.selection_set(item_id)
                    self.tree.focus(item_id)
                    self.root.after(100, lambda: self.start_edit_column(item_id, "#3"))
                    break
    def finish_edit_and_previous(self, event=None):
        """Zapisz i przejdź do poprzedniej komórki"""
        if not self.editing_item:
            return
        current_item = self.editing_item
        new_value = self.edit_var.get().strip()
        if not new_value:
            self.cancel_edit()
            return
        new_n10, err = self.validate_number(new_value, "N₁₀", 0, 100)
        if err:
            self.status_var.set(f"Błąd: {err}")
            self.edit_entry.focus()
            return
        item = self.tree.item(current_item)
        order = int(item['values'][0])
        point = next((p for p in self.data if p['order'] == order), None)
        if point:
            point['n10'] = int(new_n10)
            depth = point['depth']
            self.status_var.set(f"Zapisano N₁₀={int(new_n10)} (głęb. {depth:.1f}m) → poprzednia komórka")
        children = self.tree.get_children()
        prev_order = None
        try:
            current_index = children.index(current_item)
            if current_index > 0:
                prev_item = children[current_index - 1]
                prev_order = int(self.tree.item(prev_item)['values'][0])
            else:
                if self.cyclic_edit_mode and children:
                    last_item = children[-1]
                    prev_order = int(self.tree.item(last_item)['values'][0])
                    self.status_var.set(f"Zapisano N₁₀={int(new_n10)} (głęb. {depth:.1f}m) → ostatni punkt (tryb cykliczny)")
                else:
                    prev_order = None
                    self.cyclic_edit_mode = False
                    self.status_var.set(f"Zapisano N₁₀={int(new_n10)} (głęb. {depth:.1f}m) - KONIEC (pierwszy punkt)")
        except ValueError:
            pass
        self.edit_entry.place_forget()
        self.editing_item = None
        self.editing_column = None
        self.update_table()
        if prev_order:
            for item_id in self.tree.get_children():
                item = self.tree.item(item_id)
                if int(item['values'][0]) == prev_order:
                    self.tree.selection_set(item_id)
                    self.tree.focus(item_id)
                    self.root.after(100, lambda: self.start_edit_column(item_id, "#3"))
                    break
    def cancel_edit(self, event=None):
        """Anuluje edycję"""
        if self.editing_item:
            self.edit_entry.place_forget()
            self.editing_item = None
            self.editing_column = None
            self.cyclic_edit_mode = False
            self.status_var.set("Anulowano edycję")
    def copy_from_previous(self, event=None):
        """Kopiuje wartość z poprzedniego wiersza"""
        if not self.editing_item:
            return
        children = self.tree.get_children()
        try:
            current_index = children.index(self.editing_item)
            if current_index > 0:
                prev_item = children[current_index - 1]
                prev_values = self.tree.item(prev_item)['values']
                prev_n10 = str(prev_values[2])
                self.edit_var.set(prev_n10)
                self.edit_entry.select_range(0, tk.END)
                prev_depth = float(prev_values[1])
                current_values = self.tree.item(self.editing_item)['values']
                current_depth = float(current_values[1])
                self.status_var.set(f"Skopiowano N₁₀={prev_n10} z głęb. {prev_depth:.1f}m → {current_depth:.1f}m")
            else:
                self.status_var.set("Brak poprzedniej komórki do skopiowania")
        except (ValueError, IndexError):
            self.status_var.set("Błąd podczas kopiowania z poprzedniej komórki")
    def handle_tree_navigation(self, event=None):
        """Kończy edycję przy przejściu do innej komórki"""
        if self.editing_item:
            self.finish_edit()
        return None
    def on_tree_scroll(self, event=None):
        """Kończy edycję przy przewijaniu tabeli"""
        if self.editing_item:
            self.finish_edit()
        return None
    def start_continuous_edit(self):
        """Włącza edycję od pierwszego punktu bez wartości"""
        if not self.data:
            CustomMessageBox.showinfo("Brak danych do edycji")
            return
        first_empty = next((p for p in sorted(self.data, key=lambda x: x['depth']) if p['n10'] == 0), None)
        if not first_empty:
            first_empty = sorted(self.data, key=lambda x: x['depth'])[0]
        for item_id in self.tree.get_children():
            item = self.tree.item(item_id)
            if int(item['values'][0]) == first_empty['order']:
                self.tree.selection_set(item_id)
                self.tree.focus(item_id)
                self.tree.see(item_id)
                self.root.after(100, lambda: self.start_edit_column(item_id, "#3"))
                return
        CustomMessageBox.showwarning("Nie znaleziono punktu do edycji")
    def start_cyclic_edit(self):
        """Włącza edycję w pętli (ostatni → pierwszy)"""
        self.cyclic_edit_mode = True
        self.start_continuous_edit()
        self.status_var.set("Tryb edycji cyklicznej włączony - po ostatnim punkcie przejście do pierwszego")
    def clear_all(self):
        has_data = bool(self.data)
        has_profile = bool(self.profile_layers)
        has_input = bool(self.depth_var.get().strip() or self.n10_var.get().strip() or
                        self.layer_from_var.get().strip() or self.layer_to_var.get().strip() or
                        self.layer_description_var.get().strip())
        if has_data or has_profile or has_input:
            message = "Wyczyścić "
            items = []
            if has_data:
                items.append("wszystkie dane pomiarowe")
            if has_profile:
                items.append("profil geologiczny")
            if has_input:
                items.append("pola wprowadzania")
            message += " i ".join(items) + " oraz wykres?"
            if (has_data or has_profile) and not CustomMessageBox.askyesno(message):
                return
            if has_data:
                self.data.clear()
                self.next_order = 1
                self.sort_column = "Głęb. (m)"
                self.sort_reverse = False
                self.update_table()
                self.update_column_headers()
            if has_profile:
                self.profile_layers.clear()
                self.next_profile_id = 1
                self.profile_sort_column = "Głęb. (m)"
                self.profile_sort_reverse = False
                self.update_profile_table()
                self.update_profile_column_headers()
            if has_data or has_profile:
                self.fig.clear()
                self.ax = None
                self.canvas.draw()
                self.scrollable_frame.update()
                self.scroll_canvas.update()
                self.root.update()
                self.scroll_canvas.xview_moveto(0)
                self.scroll_canvas.yview_moveto(0)
                self.update_plot_scrollbars()
                self.update_generate_button_text()
            self.depth_var.set("")
            self.n10_var.set("")
            self.layer_from_var.set("")
            self.layer_to_var.set("")
            self.layer_description_var.set("")
            status_items = []
            if has_data:
                status_items.append("dane pomiarowe")
            if has_profile:
                status_items.append("profil geologiczny")
            if has_input:
                status_items.append("pola wprowadzania")
            self.status_var.set(f"🗑️ Wyczyszczono {' i '.join(status_items)}")
        else:
            self.status_var.set("Brak danych do wyczyszczenia")
    def clear_table(self):
        """Usuwa wszystkie punkty z tabeli"""
        if self.data:
            if CustomMessageBox.askyesno("Wyczyścić wszystkie punkty pomiarowe z tabeli?"):
                self.data.clear()
                self.next_order = 1
                self.sort_column = "Głęb. (m)"
                self.sort_reverse = False
                self.update_table()
                self.update_column_headers()
                self.status_var.set("🗑️ Wyczyszczono tabelę punktów pomiarowych")
        else:
            self.status_var.set("Tabela jest już pusta")
    def clear_plot(self):
        """Usuwa wykres"""
        if self.ax is not None:
            if CustomMessageBox.askyesno("Wyczyścić wykres?"):
                self.fig.clear()
                self.ax = None
                self.canvas.draw()
                self.scrollable_frame.update()
                self.scroll_canvas.update()
                self.root.update()
                self.scroll_canvas.xview_moveto(0)
                self.scroll_canvas.yview_moveto(0)
                self.update_plot_scrollbars()
                self.update_generate_button_text()
                self.status_var.set("🗑️ Wyczyszczono wykres")
        else:
            self.status_var.set("Wykres jest już pusty")
    def on_depth_from_enter(self, event):
        """Przejdź do pola "głębokość do" po Enter"""
        self.depth_to_entry.focus()
        return 'break'
    def on_depth_to_enter(self, event):
        """Utwórz punkty po Enter"""
        self.create_points_every_10cm()
        return 'break'
    def on_layer_from_enter(self, event):
        """Przejdź do pola "głębokość do" po Enter"""
        self.layer_to_entry.focus()
        return 'break'
    def on_layer_to_enter(self, event):
        """Przejdź do pola opisu po Enter"""
        self.layer_description_entry.focus()
        return 'break'
    def on_layer_description_enter(self, event):
        """Dodaj warstwę po Enter"""
        self.add_profile_layer()
        return 'break'
    def add_profile_layer(self):
        """Dodaje nową warstwę geologiczną do profilu"""
        if not self.data:
            CustomMessageBox.showerror("Nie można dodawać warstw bez punktów pomiarowych. Dodaj najpierw punkty DPL.")
            return
        max_allowed_depth = 10.0
        if self.data:
            deepest_point = max(p['depth'] for p in self.data)
            max_allowed_depth = min(deepest_point + 0.10, 10.0)
        depth_from, err = self.validate_number(self.layer_from_var.get(), "Głębokość od", 0, max_allowed_depth, decimal_places=1)
        if err:
            CustomMessageBox.showerror(err)
            self.layer_from_entry.focus()
            return
        depth_to, err = self.validate_number(self.layer_to_var.get(), "Głębokość do", 0, max_allowed_depth, decimal_places=1)
        if err:
            CustomMessageBox.showerror(err)
            self.layer_to_entry.focus()
            return
        depth_from = round(depth_from, 1)
        depth_to = round(depth_to, 1)
        if depth_from >= depth_to:
            CustomMessageBox.showerror("Głębokość 'od' musi być mniejsza niż głębokość 'do'")
            self.layer_from_entry.focus()
            return
        for existing_layer in self.profile_layers:
            existing_from = existing_layer['depth_from']
            existing_to = existing_layer['depth_to']
            if (depth_from < existing_to and depth_to > existing_from):
                if not (depth_from == existing_to or depth_to == existing_from):
                    CustomMessageBox.showerror(
                        f"Nowa warstwa ({depth_from:.1f}m - {depth_to:.1f}m) zachodzi na istniejącą warstwę "
                        f"({existing_from:.1f}m - {existing_to:.1f}m).\n"
                        f"Warstwy mogą się jedynie stykać, np. 1.0-1.5 i 1.5-2.0")
                    self.layer_from_entry.focus()
                    return
        description = self.layer_description_var.get().strip()
        if not description:
            CustomMessageBox.showerror("Opis warstwy nie może być pusty")
            self.layer_description_entry.focus()
            return
        self.profile_layers.append({
            'id': self.next_profile_id,
            'depth_from': depth_from,
            'depth_to': depth_to,
            'description': description
        })
        self.next_profile_id += 1
        self.profile_layers.sort(key=lambda x: x['depth_from'])
        self.layer_from_var.set("")
        self.layer_to_var.set("")
        self.layer_description_var.set("")
        self.update_profile_table()
        self.layer_from_entry.focus()
        max_depth_info = f" | Maks. głęb.: {max_allowed_depth:.1f}m" if self.data else ""
        self.status_var.set(f"➕ Dodano warstwę: {description} ({depth_from:.1f}m - {depth_to:.1f}m){max_depth_info}")
    def remove_profile_layer(self):
        """Usuwa zaznaczoną warstwę z profilu"""
        selection = self.profile_tree.selection()
        if not selection:
            CustomMessageBox.showwarning("Wybierz warstwę do usunięcia z tabeli profilu")
            return
        item = self.profile_tree.item(selection[0])
        try:
            layer_id = int(item['values'][0])
            layer_to_remove = next((l for l in self.profile_layers if l['id'] == layer_id), None)
            if layer_to_remove and CustomMessageBox.askyesno(
                f"Usunąć warstwę '{layer_to_remove['description']}' "
                f"({layer_to_remove['depth_from']:.1f}m - {layer_to_remove['depth_to']:.1f}m)?"):
                self.profile_layers = [l for l in self.profile_layers if l['id'] != layer_id]
                self.update_profile_table()
                self.status_var.set(f"❌ Usunięto warstwę: {layer_to_remove['description']}")
        except Exception as e:
            CustomMessageBox.showerror(f"Nie można usunąć warstwy: {e}")
    def clear_profile(self):
        """Usuwa wszystkie warstwy geologiczne"""
        if self.profile_layers:
            if CustomMessageBox.askyesno("Usunąć wszystkie warstwy profilu?"):
                self.profile_layers.clear()
                self.next_profile_id = 1
                self.profile_sort_column = "Głęb. (m)"
                self.profile_sort_reverse = False
                self.update_profile_table()
                self.update_profile_column_headers()
                self.status_var.set("🗑️ Wyczyszczono profil geologiczny")
        else:
            self.status_var.set("Profil geologiczny jest już pusty")
    def update_profile_table(self):
        """Odświeża tabelę warstw geologicznych"""
        for item in self.profile_tree.get_children():
            self.profile_tree.delete(item)
        if self.profile_sort_column and self.profile_layers:
            display_layers = self._apply_profile_sort()
        else:
            display_layers = sorted(self.profile_layers, key=lambda x: x['depth_from'])
        for i, layer in enumerate(display_layers):
            tag = 'alternate' if i % 2 == 1 else ''
            depth_str = f"{layer['depth_from']:.2f}\n{layer['depth_to']:.2f}"
            self.profile_tree.insert("", "end", values=(
                layer['id'],
                depth_str,
                layer['description']
            ), tags=(tag,))
        self.update_profile_scrollbar()
        self.update_profile_column_headers()
    def update_profile_scrollbar(self):
        """Pokazuje lub ukrywa pasek przewijania w zależności od ilości warstw"""
        if self.profile_layers:
            self.profile_scrollbar.grid()
        else:
            self.profile_scrollbar.grid_remove()
    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if self.sort_column and self.data:
            self._apply_sort()
            display_data = self.data
        else:
            display_data = sorted(self.data, key=lambda x: x['depth'])
        for i, point in enumerate(display_data):
            ld_str = f"{point['ld']:.3f}" if point['ld'] is not None else "-"
            ls_str = f"{point['ls']:.3f}" if point['ls'] is not None else "-"
            n10_str = str(point['n10']) if point['n10'] is not None else "-"
            depth_from = point['depth']
            depth_to = point['depth'] + 0.1
            depth_str = f"{depth_from:.2f}\n{depth_to:.2f}"
            tag = 'alternate' if i % 2 == 1 else ''
            self.tree.insert("", "end", values=(
                point['order'],
                depth_str,
                n10_str,
                ld_str,
                ls_str
            ), tags=(tag,))
        self.update_table_scrollbar()
    def update_table_scrollbar(self):
        if self.data:
            self.table_scrollbar.grid()
        else:
            self.table_scrollbar.grid_remove()
    def update_plot_scrollbars(self):
        if self.data and self.ax is not None:
            self.v_scrollbar.grid()
            self.h_scrollbar.grid()
        else:
            self.v_scrollbar.grid_remove()
            self.h_scrollbar.grid_remove()
    def update_generate_button_text(self):
        """Zmienia tekst przycisku (Generuj/Aktualizuj)"""
        if self.ax is not None:
            self.generate_plot_button.configure(text="Aktualizuj wykres")
        else:
            self.generate_plot_button.configure(text="Generuj wykres")
    def center_plot_view(self):
        """Wycentruj wykres na ekranie"""
        self.root.after(150, self._center_plot_now)
    def _center_plot_now(self):
        """Wycentruj wykres (wewnętrzna funkcja)"""
        try:
            for attempt in range(5):
                self.scrollable_frame.update()
                self.scroll_canvas.update()
                self.root.update()
                bbox = self.scroll_canvas.bbox("all")
                if not bbox:
                    continue
                self.scroll_canvas.configure(scrollregion=bbox)
                canvas_widget = self.canvas.get_tk_widget()
                canvas_width = bbox[2] - bbox[0]
                canvas_height = bbox[3] - bbox[1]
                viewport_width = self.scroll_canvas.winfo_width()
                viewport_height = self.scroll_canvas.winfo_height()
                if canvas_width > 10 and canvas_height > 10 and viewport_width > 10 and viewport_height > 10:
                    if canvas_width > viewport_width:
                        x_center = (canvas_width - viewport_width) / (2.0 * canvas_width)
                    else:
                        x_center = 0.0
                    y_top = 0.0
                    self.scroll_canvas.xview_moveto(x_center)
                    self.scroll_canvas.yview_moveto(y_top)
                    self.scroll_canvas.update()
                    break
                if attempt < 4:
                    self.root.after(50)
                    self.root.update()
        except Exception as e:
            print(f"Błąd centrowania: {e}")
            self.scroll_canvas.xview_moveto(0)
            self.scroll_canvas.yview_moveto(0)
    def _apply_sort(self):
        col_map = {
            "lp.": "order",
            "Głęb. (m)": "depth",
            "N₁₀": "n10",
            "Id": "ld",
            "Is": "ls"
        }
        key = col_map.get(self.sort_column)
        if not key:
            self.status_var.set(f"Nieznana kolumna do sortowania: {self.sort_column}")
            return
        try:
            def safe_sort_key(x):
                value = x.get(key)
                if value is None:
                    return float('inf') if not self.sort_reverse else float('-inf')
                return value
            self.data.sort(key=safe_sort_key, reverse=self.sort_reverse)
        except Exception as e:
            self.status_var.set(f"Błąd sortowania: {e}")
    def sort_by_column(self, col):
        if not self.data:
            self.status_var.set("Brak danych do sortowania")
            return
        if self.sort_column == col:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = col
            self.sort_reverse = False
        self._apply_sort()
        self.update_column_headers()
        self.update_table()
        direction = "malejąco" if self.sort_reverse else "rosnąco"
        self.status_var.set(f"Posortowano według: {col} ({direction})")
    def update_column_headers(self):
        columns = ("lp.", "Głęb. (m)", "N₁₀", "Id", "Is")
        for col in columns:
            text = col.rstrip(" ▲▼")
            if col == self.sort_column and len(self.data) > 1:
                text += " ▼" if self.sort_reverse else " ▲"
            self.tree.heading(col, text=text)
    def reset_sorting(self):
        self.sort_column = None
        self.sort_reverse = False
        self.update_column_headers()
        self.update_table()
        self.status_var.set("Resetowano sortowanie - dane posortowane według głębokości")
    def sort_profile_by_column(self, col):
        """Sortuje warstwy według wybranej kolumny"""
        if not self.profile_layers:
            self.status_var.set("Brak warstw do sortowania")
            return
        if self.profile_sort_column == col:
            self.profile_sort_reverse = not self.profile_sort_reverse
        else:
            self.profile_sort_column = col
            self.profile_sort_reverse = False
        self._apply_profile_sort()
        self.update_profile_column_headers()
        self.update_profile_table()
        direction = "malejąco" if self.profile_sort_reverse else "rosnąco"
        self.status_var.set(f"Posortowano profil według: {col} ({direction})")
    def _apply_profile_sort(self):
        """Zwraca posortowaną listę warstw"""
        col_map = {
            "lp.": "id",
            "Głęb. (m)": "depth_from",
            "Opis": "description"
        }
        key = col_map.get(self.profile_sort_column)
        if not key:
            return self.profile_layers
        try:
            return sorted(self.profile_layers, key=lambda x: x.get(key), reverse=self.profile_sort_reverse)
        except Exception as e:
            self.status_var.set(f"Błąd sortowania profilu: {e}")
            return self.profile_layers
    def update_profile_column_headers(self):
        """Dodaje strzałki sortowania w nagłówkach kolumn"""
        columns = ("lp.", "Głęb. (m)", "Opis")
        for col in columns:
            text = col.rstrip(" ▲▼")
            if col == self.profile_sort_column and len(self.profile_layers) > 1:
                text += " ▼" if self.profile_sort_reverse else " ▲"
            self.profile_tree.heading(col, text=text)
    def calculate_parameters(self, silent=False):
        if not self.data:
            if not silent:
                CustomMessageBox.showwarning("Brak danych do obliczeń")
            return
        calculated = 0
        errors = []
        for point in self.data:
            try:
                n10 = point['n10']
                if n10 is None or n10 <= 0:
                    if n10 is None:
                        errors.append(f"lp. {point['order']}: N₁₀ nie zostało wprowadzone")
                    else:
                        errors.append(f"lp. {point['order']}: N₁₀ musi być > 0")
                    continue
                ld = 0.429 * math.log10(n10) + 0.071
                ls = ld * 0.188 + 0.845
                point['ld'] = ld
                point['ls'] = ls
                calculated += 1
            except Exception as e:
                errors.append(f"lp. {point['order']}: {e}")
        self.update_table()
        self.update_column_headers()
        if not silent:
            msg = f"Obliczono parametry dla {calculated} punktów"
            if errors:
                msg += f"\nBłędy ({len(errors)}):\n" + "\n".join(errors[:5])
                if len(errors) > 5:
                    msg += f"\n... i {len(errors) - 5} więcej"
            if calculated > 0:
                CustomMessageBox.showinfo(msg, "Obliczenia zakończone")
                self.status_var.set(f"🧮 Obliczono parametry dla {calculated} punktów")
            else:
                CustomMessageBox.showerror(msg, "Błąd obliczeń")
    def generate_plot(self, silent=False):
        if not self.data:
            if not silent:
                CustomMessageBox.showwarning("Brak danych do wykresu")
            self.update_plot_scrollbars()
            return
        missing_n10_points = [p for p in self.data if p['n10'] is None]
        if missing_n10_points:
            if not silent:
                missing_orders = [str(p['order']) for p in missing_n10_points[:5]]
                missing_list = ", ".join(missing_orders)
                if len(missing_n10_points) > 5:
                    missing_list += f" i {len(missing_n10_points) - 5} więcej"
                CustomMessageBox.showwarning(
                    f"Nie można wygenerować wykresu. Brak wartości N₁₀ dla punktów: {missing_list}.\n\n"
                    "Wprowadź wartości N₁₀ dla wszystkich punktów przed wygenerowaniem wykresu.",
                    "Brak wartości N₁₀")
            self.update_plot_scrollbars()
            return
        if self.ax is not None:
            self.fig.clear()
            self.ax = None
            self.canvas.draw()
            self.root.update_idletasks()
        sorted_data = sorted(self.data, key=lambda x: x['depth'], reverse=True)
        depths = [p['depth'] for p in sorted_data]
        n10_values = [p['n10'] for p in sorted_data]
        ld_values = [p.get('ld', None) for p in sorted_data]
        ls_values = [p.get('ls', None) for p in sorted_data]
        num_points = len(depths)
        if num_points <= 10:
            fig_height = 8
            bar_height = 1.0
            fs_main = 11
            fs_table = 10
            fs_labels = 9
        elif num_points <= 25:
            fig_height = 10
            bar_height = 1.0
            fs_main = 10
            fs_table = 9
            fs_labels = 8
        elif num_points <= 40:
            fig_height = 14
            bar_height = 1.0
            fs_main = 9
            fs_table = 8
            fs_labels = 7
        else:
            fig_height = max(18, num_points * 0.4)
            bar_height = 1.0
            fs_main = 8
            fs_table = 7
            fs_labels = 6
        self.scroll_canvas.update_idletasks()
        canvas_viewport_width = self.scroll_canvas.winfo_width()
        fig_dpi = self.fig.dpi
        available_width_px = max(canvas_viewport_width - 20, 1400)
        fig_width = available_width_px / fig_dpi
        self.fig.set_size_inches(fig_width, fig_height)
        self.fig.clear()
        has_calculated_values = any(p.get('ld') is not None or p.get('ls') is not None for p in sorted_data)
        has_profile = bool(self.profile_layers)
        if has_profile and has_calculated_values:
            width_ratios = [0.18, 0.62, 0.20] if num_points <= 40 else [0.15, 0.65, 0.20]
            wspace = 0.20
            gs = self.fig.add_gridspec(1, 3, width_ratios=width_ratios, wspace=wspace)
            ax_profile = self.fig.add_subplot(gs[0, 0])
            self.ax = self.fig.add_subplot(gs[0, 1])
            ax_table = self.fig.add_subplot(gs[0, 2])
        elif has_profile:
            width_ratios = [0.25, 0.75]
            wspace = 0.25
            gs = self.fig.add_gridspec(1, 2, width_ratios=width_ratios, wspace=wspace)
            ax_profile = self.fig.add_subplot(gs[0, 0])
            self.ax = self.fig.add_subplot(gs[0, 1])
            ax_table = None
        elif has_calculated_values:
            width_ratios = [0.7, 0.3] if num_points <= 40 else [0.75, 0.25]
            wspace = 0.3 if num_points <= 40 else 0.2
            gs = self.fig.add_gridspec(1, 2, width_ratios=width_ratios, wspace=wspace)
            ax_profile = None
            self.ax = self.fig.add_subplot(gs[0, 0])
            ax_table = self.fig.add_subplot(gs[0, 1])
        else:
            gs = self.fig.add_gridspec(1, 1)
            ax_profile = None
            self.ax = self.fig.add_subplot(gs[0, 0])
            ax_table = None
        if ax_profile is not None:
            ax_profile.set_xlim(0, 1)
            ax_profile.set_ylim(-0.5, num_points - 0.5)
            ax_profile.axis('off')
            ax_profile.set_facecolor('#FFFFFF')
            if self.profile_layers:
                header_y = num_points - 0.5 + 0.6
                header_fs = min(fs_table + 2, 12)
                ax_profile.text(0.5, header_y, 'Profil geologiczny', ha='center', va='center',
                               fontsize=header_fs, weight='bold', color='black')
                ax_profile.plot([0.05, 0.95], [num_points - 0.5, num_points - 0.5],
                               color='#000000', linewidth=2.0, alpha=1.0)
                ax_profile.plot([0.05, 0.95], [-0.5, -0.5],
                               color='#000000', linewidth=2.0, alpha=1.0)
                ax_profile.plot([0.05, 0.05], [-0.5, num_points - 0.5],
                               color='#000000', linewidth=2.0, alpha=1.0)
                ax_profile.plot([0.95, 0.95], [-0.5, num_points - 0.5],
                               color='#000000', linewidth=2.0, alpha=1.0)
                sorted_layers = sorted(self.profile_layers, key=lambda x: x['depth_from'])
                for layer_idx, layer in enumerate(sorted_layers):
                    if layer_idx % 2 == 1:
                        start_y = None
                        end_y = None
                        for i, depth in enumerate(depths):
                            if abs(depth - layer['depth_from']) <= 0.01:
                                start_y = i + 0.5
                            if abs(depth - layer['depth_to']) <= 0.01:
                                end_y = i + 0.5
                        max_extended_depth = depths[0] + 0.10 if depths else 0
                        if end_y is None and abs(layer['depth_to'] - max_extended_depth) <= 0.01:
                            end_y = -0.5
                        if start_y is not None and end_y is not None:
                            ax_profile.axhspan(min(start_y, end_y), max(start_y, end_y),
                                             xmin=0.05, xmax=0.95,
                                             facecolor='#E0E0E0', alpha=1.0, zorder=1)
                drawn_boundaries = set()
                max_chart_depth = depths[0] + 0.10
                for layer in sorted_layers:
                    layer_start_depth = layer['depth_from']
                    layer_end_depth = layer['depth_to']
                    shallowest_depth = min(depths) if depths else 0
                    deepest_data_depth = max(depths) if depths else 0
                    max_extended_depth = deepest_data_depth + 0.10
                    if layer_start_depth not in drawn_boundaries:
                        start_y = None
                        is_boundary_depth = (abs(layer_start_depth - shallowest_depth) <= 0.01 or
                                           abs(layer_start_depth - max_extended_depth) <= 0.01)
                        if not is_boundary_depth:
                            for i, depth in enumerate(depths):
                                if abs(depth - layer_start_depth) <= 0.01:
                                    start_y = i + 0.5
                                    break
                            if start_y is None and layer_start_depth <= max_chart_depth and layer_start_depth > depths[0]:
                                start_y = -0.5
                            if start_y is not None and start_y >= -0.5:
                                ax_profile.plot([0.05, 0.95], [start_y, start_y],
                                               color='#000000', linewidth=1.0, alpha=0.6,
                                               linestyle='-', zorder=10)
                        drawn_boundaries.add(layer_start_depth)
                    if layer_end_depth not in drawn_boundaries:
                        end_y = None
                        is_boundary_depth = (abs(layer_end_depth - shallowest_depth) <= 0.01 or
                                           abs(layer_end_depth - max_extended_depth) <= 0.01)
                        if not is_boundary_depth:
                            for i, depth in enumerate(depths):
                                if abs(depth - layer_end_depth) <= 0.01:
                                    end_y = i + 0.5
                                    break
                            if end_y is None and layer_end_depth <= max_chart_depth and layer_end_depth > depths[0]:
                                end_y = -0.5
                            if end_y is not None and end_y >= -0.5:
                                ax_profile.plot([0.05, 0.95], [end_y, end_y],
                                               color='#000000', linewidth=1.0, alpha=0.6,
                                               linestyle='-', zorder=10)
                        drawn_boundaries.add(layer_end_depth)
                for layer in sorted_layers:
                    layer_start_depth = layer['depth_from']
                    layer_end_depth = layer['depth_to']
                    start_boundary_y = None
                    end_boundary_y = None
                    for i, depth in enumerate(depths):
                        if abs(depth - layer_start_depth) <= 0.01:
                            start_boundary_y = i + 0.5
                        if abs(depth - layer_end_depth) <= 0.01:
                            end_boundary_y = i + 0.5
                    if start_boundary_y is None and layer_start_depth <= max_chart_depth and layer_start_depth > depths[0]:
                        start_boundary_y = -0.5
                    if end_boundary_y is None and layer_end_depth <= max_chart_depth and layer_end_depth > depths[0]:
                        end_boundary_y = -0.5
                    text_y = None
                    if start_boundary_y is not None and end_boundary_y is not None:
                        if start_boundary_y == -0.5 and end_boundary_y == -0.5:
                            text_y = -0.3
                        else:
                            text_y = (start_boundary_y + end_boundary_y) / 2.0
                            layer_thickness = abs(layer_end_depth - layer_start_depth)
                            visual_height = abs(start_boundary_y - end_boundary_y)
                            if layer_thickness <= 0.15:
                                pass
                            elif visual_height < 0.6:
                                if visual_height < 0.3:
                                    option_above = max(start_boundary_y, end_boundary_y) + 0.4
                                    option_below = min(start_boundary_y, end_boundary_y) - 0.4
                                    if option_above <= num_points - 0.8:
                                        text_y = option_above
                                    elif option_below >= -0.2:
                                        text_y = option_below
                                    else:
                                        text_y = (start_boundary_y + end_boundary_y) / 2.0
                    elif start_boundary_y is not None:
                        if start_boundary_y == -0.5:
                            text_y = -0.3
                        else:
                            text_y = start_boundary_y - 0.4
                            if text_y < 0.0:
                                text_y = start_boundary_y + 0.4
                    elif end_boundary_y is not None:
                        if end_boundary_y == -0.5:
                            text_y = -0.3
                        else:
                            text_y = end_boundary_y + 0.4
                            if text_y > num_points - 0.8:
                                text_y = end_boundary_y - 0.4
                    else:
                        layer_center_depth = (layer_start_depth + layer_end_depth) / 2.0
                        min_depth, max_depth = min(depths), max(depths)
                        if max_depth > min_depth:
                            depth_ratio = (max_depth - layer_center_depth) / (max_depth - min_depth)
                            text_y = depth_ratio * (num_points - 1)
                        else:
                            text_y = (num_points - 1) / 2.0
                    if text_y is not None and -0.5 <= text_y <= num_points:
                        description = layer['description']
                        max_chars = 18 if num_points <= 20 else 15 if num_points <= 40 else 12
                        if len(description) > max_chars:
                            description = description[:max_chars-3] + "..."
                        layer_thickness = abs(layer_end_depth - layer_start_depth)
                        if layer_thickness <= 0.10:
                            font_size = max(fs_labels - 2, 5)
                            rotation = 0
                        elif layer_thickness <= 0.30:
                            font_size = max(fs_labels - 1, 6)
                            rotation = 0
                        else:
                            font_size = fs_labels
                            rotation = 0
                        if len(description) > 12 and layer_thickness > 0.40:
                            rotation = 90
                        ax_profile.text(0.5, text_y, description, ha='center', va='center',
                                       fontsize=font_size, weight='bold',
                                       rotation=rotation,
                                       color='#000000', alpha=0.95)
        if ax_table is not None:
            ax_table.set_xlim(0, 1)
            ax_table.set_ylim(-0.5, num_points - 0.5)
            ax_table.axis('off')
            ax_table.set_facecolor('#FFFFFF')
        if ax_table is not None:
            header_y = num_points - 0.5 + 0.6
            header_fs = min(fs_table + 2, 12)
            ax_table.text(0.25, header_y, 'Id', ha='center', va='center',
                         fontsize=header_fs, weight='bold', color='black')
            ax_table.text(0.75, header_y, 'Is', ha='center', va='center',
                         fontsize=header_fs, weight='bold', color='black')
            ax_table.plot([0.05, 0.95], [num_points - 0.5, num_points - 0.5],
                         color='#000000', linewidth=2.0, alpha=1.0)
            ax_table.plot([0.05, 0.95], [-0.5, -0.5],
                         color='#000000', linewidth=2.0, alpha=1.0)
            ax_table.plot([0.05, 0.05], [-0.5, num_points - 0.5],
                         color='#000000', linewidth=2.0, alpha=1.0)
            ax_table.plot([0.95, 0.95], [-0.5, num_points - 0.5],
                         color='#000000', linewidth=2.0, alpha=1.0)
            ax_table.plot([0.5, 0.5], [-0.5, num_points - 0.5],
                         color='#000000', linewidth=1.0, alpha=0.6)
            for i in range(num_points + 1):
                y_line = i - 0.5
                ax_table.plot([0.05, 0.95], [y_line, y_line],
                             color='#000000', linewidth=1.0, alpha=0.6)
            for i, (ld, ls) in enumerate(zip(ld_values, ls_values)):
                y_pos = i
                if ld is not None:
                    if ld >= 1.0:
                        ld_text = f'{ld:.2f}'
                    else:
                        ld_text = f'{ld:.3f}'
                else:
                    ld_text = '-'
                if ls is not None:
                    if ls >= 1.0:
                        ls_text = f'{ls:.2f}'
                    else:
                        ls_text = f'{ls:.3f}'
                else:
                    ls_text = '-'
                ld_color = '#000000' if ld is not None else '#808080'
                ls_color = '#000000' if ls is not None else '#808080'
                ax_table.text(0.25, y_pos, ld_text, ha='center', va='center',
                             fontsize=fs_table, weight='bold', color=ld_color)
                ax_table.text(0.75, y_pos, ls_text, ha='center', va='center',
                             fontsize=fs_table, weight='bold', color=ls_color)
                color_index = num_points - 1 - i
                if color_index % 2 == 1:
                    ax_table.axhspan(y_pos - bar_height/2, y_pos + bar_height/2,
                                   xmin=0.05, xmax=0.95,
                                   facecolor='#E0E0E0', alpha=1.0, zorder=0)
        y_pos = range(num_points)
        for i in range(num_points):
            color_index = num_points - 1 - i
            if color_index % 2 == 1:
                self.ax.axhspan(i - bar_height/2, i + bar_height/2,
                               color='#E0E0E0', alpha=1.0, zorder=0)
        for i in range(num_points + 1):
            y_line = i - 0.5
            self.ax.axhline(y=y_line, xmin=0, xmax=1, color='#000000', linewidth=0.4, alpha=0.5, zorder=0.5)
        bars = []
        for i in range(num_points):
            bar = self.ax.barh([i], [n10_values[i]], facecolor='none',
                              edgecolor='#000000', linewidth=1.5,
                              alpha=1.0, height=bar_height, zorder=10, fill=False)
            bars.extend(bar)
        
        max_n10 = max(n10_values) if n10_values else 1
        all_n10_zero = all(val == 0 for val in n10_values)
        for i, (bar, val) in enumerate(zip(bars, n10_values)):
            if val == 0 or all_n10_zero:
                x_pos = 1
            else:
                x_pos = bar.get_width() + 1
            self.ax.text(x_pos, bar.get_y() + bar.get_height() / 2,
                         f'{val}', ha='left', va='center',
                         fontsize=fs_labels, weight='bold', color='#000000')
        self.ax.set_xlabel('Liczba udarzeń N10', fontsize=fs_main + 1, weight='bold', color='#000000', labelpad=25)
        self.ax.xaxis.set_label_position('top')
        self.ax.xaxis.tick_top()
        self.ax.set_ylabel('Punkty pomiarowe (głębokość)', fontsize=fs_main + 1, weight='bold', color='#000000')
        self.ax.set_title(f'Sondowanie dynamiczne DPL - Wyniki N10 ({num_points} punktów)',
                          fontsize=fs_main + 2, weight='bold', pad=20, color='#000000')
        min_depth, max_depth = min(depths), max(depths)
        tick_positions, tick_labels = [], []
        for i in range(num_points):
            point_order = sorted_data[i]['order']
            tick_positions.append(i)
            tick_labels.append(f'{point_order}')
        for i in range(num_points):
            tick_positions.append(i + 0.5)
            tick_labels.append(f'{depths[i]:.1f} m')
        if num_points > 0:
            tick_positions.append(-0.5)
            last_depth_extended = depths[0] + 0.10
            tick_labels.append(f'{last_depth_extended:.1f} m')
        self.ax.set_yticks(tick_positions)
        self.ax.set_yticklabels(tick_labels, fontsize=fs_labels, color='#000000')
        self.ax.set_xlim(0, 110)
        self.ax.set_xticks(range(0, 111, 10))
        self.ax.set_ylim(-0.5, num_points - 0.5)
        self.ax2 = self.ax.twiny()
        self.ax2.set_xlim(0, 110)
        self.ax2.set_xticks(range(0, 111, 10))
        self.ax2.set_xlabel('Liczba udarzeń N10', fontsize=fs_main + 1, weight='bold', color='#000000', labelpad=25)
        self.ax2.xaxis.set_label_position('bottom')
        self.ax2.tick_params(axis='x', colors='#000000', labelsize=fs_labels)
        self.ax.tick_params(axis='x', colors='#000000', labelsize=fs_labels)
        self.ax.tick_params(axis='y', colors='#000000', labelsize=fs_labels)
        for spine in self.ax.spines.values():
            spine.set_color('#000000')
            spine.set_linewidth(1.5)
        self.ax.set_axisbelow(True)
        self.ax.grid(True, alpha=0.5, axis='x', color='#000000', linestyle='-', linewidth=0.4, zorder=0)
        alpha_horizontal = 0.7
        max_n10_extended = 110
        if has_profile and self.profile_layers:
            boundary_color = '#000000'
            drawn_boundaries_main = set()
            max_chart_depth = depths[0] + 0.10
            shallowest_depth = min(depths) if depths else 0
            deepest_data_depth = max(depths) if depths else 0
            max_extended_depth = deepest_data_depth + 0.10
            sorted_layers = sorted(self.profile_layers, key=lambda x: x['depth_from'])
            for layer_idx, layer in enumerate(sorted_layers):
                if layer_idx % 2 == 1:
                    layer_start_depth = layer['depth_from']
                    layer_end_depth = layer['depth_to']
                    start_y = None
                    end_y = None
                    for i, depth in enumerate(depths):
                        if abs(depth - layer_start_depth) <= 0.01:
                            start_y = i - 0.5
                        if abs(depth - layer_end_depth) <= 0.01:
                            end_y = i + 0.5
                    max_extended_depth = depths[0] + 0.10 if depths else 0
                    if end_y is None and abs(layer_end_depth - max_extended_depth) <= 0.01:
                        end_y = -0.5
                    if start_y is not None and end_y is not None:
                        self.ax.axhspan(min(start_y, end_y), max(start_y, end_y),
                                      xmin=0.0, xmax=1.0,
                                      facecolor='#E0E0E0',
                                      alpha=0.3, zorder=0)
            for layer in self.profile_layers:
                layer_start_depth = layer['depth_from']
                layer_end_depth = layer['depth_to']
                if layer_start_depth not in drawn_boundaries_main:
                    start_y = None
                    is_boundary_depth = (abs(layer_start_depth - shallowest_depth) <= 0.01 or
                                       abs(layer_start_depth - max_extended_depth) <= 0.01)
                    if not is_boundary_depth:
                        for i, depth in enumerate(depths):
                            if abs(depth - layer_start_depth) <= 0.01:
                                start_y = i + 0.5
                                break
                        if start_y is None and layer_start_depth <= max_chart_depth and layer_start_depth > depths[0]:
                            depth_progress = (layer_start_depth - depths[0]) / 0.10
                            start_y = -0.5
                        if start_y is not None:
                            y_margin = 0.1
                            if start_y >= -0.5 and start_y < (num_points - 0.5 - y_margin):
                                self.ax.axhline(y=start_y, xmin=0.0, xmax=1.0,
                                              color='#000000', linewidth=1.2, alpha=0.8,
                                              linestyle='--', zorder=200)
                    drawn_boundaries_main.add(layer_start_depth)
                if layer_end_depth not in drawn_boundaries_main:
                    end_y = None
                    is_boundary_depth = (abs(layer_end_depth - shallowest_depth) <= 0.01 or
                                       abs(layer_end_depth - max_extended_depth) <= 0.01)
                    if not is_boundary_depth:
                        for i, depth in enumerate(depths):
                            if abs(depth - layer_end_depth) <= 0.01:
                                end_y = i + 0.5
                                break
                        if end_y is None and layer_end_depth <= max_chart_depth and layer_end_depth > depths[0]:
                            depth_progress = (layer_end_depth - depths[0]) / 0.10
                            end_y = -0.5
                        if end_y is not None:
                            y_margin = 0.1
                            if end_y >= -0.5 and end_y < (num_points - 0.5 - y_margin):
                                self.ax.axhline(y=end_y, xmin=0.0, xmax=1.0,
                                              color='#000000', linewidth=1.2, alpha=0.8,
                                              linestyle='--', zorder=200)
                    drawn_boundaries_main.add(layer_end_depth)
        self.ax.set_facecolor('#FFFFFF')
        self.fig.patch.set_facecolor('#FFFFFF')
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", message="This figure includes Axes that are not compatible with tight_layout")
                self.fig.tight_layout()
        except Exception:
            self.fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
        self.canvas.draw()
        fig_width_inches, fig_height_inches = self.fig.get_size_inches()
        fig_dpi = self.fig.dpi
        fig_height_px = int(fig_height_inches * fig_dpi)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.configure(height=fig_height_px)
        for _ in range(3):
            self.scrollable_frame.update()
            self.scroll_canvas.update()
            self.root.update()
        bbox = self.scroll_canvas.bbox("all")
        if bbox:
            self.scroll_canvas.configure(scrollregion=bbox)
        self.center_plot_view()
        scroll_info = " | Użyj kółka myszy lub pasków przewijania" if num_points > 20 else ""
        if not silent:
            self.status_var.set(f"✅ Wygenerowano wykres z tabelką dla {num_points} punktów")
        else:
            self.status_var.set(f"🔄 Wykres odświeżony - {num_points} punktów")
        self.update_plot_scrollbars()
        self.update_generate_button_text()
    def save_plot_dialog(self):
        if self.ax is None:
            CustomMessageBox.showinfo("Najpierw wygeneruj wykres klikając 'Generuj wykres'", "Brak wykresu")
            return
        file_path = filedialog.asksaveasfilename(
            title="Zapisz wykres",
            defaultextension=".png",
            filetypes=[("Pliki PNG", "*.png"), ("Pliki JPG", "*.jpg"), ("Pliki PDF", "*.pdf"), ("Wszystkie pliki", "*.*")]
        )
        if not file_path:
            return
        try:
            ext = os.path.splitext(file_path)[1].lower()
            a4_width_inches = 11.69
            a4_height_inches = 8.27
            original_size = self.fig.get_size_inches()
            original_dpi = self.fig.dpi
            self.fig.set_size_inches(a4_width_inches, a4_height_inches)
            if ext == '.pdf':
                self.fig.savefig(file_path, format='pdf',
                               bbox_inches='tight',
                               pad_inches=0.2,
                               facecolor='#FFFFFF',
                               edgecolor='none',
                               dpi=300,
                               metadata={'Creator': 'DPL Analyzer v2.0',
                                       'Title': 'Analiza zagęszczenia gruntu DPL'})
                format_info = "PDF A4 poziomo (wektorowy, 300 DPI)"
            elif ext in ('.jpg', '.jpeg'):
                self.fig.savefig(file_path, format='jpg',
                               dpi=300,
                               bbox_inches='tight',
                               pad_inches=0.2,
                               facecolor='#FFFFFF',
                               edgecolor='none',
                               quality=95,
                               pil_kwargs={'optimize': True, 'progressive': True})
                format_info = "JPG A4 poziomo (300 DPI, jakość 95%)"
            else:
                self.fig.savefig(file_path, format='png',
                               dpi=300,
                               bbox_inches='tight',
                               pad_inches=0.2,
                               facecolor='#FFFFFF',
                               edgecolor='none',
                               metadata={'Software': 'DPL Analyzer v2.0',
                                       'Description': 'Analiza zagęszczenia gruntu DPL'})
                format_info = "PNG A4 poziomo (300 DPI)"
            self.fig.set_size_inches(original_size[0], original_size[1])
            self.fig.set_dpi(original_dpi)
            self.canvas.draw()
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            CustomMessageBox.showsuccess(
                f"✓ Wykres zapisany pomyślnie!\n\n📁 Plik: {os.path.basename(file_path)}\n📊 Format: {format_info}\n📐 Rozmiar kartki: A4 poziomo (297×210 mm)\n💾 Rozmiar pliku: {size_mb:.2f} MB",
                "Wykres zapisany")
            self.status_var.set(f"✅ Zapisano wykres: {os.path.basename(file_path)} ({format_info}, {size_mb:.2f} MB)")
        except Exception as e:
            CustomMessageBox.showerror(f"Nie można zapisać wykresu:\n{e}", "Błąd zapisu")
            self.status_var.set("Błąd podczas zapisu wykresu")
            try:
                self.fig.set_size_inches(original_size[0], original_size[1])
                self.fig.set_dpi(original_dpi)
                self.canvas.draw()
            except:
                pass
if __name__ == "__main__":
    root = tk.Tk()
    app = DPLAnalyzer(root)
    root.mainloop()
