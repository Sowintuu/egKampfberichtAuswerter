class Fighter:
    def __init__(self, name):
        # Init attributes.
        # Information from end report.
        self.name = name
        self.health_rel_end = None
        self.status_end = None

        # Information from main report.
        self.actions = []

        # Calculated information.
        self.health_overall = None

    def set_end_values(self, status, health):
        self.status_end = status
        self.health_rel_end = health

