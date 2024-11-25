from product_r import Product

#Algoritmo funcionamiento

def get_user_input():
    print("Productos disponibles en la Etapa 3: botellas_1, botellas_2, sobres_1, sobres_2")
    demand = {}
    while True:
        product = input("Ingrese el nombre del producto (o 'fin' para terminar): ")
        if product == 'fin':
            break
        quantity = int(input(f"Ingrese la cantidad requerida para {product}: "))
        demand[product] = quantity

    days = int(input("Ingrese el plazo en días: "))
    hours = int(input("Ingrese el plazo en horas: "))
    total_hours = days * 24 + hours
    return demand, total_hours

def simulate_to_meet_demand(stage, demand, total_hours):
    produced = {product: 0 for product in demand.keys()}
    time_used = 0

    while time_used < total_hours:
        remaining_products = [Product(product) for product in demand.keys() if produced[product] < demand[product]]
        if not remaining_products:
            break

        results = stage.process(remaining_products, 1)
        time_used += 1

        for product_id, quantity in results:
            produced[product_id] += quantity

    return time_used, produced

def simulate_orders(order_manager, stage, total_hours):
    """Simula la producción considerando los pedidos de los clientes."""
    time_used = 0
    produced = {}

    while time_used < total_hours:
        active_orders = order_manager.get_active_orders()
        if not active_orders:
            break

        for client in active_orders:
            remaining_products = [
                Product(product) for product, qty in client.order.items()
                if produced.get((client.client_id, product), 0) < qty
            ]

            if not remaining_products:
                client.status = "completed"
                print(f"Pedido completado para el cliente '{client.name}'.")
                continue

            results = stage.process(remaining_products, 1)
            time_used += 1

            for product_id, quantity in results:
                key = (client.client_id, product_id)
                produced[key] = produced.get(key, 0) + quantity

    return produced
