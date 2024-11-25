from datetime import datetime

class Client:
    def __init__(self, client_id, name, order, start_time, end_time, priority):
        self.client_id = client_id
        self.name = name
        self.order = order  # Diccionario {producto: cantidad}
        self.start_time = start_time  # Fecha y hora del pedido
        self.end_time = end_time  # Fecha y hora límite
        self.priority = priority  # Entre menor, mayor prioridad
        self.status = "active"  # Puede ser "active", "completed", o "cancelled"

    def cancel_order(self):
        """Cancela el pedido del cliente."""
        self.status = "cancelled"

    def is_active(self):
        """Verifica si el cliente tiene un pedido activo."""
        return self.status == "active"
