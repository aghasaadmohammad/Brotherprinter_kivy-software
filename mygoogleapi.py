from kivy.app import App
from kivy.uix.button import Button

class MyButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self. background_normal=''
        self.background_color = (1,1,0,1)  # set background color to red

class MyApp(App):
    def build(self):
        return MyButton()

if __name__ == '__main__':
    MyApp().run()