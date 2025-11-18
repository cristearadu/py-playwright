from pages.base_page import BasePage


class HerokuDragAndDropPage(BasePage):
    A = "#column-a"
    B = "#column-b"
    HEADER_A = "#column-a header"
    HEADER_B = "#column-b header"

    def swap_a_to_b(self):
        self.scroll_into_view(self.A)
        self.el(self.A).drag_to(self.el(self.B))

    def labels(self) -> tuple[str, str]:
        return self.get_text(self.HEADER_A), self.get_text(self.HEADER_B)