from app.api.Store.Domain.Model.MenuSummary import MenusSummary, MenuSummary
from app.api.Store.Domain.Model.Menu import Menu, Menus
from app.api.Store.Domain.Model.Group import Group, Groups
from app.api.Store.Domain.Model.Option import Option, Options


class MenuMapper:
    @staticmethod
    def menus_mapping(menus_json) -> Menus:
        menus = Menus([MenuMapper.menu_mapping(menu_json) for menu_json in menus_json])
        return menus

    @staticmethod
    def menu_mapping(menu_json) -> Menu:
        groups = MenuMapper.groups_mapping(menu_json['groups'])
        menu = Menu(str(menu_json['_id']), menu_json['section'], menu_json['name'], menu_json['price'], groups)
        return menu

    @staticmethod
    def groups_mapping(groups_json) -> Groups:
        groups = Groups([MenuMapper.group_mapping(group_json) for group_json in groups_json])
        return groups

    @staticmethod
    def group_mapping(group_json) -> Group:
        options = MenuMapper.options_mapping(group_json['options'])
        group = Group(str(group_json['_id']), group_json['name'], group_json['min_order_quantity'], group_json['max_order_quantity'], options)
        return group

    @staticmethod
    def options_mapping(options_json) -> Options:
        options = Options([MenuMapper.option_mapping(option_json) for option_json in options_json])
        return options
        
    @staticmethod
    def option_mapping(option_json) -> Option:
        option = Option(str(option_json['_id']), option_json['name'], option_json['price'])
        return option


class MenuSummaryMapper:
    @staticmethod
    def menus_mapping(menus_json) -> MenusSummary:
        menus = MenusSummary([MenuSummaryMapper.menu_mapping(menu_json) for menu_json in menus_json])
        return menus

    @staticmethod
    def menu_mapping(menu_json) -> MenuSummary:
        menu = MenuSummary(str(menu_json['_id']), menu_json['section'], menu_json['name'], menu_json['price'])
        return menu
