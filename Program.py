import tkinter as tk

class Evaluations:
    def __init__(self, solutioning, policies, documentation, satisfaction, callid, addfeedback, total):
        self.solutioning = solutioning
        self.policies = policies
        self.documentation = documentation
        self.satisfaction = satisfaction
        self.callid = callid
        self.addfeedback = addfeedback
        self.total = total

        def _conn():
            conn = sqlite3.connect(DB_NAME)
            conn.row_factory = sqlite3.Row
            conn.execute("""
                   CREATE TABLE IF NOT EXISTS Evaluations (
                       TM_evaluated VARCHAR(12) NOT NULL,
                       solutioing INT CHECK (solutioing <=25),
                       policies INT CHECK (solutioing <=25),
                       documentation INT CHECK (solutioing <=25),
                       satisfaction INT CHECK (solutioing <=25),
                       callid varchar(20) NOT NULL,
                       addfeedback varchar(200) NOT NULL,
                       total REAL
                   );
               """)
            conn.commit()
            return conn

    def Evaluate(self, solutioning, policies, documentation, satisfaction, racfid, callid, addfeedback):
        self.total = solutioning + policies + documentation + satisfaction
        self.addfeedback = addfeedback

        with self._conn() as conn:
            conn.execute(
                "INSERT INTO Evaluations (TM_evaluated,solutioning,policies,documentation,satisfaction,callid,addfeedback,total) VALUES (?, ?, ?,?,?,?,?,?)",
                (self.racfid, self.solutioning, self.policies, self.documentation, self.satisfaction, self.callid,
                 self.addfeedback, self.total)
            )
            print(f"Evaluacion guardada: {self.callid}")


class QA:
    def __init__(self,TM_evaluated, avg, evalsdone,eval1,eval2,eval3,eval4,eval5,eval6,eval7,eval8,totval):
        self.Evalsdone = evalsdone
        self.AVG = avg

        def _conn():
            conn = sqlite3.connect(DB_NAME)
            conn.row_factory = sqlite3.Row
            conn.execute("""
                        CREATE TABLE IF NOT EXISTS Evaluations (
                            TM_evaluated VARCHAR(12) NOT NULL,
                            avg REAL CHECK (solutioing <=110),
                            eval1 varchar(200) NOT NULL,
                            eval2 varchar(200) NOT NULL,
                            eval3 varchar(200) NOT NULL,
                            eval4 varchar(200) NOT NULL,
                            eval5 varchar(200) NOT NULL,
                            eval6 varchar(200) NOT NULL,
                            eval7 varchar(200) NOT NULL,
                            eval8 varchar(200) NOT NULL,
                            evalsdone INT DEFAULT 0,
                            totval REAL 
                        );
                    """)
            conn.commit()
            return conn

    def CalcAvg(self):
        with QA._conn() as conn:
            cur = conn.execute("
            prom = cur.fetchone()["prom"]

        return self.AVG

    def CalcTotscore(self):
        return self.TotScore


class TM:
    def __init__(self, racfid, boss, evaluator, name):
        self.name = name
        self.RACFID = racfid
        self.Boss = boss
        self.Evaluator = evaluator

        def _conn():
            conn = sqlite3.connect(DB_NAME)
            conn.row_factory = sqlite3.Row
            conn.execute("""
                CREATE TABLE IF NOT EXISTS TMs (
                    RACFID VARCHAR(12) PRIMARY KEY,
                    nombre VARCHAR(50) NOT NULL,
                    Boss VARCHAR(12) NOT NULL,

                    promedio REAL
                );
            """)
            conn.commit()
            return conn

    def ShowInfo(self):
        print(f"RACFID: {self.RACFID}")
        print(f"Email: {self.Email}")
        print(f"Boss: {self.Boss}")
        print(f"Evaluator: {self.Evaluator}")
        print(f"QA: {self.QA}")


class Sups(TM):
    def __init__(self, racfid, email, boss, evaluator, position):
        super().__init__(racfid, email, boss, evaluator, position)


def _conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("""
                CREATE TABLE IF NOT EXISTS Staff (
                    RACFID VARCHAR(12) PRIMARY KEY,
                    nombre VARCHAR(50) NOT NULL,
                    Email  VARCHAR(50) NOT NULL,
                    Boss VARCHAR(12) NOT NULL,
	        Position VARCHAR 
                    promedio REAL
                );
            """)
    conn.commit()
    return conn


class CEA(TM):
    def __init__(self, racfid, email, boss, evaluator, team, Position):
        super().__init__(racfid, email, boss, evaluator)
        self.Team = team


def _conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("""
                CREATE TABLE IF NOT EXISTS Staff(
                    RACFID VARCHAR(12) PRIMARY KEY,
                    nombre VARCHAR(50) NOT NULL,
                    Email  VARCHAR(50) NOT NULL,
                    Boss VARCHAR(12) NOT NULL,
        Position VARCHAR(12) NOT NULL,
                    promedio REAL
                );
            """)
    conn.commit()
    return conn


class BIG_BOSS(TM):
    def __init__(self, racfid, email, boss, evaluator, qa, team):
        super().__init__(racfid, email, boss, evaluator, qa)
        self.Team = team


def _conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("""
                CREATE TABLE IF NOT EXISTS BIGBOSS(
                    RACFID VARCHAR(12) PRIMARY KEY,
                    nombre VARCHAR(50) NOT NULL,
                    Email  VARCHAR(50) NOT NULL,
                    Boss VARCHAR(12) NOT NULL,
                    promedio REAL
                );
            """)
    conn.commit()
    return conn


class Add:
    def AddTM(self, racfid, boss, evaluator, qa, name):
        with self._conn() as conn:

            conn.execute(
            "INSERT INTO TMs (self, racfid, boss,name,position) VALUES ( ?,?,?,?)",
            (self, racfid , boss, name, position)
            )

    def AddStaff(self, racfid, , boss, name, position):
         with self._conn() as conn:

            conn.execute(
                    "INSERT INTO Staff(self, racfid, boss,name,position) VALUES ( ?,?,?,?,?)",
                    (self, racfid , boss, name, position)
                )


class Erase:
    ide = input("Ingrese racif del trabajador a eliminar: ")
    with Erase._conn() as conn:
        cur = conn.execute("DELETE FROM TMs WHERE RACFID= ?", (ide))


def EraseStaff(self, team, staff):
    ide = input("Ingrese racif del trabajador a eliminar: ")


with Erase._conn() as conn:
    cur = conn.execute("DELETE FROM Staff WHERE RACFID= ?", (ide,))




class LoginApp:
    def __init__(self):
        self.COLOR_FONDO = "mint cream"
        self.COLOR_TEXTO = "medium orchid"
        self.COLOR_ESCRIBIR = "lime green"
        self.COLOR_TITULO = "dark violet"
        self.COLOR_BOTON = "pale green"
        self.FONT_TITULO = ("Goudy Old Style", 32, "bold")
        self.FONT_SUBTITULO = ("Goudy Old Style", 18, "bold")
        self.FONT_TEXTO = ("Stencil Std", 11, "bold")

        self.ventana = tk.Tk()
        self.ventana.title("Login - QA checkup system")
        self.ventana.geometry("550x350")
        self.ventana.config(bg=self.COLOR_FONDO)

        self.crear_interfaz()
        self.ventana.mainloop()

    def crear_interfaz(self):
        tk.Label(
            self.ventana,
            text="Bienvenido",
            font=self.FONT_TITULO,
            bg=self.COLOR_FONDO,
            fg=self.COLOR_TITULO
        ).pack(pady=15)

        tk.Label(
            self.ventana,
            text="Inicie sesión utilizando su RACFID y su Password",
            font=self.FONT_SUBTITULO,
            bg=self.COLOR_FONDO,
            fg=self.COLOR_TEXTO,
            wraplength=750,
            justify="center"
        ).pack(pady=10)

        frame = tk.Frame(self.ventana, bg=self.COLOR_FONDO)
        frame.pack(pady=20)

        tk.Label(frame, text="RACFID:", font=self.FONT_SUBTITULO, bg=self.COLOR_FONDO, fg=self.COLOR_ESCRIBIR) \
            .grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_usuario = tk.Entry(frame, width=30, font=("Arial", 14))
        self.entry_usuario.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(frame, text="Contraseña:", font=self.FONT_SUBTITULO, bg=self.COLOR_FONDO, fg=self.COLOR_ESCRIBIR) \
            .grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_contrasena = tk.Entry(frame, width=30, show="*", font=("Arial", 14))
        self.entry_contrasena.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(
            self.ventana,
            text="Iniciar Sesión",
            font=("Goudy Old Style", 14, "bold"),
            bg=self.COLOR_BOTON,
            fg="black",
            width=20,
            command=self.verificar_login
        ).pack(pady=20)

    def verificar_login(self):
        self.ventana.destroy()
        WelcomeScreen("Texto Aqui")


class WelcomeScreen:
    def __init__(self, usuario):
        self.COLOR_FONDO = "mint cream"
        self.COLOR_TEXTO = "medium orchid"
        self.COLOR_TITULO = "dark violet"
        self.COLOR_BOTON = "pale green"
        self.FONT_TITULO = ("Goudy Old Style", 32, "bold")
        self.FONT_SUBTITULO = ("Goudy Old Style", 18, "bold")

        self.ventana = tk.Tk()
        self.ventana.title("Bienvenido - QA checkup system")
        self.ventana.geometry("600x400")
        self.ventana.config(bg=self.COLOR_FONDO)

        self.crear_barra_superior()

        tk.Label(
            self.ventana,
            text=f"¡Bienvenido, {usuario}!",
            font=self.FONT_TITULO,
            bg=self.COLOR_FONDO,
            fg=self.COLOR_TITULO
        ).pack(pady=40)

        tk.Label(
            self.ventana,
            text="Has iniciado sesión correctamente.\nSelecciona una opción para continuar.",
            font=self.FONT_SUBTITULO,
            bg=self.COLOR_FONDO,
            fg=self.COLOR_TEXTO,
            justify="center"
        ).pack(pady=20)

        tk.Button(
            self.ventana,
            text="Cerrar sesión",
            font=("Goudy Old Style", 14, "bold"),
            bg=self.COLOR_BOTON,
            fg="black",
            width=20,
            command=self.ventana.destroy
        ).pack(pady=20)

        self.ventana.mainloop()

    def crear_barra_superior(self):
        barra = tk.Frame(self.ventana, bg=self.COLOR_BOTON, height=40)
        barra.pack(fill="x", side="top")

        tk.Button(
            barra,
            text="Menú principal",
            bg=self.COLOR_BOTON,
            fg="black",
            font=("Goudy Old Style", 12, "bold"),
            bd=0,
            relief="flat",
            activebackground="medium sea green",
            activeforeground="white",
            command=lambda: self.mostrar_mensaje("Menú principal presionado")
        ).pack(side="left", padx=10, pady=5)

        tk.Button(
            barra,
            text="Submenú 1",
            bg=self.COLOR_BOTON,
            fg="black",
            font=("Goudy Old Style", 12, "bold"),
            bd=0,
            relief="flat",
            activebackground="medium sea green",
            activeforeground="white",
            command=lambda: self.mostrar_mensaje("Submenú 1 presionado")
        ).pack(side="left", padx=10, pady=5)

        tk.Button(
            barra,
            text="+ Agregar Submenú",
            bg="medium orchid",
            fg="white",
            font=("Goudy Old Style", 12, "bold"),
            bd=0,
            relief="flat",
            activebackground="dark violet",
            activeforeground="white",
            command=self.agregar_submenu
        ).pack(side="right", padx=10, pady=5)

    def agregar_submenu(self):
        nuevo = tk.Button(
            self.ventana.children['!frame'],
            text=f"Submenú {len(self.ventana.children['!frame'].winfo_children()) - 1}",
            bg=self.COLOR_BOTON,
            fg="black",
            font=("Goudy Old Style", 12, "bold"),
            bd=0,
            relief="flat",
            activebackground="medium sea green",
            activeforeground="white",
            command=lambda: self.mostrar_mensaje("Nuevo submenú presionado")
        )
        nuevo.pack(side="left", padx=10, pady=5)

    def mostrar_mensaje(self, texto):
        popup = tk.Toplevel(self.ventana)
        popup.title("Acción")
        popup.geometry("300x150")
        popup.config(bg=self.COLOR_FONDO)

        tk.Label(
            popup,
            text=texto,
            font=self.FONT_SUBTITULO,
            fg=self.COLOR_TEXTO,
            bg=self.COLOR_FONDO,
            wraplength=280,
            justify="center"
        ).pack(pady=30)

        tk.Button(
            popup,
            text="Cerrar",
            font=("Goudy Old Style", 12, "bold"),
            bg=self.COLOR_BOTON,
            fg="black",
            command=popup.destroy
        ).pack(pady=10)


if __name__ == "__main__":
    LoginApp()

