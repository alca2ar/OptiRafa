from datetime import datetime, timedelta
from client_r import Client
from order_manager_r import OrderManager
from simulation_r import simulate_orders
from stage_r import Stage
from machine_r import Machine


def main():
    order_manager = OrderManager()

    # Configurar las máquinas para la Etapa 3
    machines_stage3 = [
        Machine(1, 3, {"botellas_1": 600, "botellas_2": 500}),
        Machine(2, 3, {"sobres_1": 800, "sobres_2": 760}),
        Machine(3, 3, {"botellas_1": 900, "sobres_1": 925}),
    ]
    stage3 = Stage(3, machines_stage3)

    while True:
        print("\nMenú Principal:")
        print("1. Registrar un nuevo cliente")
        print("2. Cancelar un pedido")
        print("3. Simular producción")
        print("4. Consultar estado actual de producción")
        print("5. Salir")
        choice = input("Seleccione una opción: ")

        if choice == "1":
            name = input("Nombre del cliente: ")
            print("Productos disponibles: botellas_1, botellas_2, sobres_1, sobres_2")
            order = {}
            while True:
                product = input("Producto (o 'fin' para terminar): ")
                if product == "fin":
                    break
                quantity = int(input(f"Cantidad de {product}: "))
                order[product] = quantity

            # Solicitar fecha y hora específicas para la entrega
            while True:
                try:
                    end_time_str = input("Ingrese la fecha y hora de entrega (YYYY-MM-DD, HH:MM): ")
                    end_time = datetime.strptime(end_time_str, "%Y-%m-%d, %H:%M")
                    current_time = datetime(2024, 11, 25)  # Fecha inicial asumida
                    if end_time <= current_time:
                        raise ValueError("La fecha y hora de entrega deben ser futuras.")
                    break
                except ValueError as e:
                    print(f"Entrada inválida: {e}")

            priority = int(input("Prioridad del pedido (1 = mayor prioridad): "))
            order_manager.add_client(name, order, end_time, priority)
            print(f"Pedido registrado para el cliente '{name}'.")

        elif choice == "2":
            client_id = int(input("ID del cliente para cancelar su pedido: "))
            order_manager.cancel_client_order(client_id)

        elif choice == "3":
            # Solicitar fecha y hora específicas para la simulación
            while True:
                try:
                    simulate_until_str = input("Ingrese la fecha y hora de finalización de la simulación (YYYY-MM-DD, HH:MM): ")
                    simulate_until = datetime.strptime(simulate_until_str, "%Y-%m-%d, %H:%M")
                    current_time = datetime(2024, 11, 25)  # Fecha inicial asumida
                    if simulate_until <= current_time:
                        raise ValueError("La fecha y hora deben ser futuras.")
                    break
                except ValueError as e:
                    print(f"Entrada inválida: {e}")

            # Calcular el total de horas a simular
            total_hours = int((simulate_until - current_time).total_seconds() / 3600)
            produced = simulate_orders(order_manager, stage3, total_hours)
            print("Producción lograda:", produced)

        elif choice == "4":
            current_time = datetime.now()
            status = order_manager.get_production_status(stage3.machines, current_time)
            print("\nEstado de las máquinas:")
            for machine_id, machine_status in status["machines"].items():
                print(f"- Máquina {machine_id}: {machine_status}")

            print("\nEstado de los pedidos:")
            for order_status in status["orders"]:
                print(f"- Cliente {order_status['cliente']}: {order_status}")

        elif choice == "5":
            print("Saliendo del programa.")
            break

        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()
