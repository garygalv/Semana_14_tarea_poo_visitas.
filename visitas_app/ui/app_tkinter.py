import tkinter as tk
from tkinter import ttk, messagebox
from modelos.visitante import Visitante

class AppTkinter:
    """Capa UI - Interfaz gráfica (recibe el servicio por inyección de dependencias)"""
    
    def __init__(self, visita_servicio):
        self.servicio = visita_servicio
        self.root = tk.Tk()
        self.root.title("Sistema de Registro de Visitantes")
        self.root.geometry("950x650")
        self.root.resizable(False, False)
        
        self.crear_formulario()
        self.crear_tabla()
        self.actualizar_tabla()          # carga inicial
        
    def crear_formulario(self):
        form = tk.LabelFrame(self.root, text="Nuevo Visitante", padx=15, pady=15)
        form.pack(pady=15, padx=20, fill="x")
        
        tk.Label(form, text="Cédula:").grid(row=0, column=0, sticky="w", pady=5)
        self.cedula_entry = tk.Entry(form, width=25, font=("Arial", 12))
        self.cedula_entry.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(form, text="Nombre Completo:").grid(row=1, column=0, sticky="w", pady=5)
        self.nombre_entry = tk.Entry(form, width=50, font=("Arial", 12))
        self.nombre_entry.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(form, text="Motivo de la visita:").grid(row=2, column=0, sticky="w", pady=5)
        self.motivo_entry = tk.Entry(form, width=50, font=("Arial", 12))
        self.motivo_entry.grid(row=2, column=1, pady=5, padx=10)
        
        # Botones
        btn_frame = tk.Frame(form)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        tk.Button(btn_frame, text="Registrar", width=15, bg="#28a745", fg="white",
                  font=("Arial", 10, "bold"), command=self.registrar).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Eliminar Seleccionado", width=18, bg="#dc3545", fg="white",
                  font=("Arial", 10, "bold"), command=self.eliminar).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Limpiar Campos", width=15, bg="#6c757d", fg="white",
                  font=("Arial", 10, "bold"), command=self.limpiar_campos).pack(side="left", padx=8)
    
    def crear_tabla(self):
        table_frame = tk.LabelFrame(self.root, text="Visitantes Registrados", padx=10, pady=10)
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.tree = ttk.Treeview(table_frame, columns=("cedula", "nombre", "motivo"),
                                 show="headings", height=15)
        
        self.tree.heading("cedula", text="Cédula")
        self.tree.heading("nombre", text="Nombre Completo")
        self.tree.heading("motivo", text="Motivo de la Visita")
        
        self.tree.column("cedula", width=140, anchor="center")
        self.tree.column("nombre", width=320)
        self.tree.column("motivo", width=420)
        
        self.tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.bind("<Double-1>", lambda e: self.limpiar_campos())  # doble clic limpia
    
    def registrar(self):
        cedula = self.cedula_entry.get().strip()
        nombre = self.nombre_entry.get().strip()
        motivo = self.motivo_entry.get().strip()
        
        if not cedula or not nombre or not motivo:
            messagebox.showwarning("Validación", "¡Todos los campos son obligatorios!")
            return
        
        try:
            visitante = Visitante(cedula, nombre, motivo)
            self.servicio.registrar(visitante)
            self.actualizar_tabla()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "✅ Visitante registrado correctamente")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def eliminar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Selección", "Seleccione un registro en la tabla")
            return
        
        cedula = self.tree.item(seleccion[0])["values"][0]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar visitante con cédula {cedula}?"):
            self.servicio.eliminar(cedula)
            self.actualizar_tabla()
            messagebox.showinfo("Éxito", "✅ Visitante eliminado")
    
    def limpiar_campos(self):
        self.cedula_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.motivo_entry.delete(0, tk.END)
    
    def actualizar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for v in self.servicio.obtener_todos():
            self.tree.insert("", "end", values=(v.cedula, v.nombre, v.motivo))