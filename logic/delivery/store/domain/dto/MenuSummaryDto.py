class MenuSummaryDto:
    def __init__(self, _id: str, section: str, name: str, price: int):
        self._id = _id
        self.section = section
        self.name = name
        self.price = price

    @property
    def json(self):
        return {
            '_id': self._id,
            'section': self.section,
            'name': self.name,
            'price': self.price,
        }

    @staticmethod
    def mapping(menu_summary_json):
        return MenuSummaryDto(_id=menu_summary_json['_id'],
                              section=menu_summary_json['section'],
                              name=menu_summary_json['name'],
                              price=menu_summary_json['price'])
