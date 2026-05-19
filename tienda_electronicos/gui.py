"""
gui.py - Interfaz gráfica con Login
CHATARRAS EL PANZON
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import BaseDatos
from reports import GeneradorReportes
from charts import GeneradorGraficos

ADMIN_EMAIL = "hebber@gmail"
ADMIN_PASS = "12345"
BG = "#1a1a2e"
BG2 = "#16213e"
ACCENT = "#e94560"
FG = "white"
FONT = "Segoe UI"

class AplicacionPrincipal:
    def __init__(self):
        self.db = BaseDatos()
        self.reportes = GeneradorReportes(self.db)
        self.graficos = GeneradorGraficos(self.db)
        self.root = tk.Tk()
        self.root.title("CHATARRAS EL PANZON")
        self.root.geometry("500x520")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self._estilos()
        self._login()

    def _estilos(self):
        s = ttk.Style(); s.theme_use("clam")
        s.configure("Title.TLabel", background=BG, foreground=ACCENT, font=(FONT,24,"bold"))
        s.configure("Sub.TLabel", background=BG, foreground="#aac", font=(FONT,10))
        s.configure("Menu.TButton", font=(FONT,11,"bold"), padding=14, background="#0f3460", foreground=FG)
        s.map("Menu.TButton", background=[("active",ACCENT)])
        s.configure("Action.TButton", font=(FONT,10), padding=8, background=ACCENT, foreground=FG)
        s.map("Action.TButton", background=[("active","#c81e45")])
        s.configure("Treeview", font=(FONT,9), rowheight=26, background=BG2, foreground=FG, fieldbackground=BG2)
        s.configure("Treeview.Heading", font=(FONT,10,"bold"), background="#0f3460", foreground=FG)
        s.map("Treeview", background=[("selected",ACCENT)])

    def _limpiar(self):
        for w in self.root.winfo_children(): w.destroy()

    # ==================== LOGIN ====================
    def _login(self):
        self._limpiar()
        self.root.geometry("500x520")
        tk.Label(self.root, text="🔧", font=(FONT,48), bg=BG, fg=ACCENT).pack(pady=(30,0))
        tk.Label(self.root, text="CHATARRAS EL PANZON", font=(FONT,22,"bold"), bg=BG, fg=ACCENT).pack()
        tk.Label(self.root, text="Tienda de Electrónicos", font=(FONT,10), bg=BG, fg="#aac").pack(pady=(0,20))
        f = tk.Frame(self.root, bg=BG2, padx=30, pady=20); f.pack(padx=40, fill="x")
        tk.Label(f, text="Correo:", bg=BG2, fg=FG, font=(FONT,10)).pack(anchor="w")
        self.e_email = ttk.Entry(f, width=35); self.e_email.pack(pady=(0,8))
        tk.Label(f, text="Contraseña:", bg=BG2, fg=FG, font=(FONT,10)).pack(anchor="w")
        self.e_pass = ttk.Entry(f, width=35, show="*"); self.e_pass.pack(pady=(0,15))
        ttk.Button(f, text="🔑 Admin", command=self._login_admin, style="Action.TButton").pack(fill="x", pady=3)
        ttk.Button(f, text="🛒 Entrar como Cliente", command=self._login_usuario, style="Action.TButton").pack(fill="x", pady=3)

    def _login_admin(self):
        if self.e_email.get()==ADMIN_EMAIL and self.e_pass.get()==ADMIN_PASS:
            print("[TERMINAL] ✅ Admin conectado"); self._panel_admin()
        else: messagebox.showerror("Error","Credenciales incorrectas")

    def _login_usuario(self):
        nombre = self.e_email.get().strip()
        if not nombre: messagebox.showwarning("Aviso","Escribe tu correo"); return
        print(f"[TERMINAL] 🛒 Cliente: {nombre}"); self._tienda_usuario(nombre)

    # ==================== PANEL ADMIN ====================
    def _panel_admin(self):
        self._limpiar(); self.root.geometry("1500x800")
        tk.Label(self.root, text="⚡ CHATARRAS EL PANZON - Admin", font=(FONT,20,"bold"), bg=BG, fg=ACCENT).pack(pady=(15,5))
        self._resumen()
        mf = tk.Frame(self.root, bg=BG); mf.pack(expand=True, fill="both", padx=40, pady=10)
        btns = [("📦 Productos",self._v_productos),("👥 Clientes",self._v_clientes),
                ("🏪 Inventario",self._v_inventario),("💰 Ventas",self._v_ventas),
                ("🔍 Búsqueda",self._v_busqueda),("📊 Reportes",self._v_reportes),
                ("📈 Gráficos",self._v_graficos),("🔙 Cerrar Sesión",self._login)]
        for i,(t,c) in enumerate(btns):
            r,co=divmod(i,4)
            ttk.Button(mf,text=t,command=c,style="Menu.TButton").grid(row=r,column=co,padx=8,pady=8,sticky="nsew")
            mf.columnconfigure(co,weight=1); mf.rowconfigure(r,weight=1)

    def _resumen(self):
        f=tk.Frame(self.root,bg=BG2); f.pack(fill="x",padx=40,pady=8)
        productos = self.db.obtener_productos()
        clientes  = self.db.obtener_clientes()
        ventas    = self.db.obtener_ventas()
        for l,v in [("Productos",len(productos)),("Clientes",len(clientes)),
                     ("Ventas",len(ventas)),("Ingresos",f"${sum(v.total for v in ventas):,.0f}")]:
            sf=tk.Frame(f,bg=BG2); sf.pack(side="left",expand=True,fill="both",padx=15,pady=8)
            tk.Label(sf,text=str(v),font=(FONT,16,"bold"),bg=BG2,fg=ACCENT).pack()
            tk.Label(sf,text=l,font=(FONT,9),bg=BG2,fg="#aac").pack()

    # ==================== TIENDA USUARIO ====================
    def _tienda_usuario(self, nombre_usuario):
        self._limpiar(); self.root.geometry("900x650")
        self.carrito = []
        tk.Label(self.root,text=f"🛒 CHATARRAS EL PANZON - Bienvenido",font=(FONT,18,"bold"),bg=BG,fg=ACCENT).pack(pady=(10,0))
        tk.Label(self.root,text=f"Cliente: {nombre_usuario}",font=(FONT,10),bg=BG,fg="#aac").pack()
        pf=tk.Frame(self.root,bg=BG); pf.pack(fill="both",expand=True,padx=15,pady=5)
        # Productos
        lf=tk.LabelFrame(pf,text=" Productos Disponibles ",bg=BG2,fg=ACCENT,font=(FONT,11,"bold")); lf.pack(side="left",fill="both",expand=True,padx=(0,5))
        cols=("ID","Producto","Marca","Precio","Stock")
        tree=ttk.Treeview(lf,columns=cols,show="headings",height=12)
        for c in cols: tree.heading(c,text=c); tree.column(c,width=90,anchor="center")
        for p in self.db.obtener_productos():
            tree.insert("","end",values=(p.id,p.nombre,p.marca,f"${p.precio:,.2f}",p.stock))
        tree.pack(fill="both",expand=True,padx=5,pady=5)
        # Carrito
        rf=tk.LabelFrame(pf,text=" Mi Carrito ",bg=BG2,fg=ACCENT,font=(FONT,11,"bold")); rf.pack(side="right",fill="both",expand=True,padx=(5,0))
        cart_cols=("Producto","Cant.","Subtotal")
        cart_tree=ttk.Treeview(rf,columns=cart_cols,show="headings",height=10)
        for c in cart_cols: cart_tree.heading(c,text=c); cart_tree.column(c,width=90,anchor="center")
        cart_tree.pack(fill="both",expand=True,padx=5,pady=5)
        self.lbl_total=tk.Label(rf,text="Total: $0.00",font=(FONT,13,"bold"),bg=BG2,fg="#4ECDC4")
        self.lbl_total.pack(pady=5)
        # Botones
        bf=tk.Frame(self.root,bg=BG); bf.pack(fill="x",padx=15,pady=8)
        def agregar_carrito():
            sel=tree.selection()
            if not sel: messagebox.showwarning("Aviso","Selecciona un producto"); return
            vals=tree.item(sel[0])["values"]; pid=vals[0]
            cant=simpledialog.askinteger("Cantidad","¿Cuántas unidades?",parent=self.root,minvalue=1)
            if not cant: return
            prod=self.db.obtener_producto_por_id(pid)
            if cant>prod.stock: messagebox.showerror("Error",f"Solo hay {prod.stock} en stock"); return
            self.carrito.append({"id":pid,"nombre":prod.nombre,"cant":cant,"precio":prod.precio,"sub":prod.precio*cant})
            for it in cart_tree.get_children(): cart_tree.delete(it)
            for item in self.carrito: cart_tree.insert("","end",values=(item["nombre"],item["cant"],f"${item['sub']:,.2f}"))
            self.lbl_total.config(text=f"Total: ${sum(i['sub'] for i in self.carrito):,.2f}")
        def comprar():
            if not self.carrito: messagebox.showwarning("Aviso","Carrito vacío"); return
            total_compra = sum(i["sub"] for i in self.carrito)

            # ── Ventana de Método de Pago (blanco y gris) ──
            pay_win = tk.Toplevel(self.root)
            pay_win.title("Método de Pago")
            pay_win.geometry("1000x800")
            pay_win.configure(bg="#f5f5f5")
            pay_win.resizable(False, False)
            pay_win.grab_set()

            # Colores del tema blanco/gris
            PAY_BG = "#f5f5f5"
            PAY_CARD = "#ffffff"
            PAY_BORDER = "#e0e0e0"
            PAY_TEXT = "#333333"
            PAY_SUBTEXT = "#777777"
            PAY_ACCENT = "#444444"
            PAY_BTN = "#4a4a4a"
            PAY_BTN_HOVER = "#333333"
            PAY_GREEN = "#4CAF50"

            # ── Título ──
            header_f = tk.Frame(pay_win, bg=PAY_CARD, highlightbackground=PAY_BORDER, highlightthickness=1)
            header_f.pack(fill="x", padx=20, pady=(20, 10))
            tk.Label(header_f, text="💳 Finalizar Compra", font=(FONT, 18, "bold"),
                     bg=PAY_CARD, fg=PAY_TEXT).pack(pady=(15, 5))
            tk.Label(header_f, text=f"Total a pagar: ${total_compra:,.2f}",
                     font=(FONT, 14, "bold"), bg=PAY_CARD, fg=PAY_GREEN).pack(pady=(0, 15))

            # Canvas con scroll para el contenido
            canvas = tk.Canvas(pay_win, bg=PAY_BG, highlightthickness=0)
            scrollbar = ttk.Scrollbar(pay_win, orient="vertical", command=canvas.yview)
            scroll_frame = tk.Frame(canvas, bg=PAY_BG)
            scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=480)
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True, padx=(20, 0))
            scrollbar.pack(side="right", fill="y", padx=(0, 5))

            # Scroll con rueda del mouse
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

            # ── Resumen del pedido ──
            resumen_f = tk.LabelFrame(scroll_frame, text=" 📦 Resumen del Pedido ",
                                       bg=PAY_CARD, fg=PAY_ACCENT, font=(FONT, 11, "bold"),
                                       highlightbackground=PAY_BORDER, highlightthickness=1,
                                       padx=15, pady=10)
            resumen_f.pack(fill="x", padx=10, pady=(10, 5))
            for item in self.carrito:
                row_f = tk.Frame(resumen_f, bg=PAY_CARD)
                row_f.pack(fill="x", pady=2)
                tk.Label(row_f, text=f"• {item['nombre']} x{item['cant']}",
                         font=(FONT, 10), bg=PAY_CARD, fg=PAY_TEXT, anchor="w").pack(side="left")
                tk.Label(row_f, text=f"${item['sub']:,.2f}",
                         font=(FONT, 10, "bold"), bg=PAY_CARD, fg=PAY_TEXT, anchor="e").pack(side="right")
            sep = tk.Frame(resumen_f, bg=PAY_BORDER, height=1)
            sep.pack(fill="x", pady=(8, 5))
            total_row = tk.Frame(resumen_f, bg=PAY_CARD)
            total_row.pack(fill="x")
            tk.Label(total_row, text="TOTAL:", font=(FONT, 12, "bold"),
                     bg=PAY_CARD, fg=PAY_TEXT).pack(side="left")
            tk.Label(total_row, text=f"${total_compra:,.2f}", font=(FONT, 12, "bold"),
                     bg=PAY_CARD, fg=PAY_GREEN).pack(side="right")

            # ── Método de pago ──
            metodo_f = tk.LabelFrame(scroll_frame, text=" 💳 Método de Pago ",
                                      bg=PAY_CARD, fg=PAY_ACCENT, font=(FONT, 11, "bold"),
                                      highlightbackground=PAY_BORDER, highlightthickness=1,
                                      padx=15, pady=10)
            metodo_f.pack(fill="x", padx=10, pady=5)

            metodo_var = tk.StringVar(value="credito")
            metodos = [
                ("💳  Tarjeta de Crédito", "credito"),
                ("💳  Tarjeta de Débito", "debito"),
                ("🅿️  PayPal", "paypal"),
                ("🏦  Transferencia Bancaria", "transferencia"),
            ]
            for texto, valor in metodos:
                rb = tk.Radiobutton(metodo_f, text=texto, variable=metodo_var, value=valor,
                                    font=(FONT, 10), bg=PAY_CARD, fg=PAY_TEXT,
                                    selectcolor=PAY_BG, activebackground=PAY_CARD,
                                    activeforeground=PAY_TEXT, anchor="w",
                                    command=lambda: _toggle_tarjeta())
                rb.pack(fill="x", pady=2)

            # ── Información de tarjeta ──
            tarjeta_f = tk.LabelFrame(scroll_frame, text=" 🔒 Información de la Tarjeta ",
                                       bg=PAY_CARD, fg=PAY_ACCENT, font=(FONT, 11, "bold"),
                                       highlightbackground=PAY_BORDER, highlightthickness=1,
                                       padx=15, pady=10)
            tarjeta_f.pack(fill="x", padx=10, pady=5)

            tk.Label(tarjeta_f, text="Número de Tarjeta:", font=(FONT, 10),
                     bg=PAY_CARD, fg=PAY_SUBTEXT).pack(anchor="w", pady=(5, 0))
            e_num_tarjeta = tk.Entry(tarjeta_f, font=(FONT, 12), relief="solid", bd=1,
                                      bg="white", fg=PAY_TEXT, insertbackground=PAY_TEXT)
            e_num_tarjeta.pack(fill="x", pady=(2, 8), ipady=5)
            e_num_tarjeta.insert(0, "")

            tk.Label(tarjeta_f, text="Nombre del Titular:", font=(FONT, 10),
                     bg=PAY_CARD, fg=PAY_SUBTEXT).pack(anchor="w", pady=(0, 0))
            e_titular = tk.Entry(tarjeta_f, font=(FONT, 12), relief="solid", bd=1,
                                  bg="white", fg=PAY_TEXT, insertbackground=PAY_TEXT)
            e_titular.pack(fill="x", pady=(2, 8), ipady=5)

            row_exp_cvv = tk.Frame(tarjeta_f, bg=PAY_CARD)
            row_exp_cvv.pack(fill="x", pady=(0, 5))

            left_col = tk.Frame(row_exp_cvv, bg=PAY_CARD)
            left_col.pack(side="left", fill="x", expand=True, padx=(0, 10))
            tk.Label(left_col, text="Fecha de Expiración (MM/AA):", font=(FONT, 10),
                     bg=PAY_CARD, fg=PAY_SUBTEXT).pack(anchor="w")
            e_exp = tk.Entry(left_col, font=(FONT, 12), relief="solid", bd=1,
                              bg="white", fg=PAY_TEXT, insertbackground=PAY_TEXT, width=12)
            e_exp.pack(fill="x", ipady=5)

            right_col = tk.Frame(row_exp_cvv, bg=PAY_CARD)
            right_col.pack(side="right", fill="x", expand=True)
            tk.Label(right_col, text="CVV:", font=(FONT, 10),
                     bg=PAY_CARD, fg=PAY_SUBTEXT).pack(anchor="w")
            e_cvv = tk.Entry(right_col, font=(FONT, 12), relief="solid", bd=1,
                              bg="white", fg=PAY_TEXT, insertbackground=PAY_TEXT, width=8, show="*")
            e_cvv.pack(fill="x", ipady=5)

            # ── Función para mostrar/ocultar campos de tarjeta ──
            def _toggle_tarjeta():
                metodo = metodo_var.get()
                if metodo in ("credito", "debito"):
                    tarjeta_f.pack(fill="x", padx=10, pady=5, after=metodo_f)
                else:
                    tarjeta_f.pack_forget()

            # ── Dirección de envío ──
            envio_f = tk.LabelFrame(scroll_frame, text=" 📍 Dirección de Envío ",
                                     bg=PAY_CARD, fg=PAY_ACCENT, font=(FONT, 11, "bold"),
                                     highlightbackground=PAY_BORDER, highlightthickness=1,
                                     padx=15, pady=10)
            envio_f.pack(fill="x", padx=10, pady=5)

            tk.Label(envio_f, text="Calle y Número:", font=(FONT, 10),
                     bg=PAY_CARD, fg=PAY_SUBTEXT).pack(anchor="w", pady=(5, 0))
            e_calle = tk.Entry(envio_f, font=(FONT, 12), relief="solid", bd=1,
                                bg="white", fg=PAY_TEXT, insertbackground=PAY_TEXT)
            e_calle.pack(fill="x", pady=(2, 8), ipady=5)

            row_ciudad = tk.Frame(envio_f, bg=PAY_CARD)
            row_ciudad.pack(fill="x", pady=(0, 5))

            col_ciudad = tk.Frame(row_ciudad, bg=PAY_CARD)
            col_ciudad.pack(side="left", fill="x", expand=True, padx=(0, 10))
            tk.Label(col_ciudad, text="Ciudad:", font=(FONT, 10),
                     bg=PAY_CARD, fg=PAY_SUBTEXT).pack(anchor="w")
            e_ciudad = tk.Entry(col_ciudad, font=(FONT, 12), relief="solid", bd=1,
                                 bg="white", fg=PAY_TEXT, insertbackground=PAY_TEXT)
            e_ciudad.pack(fill="x", ipady=5)

            col_estado = tk.Frame(row_ciudad, bg=PAY_CARD)
            col_estado.pack(side="left", fill="x", expand=True, padx=(0, 10))
            tk.Label(col_estado, text="Estado:", font=(FONT, 10),
                     bg=PAY_CARD, fg=PAY_SUBTEXT).pack(anchor="w")
            e_estado = tk.Entry(col_estado, font=(FONT, 12), relief="solid", bd=1,
                                 bg="white", fg=PAY_TEXT, insertbackground=PAY_TEXT)
            e_estado.pack(fill="x", ipady=5)

            col_cp = tk.Frame(row_ciudad, bg=PAY_CARD)
            col_cp.pack(side="right", fill="x", expand=True)
            tk.Label(col_cp, text="C.P.:", font=(FONT, 10),
                     bg=PAY_CARD, fg=PAY_SUBTEXT).pack(anchor="w")
            e_cp = tk.Entry(col_cp, font=(FONT, 12), relief="solid", bd=1,
                             bg="white", fg=PAY_TEXT, insertbackground=PAY_TEXT, width=8)
            e_cp.pack(fill="x", ipady=5)

            # ── Botones finales ──
            btn_frame = tk.Frame(pay_win, bg=PAY_BG)
            btn_frame.pack(fill="x", padx=20, pady=(10, 20))

            def confirmar_pago():
                metodo = metodo_var.get()
                # Validar campos de tarjeta si aplica
                if metodo in ("credito", "debito"):
                    if not e_num_tarjeta.get().strip():
                        messagebox.showwarning("Aviso", "Ingresa el número de tarjeta", parent=pay_win); return
                    if not e_titular.get().strip():
                        messagebox.showwarning("Aviso", "Ingresa el nombre del titular", parent=pay_win); return
                    if not e_exp.get().strip():
                        messagebox.showwarning("Aviso", "Ingresa la fecha de expiración", parent=pay_win); return
                    if not e_cvv.get().strip():
                        messagebox.showwarning("Aviso", "Ingresa el CVV", parent=pay_win); return
                # Validar dirección
                if not e_calle.get().strip():
                    messagebox.showwarning("Aviso", "Ingresa la dirección de envío", parent=pay_win); return
                if not e_ciudad.get().strip():
                    messagebox.showwarning("Aviso", "Ingresa la ciudad", parent=pay_win); return
                if not e_estado.get().strip():
                    messagebox.showwarning("Aviso", "Ingresa el estado", parent=pay_win); return
                if not e_cp.get().strip():
                    messagebox.showwarning("Aviso", "Ingresa el código postal", parent=pay_win); return

                # Construir dirección completa
                direccion_completa = f"{e_calle.get().strip()}, {e_ciudad.get().strip()}, {e_estado.get().strip()}, C.P. {e_cp.get().strip()}"

                # Procesar la compra
                cl = self.db.buscar_clientes(nombre_usuario)
                if not cl:
                    cl_obj = self.db.agregar_cliente(nombre_usuario, nombre_usuario, direccion_completa)
                    cid = cl_obj.id
                else:
                    cid = cl[0].id
                    cl[0].direccion = direccion_completa

                ok = True
                for item in self.carrito:
                    v = self.db.registrar_venta(item["id"], item["cant"], cid)
                    if not v:
                        ok = False

                # Limpiar binding del mousewheel antes de cerrar
                canvas.unbind_all("<MouseWheel>")

                if ok:
                    metodo_nombres = {"credito": "Tarjeta de Crédito", "debito": "Tarjeta de Débito",
                                      "paypal": "PayPal", "transferencia": "Transferencia Bancaria"}
                    pay_win.destroy()
                    messagebox.showinfo("✅ Compra Exitosa",
                                        f"Total: ${total_compra:,.2f}\n"
                                        f"Método: {metodo_nombres[metodo]}\n"
                                        f"Envío a: {direccion_completa}\n\n"
                                        f"¡Gracias por tu compra!")
                    self.carrito.clear()
                    for it in cart_tree.get_children(): cart_tree.delete(it)
                    self.lbl_total.config(text="Total: $0.00")
                    for it in tree.get_children(): tree.delete(it)
                    for p in self.db.obtener_productos():
                        tree.insert("", "end", values=(p.id, p.nombre, p.marca, f"${p.precio:,.2f}", p.stock))
                else:
                    pay_win.destroy()
                    messagebox.showerror("Error", "Hubo un problema con la compra")

            def cancelar_pago():
                canvas.unbind_all("<MouseWheel>")
                pay_win.destroy()

            btn_confirmar = tk.Button(btn_frame, text="✅  Confirmar Pago", font=(FONT, 12, "bold"),
                                      bg=PAY_GREEN, fg="white", activebackground="#43A047",
                                      activeforeground="white", relief="flat", cursor="hand2",
                                      padx=20, pady=10, command=confirmar_pago)
            btn_confirmar.pack(side="left", expand=True, fill="x", padx=(0, 5))

            btn_cancelar = tk.Button(btn_frame, text="❌  Cancelar", font=(FONT, 12, "bold"),
                                     bg="#bdbdbd", fg=PAY_TEXT, activebackground="#9e9e9e",
                                     activeforeground=PAY_TEXT, relief="flat", cursor="hand2",
                                     padx=20, pady=10, command=cancelar_pago)
            btn_cancelar.pack(side="right", expand=True, fill="x", padx=(5, 0))

            pay_win.protocol("WM_DELETE_WINDOW", cancelar_pago)
        def quitar():
            sel=cart_tree.selection()
            if not sel: return
            idx=cart_tree.index(sel[0]); self.carrito.pop(idx)
            for it in cart_tree.get_children(): cart_tree.delete(it)
            for item in self.carrito: cart_tree.insert("","end",values=(item["nombre"],item["cant"],f"${item['sub']:,.2f}"))
            self.lbl_total.config(text=f"Total: ${sum(i['sub'] for i in self.carrito):,.2f}")
        ttk.Button(bf,text="➕ Agregar al Carrito",command=agregar_carrito,style="Action.TButton").pack(side="left",padx=5)
        ttk.Button(bf,text="➖ Quitar del Carrito",command=quitar,style="Action.TButton").pack(side="left",padx=5)
        ttk.Button(bf,text="💰 Comprar",command=comprar,style="Action.TButton").pack(side="left",padx=5)
        ttk.Button(bf,text="🔙 Cerrar Sesión",command=self._login,style="Action.TButton").pack(side="right",padx=5)

    # ==================== HELPERS ====================
    def _win(self,t,w=850,h=550):
        win=tk.Toplevel(self.root); win.title(t); win.geometry(f"{w}x{h}"); win.configure(bg=BG); win.grab_set()
        ttk.Label(win,text=t,style="Title.TLabel").pack(pady=(10,5)); return win

    def _tabla(self,parent,cols,datos,h=12):
        c=tk.Frame(parent,bg=BG); c.pack(fill="both",expand=True,padx=15,pady=5)
        sy=ttk.Scrollbar(c,orient="vertical"); sy.pack(side="right",fill="y")
        t=ttk.Treeview(c,columns=cols,show="headings",height=h,yscrollcommand=sy.set); sy.config(command=t.yview)
        for col in cols: t.heading(col,text=col); t.column(col,width=100,anchor="center")
        for f in datos: t.insert("","end",values=f)
        t.pack(fill="both",expand=True); return t

    def _ref(self,t,d):
        for i in t.get_children(): t.delete(i)
        for f in d: t.insert("","end",values=f)

    # ==================== VENTANAS ADMIN ====================
    def _v_productos(self):
        win=self._win("📦 Productos",900,600)
        cols=("ID","Nombre","Marca","Precio","Categoría","Stock")
        datos=[(p.id,p.nombre,p.marca,f"${p.precio:,.2f}",p.categoria,p.stock) for p in self.db.obtener_productos()]
        tree=self._tabla(win,cols,datos)
        bf=tk.Frame(win,bg=BG); bf.pack(fill="x",padx=15,pady=10)
        def agregar():
            d=_DlgProd(win)
            if d.r: self.db.agregar_producto(*d.r); self._ref(tree,[(p.id,p.nombre,p.marca,f"${p.precio:,.2f}",p.categoria,p.stock) for p in self.db.obtener_productos()])
        def eliminar():
            s=tree.selection()
            if not s: return
            if messagebox.askyesno("Confirmar","¿Eliminar?"): self.db.eliminar_producto(tree.item(s[0])["values"][0]); self._ref(tree,[(p.id,p.nombre,p.marca,f"${p.precio:,.2f}",p.categoria,p.stock) for p in self.db.obtener_productos()])
        ttk.Button(bf,text="➕ Agregar",command=agregar,style="Action.TButton").pack(side="left",padx=5)
        ttk.Button(bf,text="🗑️ Eliminar",command=eliminar,style="Action.TButton").pack(side="left",padx=5)
        ttk.Button(bf,text="Cerrar",command=win.destroy,style="Action.TButton").pack(side="right",padx=5)

    def _v_clientes(self):
        win=self._win("👥 Clientes",900,600)
        cols=("ID","Nombre","Contacto","Dirección","Compras")
        datos=[(c.id,c.nombre,c.contacto,c.direccion,len(c.historial_compras)) for c in self.db.obtener_clientes()]
        tree=self._tabla(win,cols,datos)
        bf=tk.Frame(win,bg=BG); bf.pack(fill="x",padx=15,pady=10)
        def agregar():
            d=_DlgCli(win)
            if d.r: self.db.agregar_cliente(*d.r); self._ref(tree,[(c.id,c.nombre,c.contacto,c.direccion,len(c.historial_compras)) for c in self.db.obtener_clientes()])
        def historial():
            s=tree.selection()
            if not s: return
            cid=tree.item(s[0])["values"][0]; cl=self.db.obtener_cliente_por_id(cid)
            hw=self._win(f"Historial - {cl.nombre}",700,400)
            self._tabla(hw,("ID","Fecha","Producto","Cant.","Total"),[(v.id,v.fecha,v.producto_nombre,v.cantidad,f"${v.total:,.2f}") for v in self.db.buscar_ventas_por_cliente(cid)])
        ttk.Button(bf,text="➕ Agregar",command=agregar,style="Action.TButton").pack(side="left",padx=5)
        ttk.Button(bf,text="📋 Historial",command=historial,style="Action.TButton").pack(side="left",padx=5)
        ttk.Button(bf,text="Cerrar",command=win.destroy,style="Action.TButton").pack(side="right",padx=5)

    def _v_inventario(self):
        win=self._win("🏪 Inventario",900,600)
        def datos():
            return [(p.id,p.nombre,p.marca,p.categoria,p.stock,"🔴 BAJO" if p.stock<=10 else("🟡 MEDIO" if p.stock<=30 else "🟢 OK")) for p in self.db.obtener_productos()]
        tree=self._tabla(win,("ID","Producto","Marca","Categoría","Stock","Estado"),datos())
        bf=tk.Frame(win,bg=BG); bf.pack(fill="x",padx=15,pady=10)
        def entrada():
            s=tree.selection()
            if not s: return
            c=simpledialog.askinteger("Entrada","Cantidad:",parent=win,minvalue=1)
            if c: self.db.entrada_inventario(tree.item(s[0])["values"][0],c); self._ref(tree,datos())
        def salida():
            s=tree.selection()
            if not s: return
            c=simpledialog.askinteger("Salida","Cantidad:",parent=win,minvalue=1)
            if c:
                if not self.db.salida_inventario(tree.item(s[0])["values"][0],c): messagebox.showerror("Error","Stock insuficiente")
                self._ref(tree,datos())
        ttk.Button(bf,text="📦 Entrada",command=entrada,style="Action.TButton").pack(side="left",padx=5)
        ttk.Button(bf,text="📤 Salida",command=salida,style="Action.TButton").pack(side="left",padx=5)
        ttk.Button(bf,text="Cerrar",command=win.destroy,style="Action.TButton").pack(side="right",padx=5)

    def _v_ventas(self):
        win=self._win("💰 Ventas",950,650)
        cols=("ID","Fecha","Producto","Cant.","Cliente","Total")
        datos=[(v.id,v.fecha,v.producto_nombre,v.cantidad,v.cliente_nombre,f"${v.total:,.2f}") for v in self.db.obtener_ventas()]
        tree=self._tabla(win,cols,datos,h=8)
        form=tk.LabelFrame(win,text=" Nueva Venta ",bg=BG2,fg=ACCENT,font=(FONT,11,"bold"),padx=15,pady=10); form.pack(fill="x",padx=15,pady=10)
        tk.Label(form,text="Producto:",bg=BG2,fg=FG,font=(FONT,10)).grid(row=0,column=0,sticky="w")
        cp=ttk.Combobox(form,state="readonly",width=30,values=[f"{p.id} - {p.nombre} (Stock:{p.stock})" for p in self.db.obtener_productos()]); cp.grid(row=0,column=1,padx=10)
        tk.Label(form,text="Cliente:",bg=BG2,fg=FG,font=(FONT,10)).grid(row=0,column=2,sticky="w")
        cc=ttk.Combobox(form,state="readonly",width=30,values=[f"{c.id} - {c.nombre}" for c in self.db.obtener_clientes()]); cc.grid(row=0,column=3,padx=10)
        tk.Label(form,text="Cantidad:",bg=BG2,fg=FG,font=(FONT,10)).grid(row=1,column=0,sticky="w",pady=5)
        ec=ttk.Entry(form,width=10); ec.grid(row=1,column=1,sticky="w",padx=10)
        def reg():
            if not cp.get() or not cc.get() or not ec.get(): messagebox.showwarning("Aviso","Completa campos"); return
            try: pid=int(cp.get().split(" - ")[0]); cid=int(cc.get().split(" - ")[0]); cant=int(ec.get())
            except: messagebox.showerror("Error","Valores inválidos"); return
            v=self.db.registrar_venta(pid,cant,cid)
            if v: messagebox.showinfo("Éxito",f"Total: ${v.total:,.2f}"); self._ref(tree,[(v.id,v.fecha,v.producto_nombre,v.cantidad,v.cliente_nombre,f"${v.total:,.2f}") for v in self.db.obtener_ventas()]); ec.delete(0,"end")
            else: messagebox.showerror("Error","Revisa la terminal")
        ttk.Button(form,text="💰 Registrar",command=reg,style="Action.TButton").grid(row=1,column=2,columnspan=2)
        ttk.Button(win,text="Cerrar",command=win.destroy,style="Action.TButton").pack(pady=5)

    def _v_busqueda(self):
        win=self._win("🔍 Búsqueda",900,600)
        sf=tk.Frame(win,bg=BG2,padx=15,pady=10); sf.pack(fill="x",padx=15,pady=5)
        tk.Label(sf,text="Buscar:",bg=BG2,fg=FG,font=(FONT,10)).pack(side="left")
        e=ttk.Entry(sf,width=30); e.pack(side="left",padx=10)
        tk.Label(sf,text="Campo:",bg=BG2,fg=FG,font=(FONT,10)).pack(side="left")
        cb=ttk.Combobox(sf,state="readonly",width=15,values=["nombre","marca","categoria","precio","cliente"]); cb.set("nombre"); cb.pack(side="left",padx=10)
        cols=("ID","Nombre","Marca","Precio","Categoría","Stock"); tree=self._tabla(win,cols,[])
        def buscar():
            campo=cb.get(); t=e.get().strip()
            if campo=="cliente":
                r=self.db.buscar_clientes(t); tree["columns"]=("ID","Nombre","Contacto","Dirección","Compras")
                for c in tree["columns"]: tree.heading(c,text=c); tree.column(c,width=120,anchor="center")
                self._ref(tree,[(c.id,c.nombre,c.contacto,c.direccion,len(c.historial_compras)) for c in r])
            else:
                r=self.db.buscar_productos(t,campo); tree["columns"]=cols
                for c in cols: tree.heading(c,text=c); tree.column(c,width=100,anchor="center")
                self._ref(tree,[(p.id,p.nombre,p.marca,f"${p.precio:,.2f}",p.categoria,p.stock) for p in r])
        ttk.Button(sf,text="🔍 Buscar",command=buscar,style="Action.TButton").pack(side="left",padx=10)
        ttk.Button(win,text="Cerrar",command=win.destroy,style="Action.TButton").pack(side="bottom",pady=10)

    def _v_reportes(self):
        win=self._win("📊 Reportes",700,450)
        tk.Label(win,text="Los reportes se muestran en la terminal",font=(FONT,10),bg=BG,fg="#aac").pack(pady=5)
        bf=tk.Frame(win,bg=BG); bf.pack(expand=True)
        for t,c in [("📋 Resumen General",self.reportes.resumen_general),("🏆 Más Vendidos",self.reportes.productos_mas_vendidos),
                     ("⚠️ Bajo Stock",self.reportes.productos_bajo_stock),("👥 Clientes Top",self.reportes.clientes_top)]:
            def go(cmd=c): cmd(); messagebox.showinfo("Listo","Revisa la terminal")
            ttk.Button(bf,text=t,command=go,style="Menu.TButton").pack(fill="x",padx=40,pady=8)
        ttk.Button(win,text="Cerrar",command=win.destroy,style="Action.TButton").pack(pady=10)

    def _v_graficos(self):
        win=self._win("📈 Gráficos",700,400)
        bf=tk.Frame(win,bg=BG); bf.pack(expand=True)
        for t,c in [("📊 Ventas por Categoría",self.graficos.ventas_por_categoria),("📈 Tendencia",self.graficos.tendencia_ventas),("📉 Comparativa",self.graficos.comparativa_productos)]:
            ttk.Button(bf,text=t,command=c,style="Menu.TButton").pack(fill="x",padx=40,pady=8)
        ttk.Button(win,text="Cerrar",command=win.destroy,style="Action.TButton").pack(pady=10)

    def ejecutar(self): self.root.mainloop()

# ==================== DIALOGOS ====================
class _DlgProd:
    def __init__(self,parent):
        self.r=None; w=tk.Toplevel(parent); w.title("Agregar Producto"); w.geometry("400x350"); w.configure(bg=BG); w.grab_set()
        self.entries=[]
        for campo in ["Nombre:","Marca:","Precio:","Categoría:","Stock:"]:
            tk.Label(w,text=campo,bg=BG,fg=FG,font=(FONT,10)).pack(anchor="w",padx=30,pady=(5,0))
            e=ttk.Entry(w,width=35); e.pack(padx=30); self.entries.append(e)
        def guardar():
            v=[e.get().strip() for e in self.entries]
            if not all(v): messagebox.showwarning("Aviso","Completa campos",parent=w); return
            try: self.r=(v[0],v[1],float(v[2]),v[3],int(v[4])); w.destroy()
            except: messagebox.showerror("Error","Precio/Stock inválidos",parent=w)
        ttk.Button(w,text="✅ Guardar",command=guardar,style="Action.TButton").pack(pady=15)
        w.wait_window()

class _DlgCli:
    def __init__(self,parent):
        self.r=None; w=tk.Toplevel(parent); w.title("Agregar Cliente"); w.geometry("400x280"); w.configure(bg=BG); w.grab_set()
        self.entries=[]
        for campo in ["Nombre:","Contacto:","Dirección:"]:
            tk.Label(w,text=campo,bg=BG,fg=FG,font=(FONT,10)).pack(anchor="w",padx=30,pady=(5,0))
            e=ttk.Entry(w,width=35); e.pack(padx=30); self.entries.append(e)
        def guardar():
            v=[e.get().strip() for e in self.entries]
            if not all(v): messagebox.showwarning("Aviso","Completa campos",parent=w); return
            self.r=tuple(v); w.destroy()
        ttk.Button(w,text="✅ Guardar",command=guardar,style="Action.TButton").pack(pady=15)
        w.wait_window()
