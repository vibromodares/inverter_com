from typing import Optional

from app.database.model.database_model import DataModel


class CommunicationResponse:
    description: str = ''
    range_in: str
    code: str
    response_data: str
    response_data_in: str
    range_start: int
    range_end: int
    db: DataModel
    scale: int
    unit: str
    have_allotment: bool
    true_value: float

    def __init__(self, code: str, range_in: str, response_data: str, db: Optional[DataModel], have_allotment: bool = True,
                 scale: int = -1, unit: str = ''):
        self.code = code

        self.db = db
        self.unit = unit
        self.scale = scale
        self.have_allotment = have_allotment
        self.true_value = 0

        if self.db is None:
            return

        self.range_in = range_in
        self.range_start = int(range_in[0], 16)
        self.range_end = int(range_in[3], 16)

        self.response_data_in = response_data

        binary_response_data = format(int(response_data, 16), '0>16b')
        self.response_data = binary_response_data[15 - self.range_end:15 - self.range_start + 1]

        if self.have_allotment:
            temp_response_1 = self.db.get_responses('0x' + self.code, str(int(self.response_data, 2)), self.range_in)
            temp_response_2 = self.db.get_responses('0x' + self.code, self.response_data_in, self.range_in)

            if len(temp_response_1) != 0:
                self.response = temp_response_1
            elif len(temp_response_2) != 0:
                self.response = temp_response_2
            elif self.response_data == '0000':
                temp_response_3 = self.db.get_responses('0x' + self.code, range_in=self.range_in)  # for Reserved
                self.response = temp_response_3
            else:
                self.response = []

            if len(self.response) == 0:
                print(self.response)
                print('cant find bad data response allotment', self.code, self.response_data, self.range_in)

            elif len(self.response) != 1:
                print(self.response)
                print('bad data response allotment', self.code, self.response_data, self.range_in)

            else:
                self.response = self.response[0]
                self.description = self.response['description']
        else:
            self.description = str(int(self.response_data_in, 16) * float(self.scale)) + ' ' + self.unit
            self.true_value = int(self.response_data_in, 16) * float(self.scale)

    def __repr__(self):
        # return "CR(" + self.code + ", " + self.range_in + ", " + self.response_data + ", " + self.description + ")"
        return "CR(" + self.code + ", " + self.description + ")"
