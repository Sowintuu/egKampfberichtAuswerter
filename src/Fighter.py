class Fighter:
    def __init__(self, name):
        self.name = name
        self.health_rel_end = None
        self.status_end = None

    def set_end_values(self, status, health):
        self.status_end = status
        self.health_rel_end = health

