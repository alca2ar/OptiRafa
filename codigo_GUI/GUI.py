import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime, timedelta
from PIL import Image, ImageTk

from client_r import Client
from order_manager_r import OrderManager
from simulation_r import simulate_orders
from stage_r import Stage
from machine_r import Machine


# Cargar imágenes
def load_image(file):
    path = fr"D:\PirataCuliacan\Respaldo\img\{file}.png"
    return ImageTk.PhotoImage(Image.open(path))


# Clase principal de la GUI
class ProductionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Producción")
        self.current_time = datetime(2024, 11, 25)
        self.order_manager = OrderManager()
        self.machines = [
            Machine(1, 3, {"botellas_1": 600, "botellas_2": 500}),
            Machine(2, 3, {"sobres_1": 800, "sobres_2": 760}),
            Machine(3, 3, {"botellas_1": 900, "sobres_1": 925}),
        ]
        
        # Imágenes
        self.images = {
            "apagado": load_image("apagado"),
            "encendido": load_image("encendido"),
            "enojao": load_image("enojao"),
            "feliz": load_image("feliz"),
            "neutro": load_image("neutro"),
        }

        self.create_widgets()

    def create_widgets(self):
        # Menú de acciones
        frame_menu = tk.Frame(self.root, padx=10, pady=10)
        frame_menu.pack()

        tk.Label(frame_menu, text="Seleccione una acción:", font=("Arial", 12)).pack(pady=5)
        ttk.Button(frame_menu, text="Registrar cliente", command=self.register_client).pack(fill="x", pady=5)
        ttk.Button(frame_menu, text="Cancelar pedido", command=self.cancel_order).pack(fill="x", pady=5)
        ttk.Button(frame_menu, text="Simular producción", command=self.simulate_production).pack(fill="x", pady=5)
        ttk.Button(frame_menu, text="Estado de producción", command=self.show_status).pack(fill="x", pady=5)

    def register_client(self):
        def add_product():
            """Agrega el producto y la cantidad a la lista temporal."""
            product = product_var.get()
            try:
                quantity = int(entry_quantity.get())
                if quantity <= 0:
                    raise ValueError("La cantidad debe ser mayor a 0.")
                products_list.append({"product": product, "quantity": quantity})
                update_product_list()
            except ValueError:
                messagebox.showerror("Error", "Ingrese una cantidad válida.")

        def update_product_list():
            """Actualiza la visualización de la lista de productos."""
            listbox_products.delete(0, tk.END)  # Limpia la lista actual
            for idx, item in enumerate(products_list):
                listbox_products.insert(tk.END, f"{idx + 1}. {item['product']} - {item['quantity']} unidades")

        def submit():
            """Envía el pedido registrado."""
            name = entry_name.get()
            try:
                priority = int(entry_priority.get())
                end_time = datetime.strptime(entry_end_time.get(), "%Y-%m-%d, %H:%M")
            except ValueError:
                messagebox.showerror("Error", "Datos inválidos. Verifique prioridad o fecha.")
                return

            if not products_list:
                messagebox.showerror("Error", "Debe agregar al menos un producto al pedido.")
                return

            order = {item["product"]: item["quantity"] for item in products_list}
            self.order_manager.add_client(name, order, end_time, priority)
            messagebox.showinfo("Éxito", f"Pedido registrado para el cliente {name}.")
            window.destroy()

        # Ventana de registro de cliente
        window = tk.Toplevel(self.root)
        window.title("Registrar Cliente")

        tk.Label(window, text="Nombre del cliente:").pack()
        entry_name = tk.Entry(window)
        entry_name.pack()

        tk.Label(window, text="Producto:").pack()
        product_var = tk.StringVar(value="botellas_1")  # Valor predeterminado
        product_menu = ttk.Combobox(window, textvariable=product_var)
        product_menu['values'] = ["botellas_1", "botellas_2", "sobres_1", "sobres_2"]  # Opciones disponibles
        product_menu.pack()

        tk.Label(window, text="Cantidad:").pack()
        entry_quantity = tk.Entry(window)
        entry_quantity.pack()

        ttk.Button(window, text="Agregar Producto", command=add_product).pack(pady=5)

        # Lista de productos agregados
        tk.Label(window, text="Productos agregados:").pack()
        listbox_products = tk.Listbox(window, height=5, width=50)
        listbox_products.pack(pady=5)

        # Prioridad y fecha de entrega
        tk.Label(window, text="Prioridad:").pack()
        entry_priority = tk.Entry(window)
        entry_priority.pack()

        tk.Label(window, text="Fecha y hora de entrega (YYYY-MM-DD, HH:MM):").pack()
        entry_end_time = tk.Entry(window)
        entry_end_time.pack()

        # Botón de registro
        ttk.Button(window, text="Registrar Pedido", command=submit).pack(pady=10)

        # Inicializa la lista de productos
        products_list = []

    def cancel_order(self):
        def submit():
            client_id = int(entry_id.get())
            if 0 <= client_id < len(self.order_manager.orders):
                del self.order_manager.orders[client_id]
                messagebox.showinfo("Éxito", "Pedido cancelado.")
            else:
                messagebox.showerror("Error", "ID inválido.")
            window.destroy()

        window = tk.Toplevel(self.root)
        window.title("Cancelar Pedido")

        tk.Label(window, text="ID del cliente para cancelar el pedido:").pack()
        entry_id = tk.Entry(window)
        entry_id.pack()

        ttk.Button(window, text="Cancelar Pedido", command=submit).pack(pady=10)

    def simulate_production(self):
        def submit():
            try:
                simulate_until = datetime.strptime(entry_end_time.get(), "%Y-%m-%d, %H:%M")
                total_hours = int((simulate_until - self.current_time).total_seconds() / 3600)
                produced = simulate_orders(self.order_manager, Stage(3, self.machines), total_hours)

                # Muestra los resultados
                result_text = ""
                for cliente, productos in produced:  # Ajustado para trabajar con tuplas
                    if isinstance(productos, dict):  # Verifica si productos es un diccionario
                        for product, quantity in productos.items():
                            result_text += f"Cliente: {cliente}, Producto: {product}, Cantidad Producida: {quantity}\n"
                    else:
                        result_text += f"Cliente: {cliente}, Productos: {productos} (estructura inesperada)\n"

                messagebox.showinfo("Resultados de Simulación", result_text if result_text else "No se completó ninguna producción.")
                window.destroy()
            except ValueError as e:
                messagebox.showerror("Error", f"Entrada inválida: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}")

        window = tk.Toplevel(self.root)
        window.title("Simular Producción")

        tk.Label(window, text="Fecha y hora de finalización de la simulación (YYYY-MM-DD, HH:MM):").pack()
        entry_end_time = tk.Entry(window)
        entry_end_time.pack()

        ttk.Button(window, text="Simular", command=submit).pack(pady=10)


    def show_status(self):
        window = tk.Toplevel(self.root)
        window.title("Estado de Producción")

        tk.Label(window, text="Estado de las máquinas:", font=("Arial", 12)).pack(pady=5)
        for machine in self.machines:
            frame_machine = tk.Frame(window, pady=5)
            frame_machine.pack()
            tk.Label(frame_machine, text=f"Máquina {machine.id}:").pack(side="left")
            tk.Label(frame_machine, text=machine.status.capitalize(), fg="green" if machine.status == "encendido" else "red").pack(side="left")

        orders_status = self.order_manager.get_production_status(self.machines, self.current_time)
        tk.Label(window, text="Estado de los pedidos:", font=("Arial", 12)).pack(pady=5)
        for order in orders_status["orders"]:
            tk.Label(window, text=f"Cliente: {order['cliente']}, Estado: {order['estado']}").pack()


# Crear y ejecutar la aplicación
root = tk.Tk()
app = ProductionGUI(root)
root.mainloop()
