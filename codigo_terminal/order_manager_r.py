from datetime import datetime, timedelta
from client_r import Client


class OrderManager:
    def __init__(self):
        self.clients = []  # Lista de objetos Client
        self.client_counter = 0  # Para generar IDs únicos

    def add_client(self, name, order, end_time, priority):
        """Registra un nuevo cliente y su pedido."""
        self.client_counter += 1
        client_id = self.client_counter
        start_time = datetime.now()
        new_client = Client(client_id, name, order, start_time, end_time, priority)
        self.clients.append(new_client)

    def cancel_client_order(self, client_id):
        """Cancela el pedido de un cliente específico."""
        for client in self.clients:
            if client.client_id == client_id:
                client.cancel_order()
                print(f"Pedido del cliente '{client.name}' cancelado.")
                return
        print(f"No se encontró el cliente con ID {client_id}.")

    def get_active_orders(self):
        """Obtiene los pedidos activos, ordenados por prioridad."""
        return sorted([c for c in self.clients if c.is_active()], key=lambda x: x.priority)
    

    def get_production_status(self, machines, current_time):
        """Verifica el estado actual de las máquinas y el progreso de los pedidos."""
        status = {"machines": {}, "orders": []}
        
        # Estado de las máquinas
        for machine in machines:
            status["machines"][machine.id] = {
                "estado": machine.state,
                "producto_actual": machine.current_product,
                "tiempo_restante": machine.remaining_time,  # Corrección aquí
            }

        # Progreso de los pedidos
        for client in self.clients:
            if client.is_active():
                orders_fulfilled = all(
                    quantity <= 0 for quantity in client.order.values()
                )
                status["orders"].append({
                    "cliente": client.name,
                    "prioridad": client.priority,
                    "estado": "completado" if orders_fulfilled else "pendiente",
                    "productos_pendientes": client.order if not orders_fulfilled else {}
                })
        
        return status
