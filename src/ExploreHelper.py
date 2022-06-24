import pyautogui
import ctypes

class ExploreHelper(object):
    DICTIONARY = {'de': {},
                  'en': {}}
    DICTIONARY['de']['reload'] = 'Kicke den "Neu laden" Button unterhalb der Karte.'
    DICTIONARY['de']['init_top_left'] = 'Bewege den Mauszeiger zur oberen linken Ecke des zu überwachenden Bereichs ' \
                                        'und drücke "Enter".'
    DICTIONARY['de']['init_bottom_right'] = 'Bewege den Mauszeiger zur unteren rechten Ecke des zu überwachenden ' \
                                            'Bereichs und drücke "Enter".'

    def __init__(self):
        # Init attributes.
        self.pos_top_left = None
        self.pos_bottom_right = None
        self.x_positions = []
        self.y_positions = []
        self.color_matrix = []
        self.color_matrix_old = []

        # Setup dictionary.
        self.dictionary = self.DICTIONARY['de']

    def init_helper(self):
        # Get positions.
        input(self.dictionary['init_top_left'])
        pos_top_left = list(pyautogui.position())

        input(self.dictionary['init_bottom_right'])
        pos_bottom_right = list(pyautogui.position())

        # Get screen region.
        # self.screen_region = []
        # self.screen_region.extend(self.pos_top_left)
        # self.screen_region.extend(self.pos_bottom_right)

        # Get tile points.
        x_length = pos_bottom_right[0] - pos_top_left[0]
        y_length = pos_bottom_right[1] - pos_top_left[1]

        self.x_positions = [pos_top_left[0] + 1/6 * x_length,
                            pos_top_left[0] + 3/6 * x_length,
                            pos_top_left[0] + 5/6 * x_length]
        self.y_positions = [pos_top_left[0] + 1/6 * y_length,
                            pos_top_left[0] + 3/6 * y_length,
                            pos_top_left[0] + 5/6 * y_length]

        # Init color matrix for next steps.
        self.color_matrix = [(0, 0, 0)] * 8

        # Get initial color matrix.
        self.get_color_matrix()

        breakpoint()

    # Get color information from the tile positions.
    # Doesn't save the middle tile.
    def get_color_matrix(self):
        # Save previous color matrix.
        self.color_matrix_old = self.color_matrix.copy()

        # Re init matrix.
        self.color_matrix = []

        # get screenshot.
        im = pyautogui.screenshot()

        # Store color information for each tile.
        for x_id, x_pos in enumerate(self.x_positions):
            for y_id, y_pos in enumerate(self.y_positions):
                # Skip the middle tile.
                if x_id != 1 or y_id != 1:
                    self.color_matrix.append(im.getpixel((x_pos, y_pos)))

        breakpoint()



    def compare_cycle(self):
        # Reload.
        pyautogui.click(r'..\temp\Karte.png')

        # Get current color matrix.
        self.get_color_matrix()

        # Compare old and current matrix.
        for k in enumerate(self.color_matrix):
            if self.color_matrix != self.color_matrix_old:
                ctypes.windll.user32.MessageBoxW(0, "Your text", "Your title", 1)


if __name__ == '__main__':
    eh = ExploreHelper()
    eh.init_helper()
