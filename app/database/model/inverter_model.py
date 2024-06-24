class InverterModel:
    def __init__(self, model_id: int = None, name: str = None, com_disc: str = None):
        if model_id is None or name is None or com_disc is None:
            pass  # TODO inja bayad tasmim begirim age in etefaghe biofte yani chi(yani keihas etefagh miofte) v bayad chi kar konim
        self.model_id = model_id
        self.name = name
        self.com_disc = com_disc

        # TODO:yeki az aval check kone kodoma behesh vaslan

        # TODO :falg dashte bashe k faal v gheir faal beshe

        # TODO:to log ham bayad az in estefade kone

    def __repr__(self):
        return f"InverterModel({self.model_id}, {self.name}, {self.com_disc})"
