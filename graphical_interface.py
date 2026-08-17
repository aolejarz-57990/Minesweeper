from abc import ABC, abstractmethod


class GraphicalInterface(ABC):

    def __init__(self):
        self.running = True

    @abstractmethod
    def draw_map(self):
        pass

    @abstractmethod
    def handle_mouse_click(self, button):
        pass

    @abstractmethod
    def get_events(self):
        pass

    @abstractmethod
    def update_display(self):
        pass

    @abstractmethod
    def close(self):
        pass

    def run(self):

        while self.running:

            buttons = self.get_events()

            for button in buttons:
                self.handle_mouse_click(button)

            self.draw_map()

            self.update_display()

        self.close()