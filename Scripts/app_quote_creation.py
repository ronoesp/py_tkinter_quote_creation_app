from window_main import WindowMain as wm
from DB.data_base_controller import DatabaseController

class App():
    def __init__(self):
        DatabaseController.init_db()
        self.wm = wm()
        
    def main(self):
        self.wm.main()
        
app = App()
app.main()