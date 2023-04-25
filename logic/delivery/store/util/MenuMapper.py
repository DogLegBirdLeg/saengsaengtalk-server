from logic.delivery.store.domain.entity.Menu import Menu
from logic.delivery.store.domain.entity.Group import Group
from logic.delivery.store.domain.entity.Option import Option


class MenuMapper:
    @staticmethod
    def menu_mapping(menu_json) -> Menu:
        groups = [MenuMapper.group_mapping(group_json) for group_json in menu_json['groups']]
        menu = Menu(str(menu_json['_id']), menu_json['section'], menu_json['name'], menu_json['price'], groups)
        return menu

    @staticmethod
    def group_mapping(group_json) -> Group:
        options = [MenuMapper.option_mapping(option_json) for option_json in group_json['options']]
        group = Group(str(group_json['_id']), group_json['name'], group_json['min_order_quantity'], group_json['max_order_quantity'], options)
        return group
        
    @staticmethod
    def option_mapping(option_json) -> Option:
        option = Option(str(option_json['_id']), option_json['name'], option_json['price'])
        return option
