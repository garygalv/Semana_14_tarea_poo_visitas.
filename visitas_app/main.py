from servicios.visita_servicio import VisitaServicio
from ui.app_tkinter import AppTkinter

if __name__ == "__main__":
    # Inyección de dependencias (obligatorio)
    servicio = VisitaServicio()
    app = AppTkinter(servicio)
    app.root.mainloop()