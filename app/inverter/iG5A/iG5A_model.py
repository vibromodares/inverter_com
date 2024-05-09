from app.inverter.inverter_model import InverterBaseModel


class iG5AModel(InverterBaseModel):
    def __init__(self):
        super().__init__()
        self.model = 'iG5A'
