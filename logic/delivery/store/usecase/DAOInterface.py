from abc import *
from typing import List
from logic.delivery.store.domain.dto.MenuSummaryDto import MenuSummaryDto


class MenuDAO(metaclass=ABCMeta):
    @abstractmethod
    def find_all_menu_summary_by_store_id(self, store_id) -> List[MenuSummaryDto]:
        pass
