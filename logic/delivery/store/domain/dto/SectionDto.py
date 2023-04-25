from logic.delivery.store.domain.dto.MenuSummaryDto import MenuSummaryDto
from typing import List


class Section:
    def __init__(self, name, menus: List[MenuSummaryDto]):
        self.name = name
        self.menus = menus

    @property
    def json(self):
        return {
            'section_name': self.name,
            'menus': [menu.json for menu in self.menus]
        }


class Sections:
    def __init__(self, menus: List[MenuSummaryDto]):
        self.sections: List[Section] = []

        def find_section(name):
            for section in self.sections:
                if name == section.name:
                    return section

        for menu in menus:
            section = find_section(menu.section)
            if section is None:
                self.sections.append(Section(menu.section, [menu]))
                continue
            section.menus.append(menu)

    @property
    def json(self):
        return [section.json for section in self.sections]
