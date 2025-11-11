import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector

# -----------------------
# CONFIGURACIÓN MySQL
# -----------------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',  # Cambia por tu contraseña real
    'database': 'qa_system'
}
conn = mysql.connector.connect(**DB_CONFIG)
cur = conn.cursor()
cur.execute("""CREATE DATABASE qa_system;""")
+
# -----------------------
# CLASE DE EVALUACIONES
# -----------------------
class Evaluations:
    def __init__(self):
        self.total = 0

    def _conn(self):
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Evaluations (
                TM_evaluated VARCHAR(12) NOT NULL,
                solutioning INT,
                policies INT,
                documentation INT,
                satisfaction INT,
                callid VARCHAR(20) NOT NULL,
                addfeedback VARCHAR(200),
                total REAL
            );
        """)
        conn.commit()
        cur.close()
        return conn

    def Evaluate(self, solutioning, policies, documentation, satisfaction, racfid, callid, addfeedback):
        """Guarda la evaluación y recalcula el promedio del TM."""
        self.total = solutioning + policies + documentation + satisfaction
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO Evaluations (TM_evaluated, solutioning, policies, documentation, satisfaction, callid, addfeedback, total) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (racfid, solutioning, policies, documentation, satisfaction, callid, addfeedback, self.total)
            )
            conn.commit()

            # Calcular promedio de todas las evaluaciones del TM
            cur.execute("SELECT AVG(total) FROM Evaluations WHERE TM_evaluated=%s", (racfid,))
            avg = cur.fetchone()[0] or 0

            # Actualizar promedio del TM
            cur.execute("UPDATE TMs SET promedio=%s WHERE RACFID=%s", (avg, racfid))
            conn.commit()
            cur.close()

# -----------------------
# LOGIN PRINCIPAL
# -----------------------
class LoginApp:
    def __init__(self):
        self.COLOR_FONDO = "mint cream"
        self.COLOR_TEXTO = "medium orchid"
        self.COLOR_TITULO = "dark violet"
        self.COLOR_BOTON = "pale green"
        self.FONT_TITULO = ("Goudy Old Style", 24, "bold")
        self.FONT_SUBTITULO = ("Goudy Old Style", 12, "bold")

        self.ventana = tk.Tk()
        self.ventana.title("Login - QA Checkup System")
        self.ventana.geometry("520x320")
        self.ventana.config(bg=self.COLOR_FONDO)

        self.crear_tablas_y_usuarios()
        self.crear_interfaz_login()
        self.ventana.mainloop()

    def crear_tablas_y_usuarios(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS Staff(
                    RACFID VARCHAR(12) PRIMARY KEY,
                    nombre VARCHAR(50),
                    Boss VARCHAR(12),
                    Position VARCHAR(50),
                    password VARCHAR(50),
                    promedio INT DEFAULT 0
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS TMs(
                    RACFID VARCHAR(12) PRIMARY KEY,
                    nombre VARCHAR(50),
                    Boss VARCHAR(12),
                    password VARCHAR(50),
                    promedio INT DEFAULT 0
                );
            """)

            # Usuarios por defecto
            cur.execute(
                "INSERT IGNORE INTO Staff (RACFID, nombre, Boss, Position, password, promedio) VALUES "
                "(%s,%s,%s,%s,%s,%s)",
                ('BIGBOSS', 'Big Boss', 'None', 'Big Boss', 'admin123', 100)
            )
            cur.execute(
                "INSERT IGNORE INTO Staff (RACFID, nombre, Boss, Position, password, promedio) VALUES "
                "(%s,%s,%s,%s,%s,%s)",
                ('CEA001', 'Carlos EA', 'BIGBOSS', 'CEA', 'cea123', 90)
            )
            cur.execute(
                "INSERT IGNORE INTO Staff (RACFID, nombre, Boss, Position, password, promedio) VALUES "
                "(%s,%s,%s,%s,%s,%s)",
                ('TL001', 'Laura TL', 'CEA001', 'TL', 'tl123', 85)
            )
            cur.execute(
                "INSERT IGNORE INTO TMs (RACFID, nombre, Boss, password, promedio) VALUES "
                "(%s,%s,%s,%s,%s)",
                ('TMTEST', 'Test TM', 'TL001', 'tm123', 80)
            )

            conn.commit()
            cur.close()
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Error DB", f"No se pudieron crear tablas o usuarios:\n{e}")

    def crear_interfaz_login(self):
        tk.Label(self.ventana, text="Bienvenido", font=self.FONT_TITULO,
                 bg=self.COLOR_FONDO, fg=self.COLOR_TITULO).pack(pady=10)
        tk.Label(self.ventana, text="Ingrese su RACFID y contraseña", font=self.FONT_SUBTITULO,
                 bg=self.COLOR_FONDO, fg=self.COLOR_TEXTO).pack(pady=5)

        frame = tk.Frame(self.ventana, bg=self.COLOR_FONDO)
        frame.pack(pady=20)
        tk.Label(frame, text="RACFID:", font=self.FONT_SUBTITULO, bg=self.COLOR_FONDO).grid(row=0, column=0, padx=10)
        self.entry_usuario = tk.Entry(frame, width=30)
        self.entry_usuario.grid(row=0, column=1)
        tk.Label(frame, text="Contraseña:", font=self.FONT_SUBTITULO, bg=self.COLOR_FONDO).grid(row=1, column=0)
        self.entry_contrasena = tk.Entry(frame, width=30, show="*")
        self.entry_contrasena.grid(row=1, column=1)
        tk.Button(self.ventana, text="Iniciar Sesión", bg=self.COLOR_BOTON,
                  command=self.verificar_login).pack(pady=15)

    def verificar_login(self):
        racfid = self.entry_usuario.get().strip()
        password = self.entry_contrasena.get().strip()
        if not racfid or not password:
            messagebox.showwarning("Atención", "Ingrese usuario y contraseña.")
            return

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM Staff WHERE RACFID=%s AND password=%s", (racfid, password))
            usuario = cur.fetchone()
            tipo = "Staff"
            if not usuario:
                cur.execute("SELECT * FROM TMs WHERE RACFID=%s AND password=%s", (racfid, password))
                usuario = cur.fetchone()
                tipo = "TM" if usuario else None
            cur.close()
            conn.close()

            if usuario:
                self.ventana.destroy()
                WelcomeScreen(usuario['nombre'], usuario.get('Boss', ''), usuario.get('Position', ''), tipo, racfid)
            else:
                messagebox.showerror("Error", "Credenciales incorrectas.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error DB", str(e))

# -----------------------
# PANTALLA PRINCIPAL
# -----------------------
class WelcomeScreen:
    def __init__(self, nombre, boss, position, tipo, racfid):
        self.nombre = nombre
        self.boss = boss
        self.position = position
        self.tipo = tipo
        self.racfid = racfid
        self.COLOR_FONDO = "mint cream"
        self.COLOR_TEXTO = "dark violet"

        self.root = tk.Tk()
        self.root.title(f"Bienvenido - {nombre}")
        self.root.geometry("700x450")
        self.root.config(bg=self.COLOR_FONDO)

        self.crear_menu_barra()

        centro = tk.Frame(self.root, bg=self.COLOR_FONDO)
        centro.pack(expand=True)
        tk.Label(centro, text=f"Bienvenido, {nombre}\nTu jefe directo: {boss}",
                 font=("Goudy Old Style", 20, "bold"), bg=self.COLOR_FONDO, fg=self.COLOR_TEXTO).pack(pady=20)
        tk.Button(self.root, text="Cerrar Sesión", bg="green", fg="white",
                  font=("Arial", 12, "bold"), command=self.root.destroy).pack(side="bottom", pady=20)
        self.root.mainloop()

    def crear_menu_barra(self):
        barra = tk.Frame(self.root, bg="light green", height=40)
        barra.pack(fill="x", side="top")

        if self.position == "Big Boss":
            tk.Button(barra, text="Manejo de Personal", bg="white", command=self.manejo_personal_bigboss).pack(side="left", padx=5)
            tk.Button(barra, text="Realizar Evaluación", bg="white", command=self.realizar_evaluacion).pack(side="left", padx=5)
        elif self.position in ["CEA", "TL"]:
            tk.Button(barra, text="Manejo de TMs", bg="white", command=self.manejo_tms_cea_tl).pack(side="left", padx=5)
            if self.position == "CEA":
                tk.Button(barra, text="Realizar Evaluación", bg="white", command=self.realizar_evaluacion).pack(side="left", padx=5)
        elif self.tipo == "TM":
            tk.Button(barra, text="Mis Evaluaciones", bg="white", command=self.ver_evaluaciones).pack(side="left", padx=5)

    # -------------------- BIG BOSS --------------------
    def manejo_personal_bigboss(self):
        win = tk.Toplevel(self.root)
        win.title("Manejo de Personal - Big Boss")
        win.geometry("500x500")

        tk.Label(win, text="Agregar nuevo miembro", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(win, text="Tipo (Staff/TM):").pack()
        tipo = tk.Entry(win)
        tipo.pack()
        tk.Label(win, text="RACFID:").pack()
        racfid = tk.Entry(win)
        racfid.pack()
        tk.Label(win, text="Nombre:").pack()
        nombre = tk.Entry(win)
        nombre.pack()
        tk.Label(win, text="RACFID del jefe (Boss):").pack()
        boss = tk.Entry(win)
        boss.pack()
        tk.Label(win, text="Contraseña:").pack()
        password = tk.Entry(win, show="*")
        password.pack()
        tk.Label(win, text="Posición (solo Staff):").pack()
        position = tk.Entry(win)
        position.pack()

        def guardar():
            tipo_val = tipo.get().strip().upper()
            r, n, b, p, pos = racfid.get().strip(), nombre.get().strip(), boss.get().strip(), password.get().strip(), position.get().strip()
            if not r or not n or not p:
                messagebox.showwarning("Campos Vacíos", "Todos los campos obligatorios deben llenarse.")
                return
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cur = conn.cursor()
                if tipo_val == "STAFF":
                    cur.execute(
                        "INSERT IGNORE INTO Staff (RACFID, nombre, Boss, Position, password) VALUES (%s,%s,%s,%s,%s)",
                        (r, n, b or None, pos or None, p)
                    )
                else:
                    cur.execute(
                        "INSERT IGNORE INTO TMs (RACFID, nombre, Boss, password) VALUES (%s,%s,%s,%s)",
                        (r, n, b or None, p)
                    )
                conn.commit()
                cur.close()
                conn.close()
                messagebox.showinfo("Éxito", "Personal agregado correctamente.")
                win.destroy()
            except mysql.connector.Error as e:
                messagebox.showerror("Error DB", str(e))

        def eliminar():
            racf1 = simpledialog.askstring("Eliminar", "Ingrese el RACFID:")
            racf2 = simpledialog.askstring("Confirmar", "Ingrese nuevamente el RACFID:")
            if racf1 == racf2:
                try:
                    conn = mysql.connector.connect(**DB_CONFIG)
                    cur = conn.cursor()
                    cur.execute("DELETE FROM Evaluations WHERE TM_evaluated=%s", (racf1,))
                    cur.execute("DELETE FROM Staff WHERE RACFID=%s", (racf1,))
                    cur.execute("DELETE FROM TMs WHERE RACFID=%s", (racf1,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    messagebox.showinfo("Eliminado", f"Usuario {racf1} eliminado.")
                except mysql.connector.Error as e:
                    messagebox.showerror("Error DB", str(e))

        tk.Button(win, text="Guardar", bg="pale green", command=guardar).pack(pady=10)
        tk.Button(win, text="Eliminar Usuario", bg="light coral", command=eliminar).pack(pady=10)

    # -------------------- CEA / TL --------------------
    def manejo_tms_cea_tl(self):
        win = tk.Toplevel(self.root)
        win.title("Manejo de TMs (CEA/TL)")
        win.geometry("480x480")

        tk.Label(win, text="Agregar nuevo TM", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(win, text="RACFID del TM:").pack()
        racfid = tk.Entry(win)
        racfid.pack()
        tk.Label(win, text="Nombre:").pack()
        nombre = tk.Entry(win)
        nombre.pack()
        tk.Label(win, text="RACFID del CEA:").pack()
        cea = tk.Entry(win)
        cea.pack()
        tk.Label(win, text="RACFID del TL:").pack()
        tl = tk.Entry(win)
        tl.pack()
        tk.Label(win, text="Contraseña:").pack()
        password = tk.Entry(win, show="*")
        password.pack()

        if self.position == "CEA":
            cea.insert(0, self.racfid)
            cea.config(state="disabled")
        elif self.position == "TL":
            tl.insert(0, self.racfid)
            tl.config(state="disabled")

        def guardar():
            r, n, c, t, p = racfid.get().strip(), nombre.get().strip(), cea.get().strip(), tl.get().strip(), password.get().strip()
            if not r or not n or not p or not (c or t):
                messagebox.showwarning("Campos Vacíos", "Todos los campos son obligatorios.")
                return
            boss_value = t if t else c
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cur = conn.cursor()
                cur.execute("INSERT IGNORE INTO TMs (RACFID, nombre, Boss, password) VALUES (%s,%s,%s,%s)",
                            (r, n, boss_value, p))
                conn.commit()
                cur.close()
                conn.close()
                messagebox.showinfo("Éxito", "TM agregado correctamente.")
                win.destroy()
            except mysql.connector.Error as e:
                messagebox.showerror("Error DB", str(e))

        def eliminar():
            racf1 = simpledialog.askstring("Eliminar TM", "Ingrese el RACFID del TM:")
            racf2 = simpledialog.askstring("Confirmar", "Ingrese nuevamente el RACFID:")
            if racf1 == racf2:
                try:
                    conn = mysql.connector.connect(**DB_CONFIG)
                    cur = conn.cursor()
                    cur.execute("DELETE FROM Evaluations WHERE TM_evaluated=%s", (racf1,))
                    cur.execute("DELETE FROM TMs WHERE RACFID=%s", (racf1,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    messagebox.showinfo("Eliminado", f"TM {racf1} eliminado correctamente.")
                except mysql.connector.Error as e:
                    messagebox.showerror("Error DB", str(e))

        tk.Button(win, text="Guardar TM", bg="pale green", command=guardar).pack(pady=10)
        tk.Button(win, text="Eliminar TM", bg="light coral", command=eliminar).pack(pady=10)

    # -------------------- EVALUAR --------------------
    def realizar_evaluacion(self):
        win = tk.Toplevel(self.root)
        win.title("Realizar Evaluación")
        win.geometry("500x450")

        tk.Label(win, text="RACFID del TM a evaluar:").pack()
        racfid_entry = tk.Entry(win)
        racfid_entry.pack()

        valores = {k: tk.IntVar() for k in ["solutioning", "policies", "documentation", "satisfaction"]}
        total_label = tk.Label(win, text="Total: 0", font=("Arial", 14, "bold"))
        total_label.pack(pady=10)

        def actualizar_total():
            total = sum(v.get() * 25 for v in valores.values())
            total_label.config(text=f"Total: {total}")

        for c in valores:
            tk.Checkbutton(win, text=c.capitalize(), variable=valores[c],
                           onvalue=1, offvalue=0, command=actualizar_total).pack(anchor="w", padx=20)

        tk.Label(win, text="Call ID:").pack()
        callid_entry = tk.Entry(win)
        callid_entry.pack()
        tk.Label(win, text="Feedback adicional:").pack()
        feedback_entry = tk.Entry(win, width=50)
        feedback_entry.pack()

        def guardar_eval():
            racfid = racfid_entry.get().strip()
            callid = callid_entry.get().strip()
            fb = feedback_entry.get().strip()
            if not racfid or not callid:
                messagebox.showwarning("Campos Vacíos", "Debe ingresar el RACFID y Call ID.")
                return
            try:
                ev = Evaluations()
                ev.Evaluate(valores["solutioning"].get() * 25,
                            valores["policies"].get() * 25,
                            valores["documentation"].get() * 25,
                            valores["satisfaction"].get() * 25,
                            racfid, callid, fb)
                messagebox.showinfo("Éxito", f"Evaluación guardada correctamente.\nPromedio actualizado para {racfid}.")
                win.destroy()
            except mysql.connector.Error as e:
                messagebox.showerror("Error DB", str(e))

        tk.Button(win, text="Guardar Evaluación", bg="pale green", command=guardar_eval).pack(pady=15)

    def ver_evaluaciones(self):
        win = tk.Toplevel(self.root)
        win.title("Mis Evaluaciones")
        win.geometry("400x400")
        tk.Label(win, text=f"Evaluaciones de {self.nombre}", font=("Arial", 14, "bold")).pack(pady=10)
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute("SELECT callid, total FROM Evaluations WHERE TM_evaluated=%s", (self.racfid,))
            data = cur.fetchall()
            if not data:
                tk.Label(win, text="No hay evaluaciones registradas.").pack()
            else:
                for callid, total in data:
                    tk.Label(win, text=f"Call: {callid} - Total: {total}").pack(anchor="w", padx=20)
            cur.close()
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Error DB", str(e))

# -----------------------
# EJECUCIÓN PRINCIPAL
# -----------------------
if __name__ == "__main__":
    LoginApp()
