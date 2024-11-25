class Machine:
    def __init__(self, id, stage, rates):
        self.id = id
        self.stage = stage
        self.rates = rates  # Diccionario {producto: tasa}
        self.remaining_time = 0  # Tiempo restante para terminar la tarea actual
        self.last_product = None  # Producto procesado anteriormente
        self.state = "apagada"  # Estado inicial de la máquina
        self.current_product = None  # Producto que está procesando

    def calculate_setup_time(self):
        """Devuelve el tiempo de setup según la etapa."""
        if self.stage == 1:
            return 0.5  # 30 minutos = 0.5 horas
        elif self.stage == 2:
            return 0.833  # 50 minutos = 0.833 horas
        elif self.stage == 3:
            return 0.333  # 20 minutos = 0.333 horas
        return 0

    def produce(self, product, time):
        """
        Intenta producir un producto dado durante un periodo de tiempo.
        Retorna la cantidad producida.
        """
        if self.remaining_time > 0:
            # La máquina está ocupada, reduce el tiempo restante.
            self.remaining_time = max(0, self.remaining_time - time)
            if self.remaining_time == 0:
                # Termina la producción actual.
                self.state = "apagada"
                self.current_product = None
            return 0  # No produce nada nuevo mientras está ocupada.

        # Calcular tiempo de setup si cambia de producto.
        setup_time = 0
        if self.last_product is not None and self.last_product != product:
            setup_time = self.calculate_setup_time()

        if product in self.rates:
            # Configurar nueva producción.
            self.remaining_time = 1 + setup_time  # Un lote tarda 1 hora + tiempo de setup
            self.state = "prendida"
            self.current_product = product
            self.last_product = product

            # Calcular producción efectiva considerando tiempo disponible.
            production_time = max(0, time - setup_time)
            return self.rates[product] * production_time
        return 0  # No puede producir este producto.

    def update_time(self, time):
        """
        Actualiza el estado de la máquina al reducir el tiempo restante.
        """
        if self.remaining_time > 0:
            self.remaining_time = max(0, self.remaining_time - time)
            if self.remaining_time == 0:
                # Si el tiempo restante llega a 0, apagar la máquina.
                self.state = "apagada"
                self.current_product = None
