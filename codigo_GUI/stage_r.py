class Stage:
    def __init__(self, id, machines):
        self.id = id
        self.machines = machines

    def process(self, products, time):
        output = []
        for product in products:
            for machine in self.machines:
                produced = machine.produce(product.id, time)
                if produced > 0:
                    output.append((product.id, produced))
                    break
        return output
