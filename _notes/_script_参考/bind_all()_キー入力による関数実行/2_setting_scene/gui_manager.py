import tkinter as tk
from tk_gui_base import TKGUIBase as tgb

class GUIManager():
    def __init__(self):
        self.gui = tgb()
        
    def main(self):
        self.gui.main()
    
app = GUIManager()
app.main()