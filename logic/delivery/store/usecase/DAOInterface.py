from abc import *
from logic.delivery.store.domain.dto.MenuSummaryDto import MenuSummaryDto


class MenuDAO(metaclass=ABCMeta):
    @abstractmethod
    def find_all_menu_summary_by_store_id(self, store_id) -> MenuSummaryDto:
        pass
