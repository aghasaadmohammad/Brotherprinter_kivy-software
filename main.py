import kivy
from kivy.app import App
import pandas as pd
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from PIL import ImageColor
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.core.window import Window
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from kivy.utils import get_color_from_hex

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)

df = pd.read_csv('myfile.csv')
colorsname=df['Colors - Display Name']
colorsdisplaycolor=df['Colors - Display Color']
colorsprinttext=df['Colors - Print text']
textcolor=df['Text Color']
printingargs=[0,0,0,0,0]
color_displayname=df.loc[0]


# print(color_displayname['Colors - Display Color'])
class KeypadPopup(Popup):
    def __init__(self, callback, **kwargs):
        super(KeypadPopup, self).__init__(**kwargs)
        self.callback = callback
        mybox=BoxLayout(orientation='vertical', size_hint=(1, None),size_hint_y = 1)
        self.text_input = TextInput(size_hint=(0.8, None))
        mybox.add_widget(self.text_input)
        layout = GridLayout(cols=6, spacing=0)


        for i in range(1, 10):
            button = Button(text=str(i), size_hint=(None, None), size=(50, 50))
            button.bind(on_press=self.button_pressed)
            layout.add_widget(button)

        button = Button(text="0", size_hint=(None, None), size=(50, 50))
        button.bind(on_press=self.button_pressed)
        layout.add_widget(button)

        buttondel = Button(text="Del", size_hint=(None, None), size=(50, 50))
        buttondel.bind(on_press=self.deltext)
        buttonProceed = Button(text="ok", size_hint=(None, None), size=(50, 50))
        buttonProceed.bind(on_press=self.customamount)
        layout.add_widget(buttondel)
        layout.add_widget(buttonProceed)
        mybox.add_widget(layout)

        self.content = mybox
        self.size_hint = (0.6, 0.6)
        self.size = (200, 250)
    def deltext(self,button):
        self.text_input.text =''
    def button_pressed(self, button):
        self.text_input.text += button.text
    def customamount(self,button):
        printingargs[1]=self.text_input.text
        pass
    def printing_data(self):
        pass
class MyApp(BoxLayout):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.count=0
        # Set the orientation of the BoxLayout
        self.orientation = 'vertical'
        # Create an instance of the scrollerPage widget
        self.scroller_page = scrollerPage()
        # Add the scrollerPage widget as a child widget of MyApp
        # self.add_widget(self.scroller_page)
        #
        # ###############################################################
        button_layout = BoxLayout(orientation='horizontal', size_hint=(0.572, 0.1))
        self.my_label = Label(text=str(self.count),size_hint=(1,1))

        self.increment_button = Button(text='Increment',size_hint=(1,1))
        self.increment_button.bind(on_press=self.increment_label)


        # Create a Button widget to decrement the label value
        self.decrement_button = Button(text='Decrement',size_hint=(1,1))
        self.decrement_button.bind(on_press=self.decrement_label)
        self.myprint = Button(text='Print', size_hint=(1, 1))
        self.myprint.bind(on_press=self.sendprint)
        button_layout.add_widget(self.increment_button)
        button_layout.add_widget(self.my_label)
        button_layout.add_widget(self.decrement_button)

        button_layout.add_widget(self.myprint)
        self.add_widget(button_layout)
        ################################################
    def increment_label(self, *args):
        current_value = int(self.my_label.text)
        self.my_label.text = str(current_value + 1)


    def decrement_label(self, *args):
        current_value = int(self.my_label.text)
        if current_value>0:
            self.my_label.text = str(current_value - 1)

    def sendprint(self,*args):
        # conn = cups.Connection()
        # printers = conn.getPrinters()
        # print(printers)
        # printer_name = 'Brother_QL_1110NWB'
        # print(printer_name)
        printingargs[3] = self.my_label.text
        printingargs[4] = self.ids.switch_label.text
        with open("labelprint.txt", "w") as file:
            for i, item in enumerate(printingargs):
                file.write("%s\n" % item)
                printingargs[i] = 0
        # conn.printFile(printer_name, 'labelprint.txt', '',
        #                {'landscape': 'True', 'cpi': '14', 'lpi': '10'})  # the smaller cpi/lpi the bigger the fonts

        # print(printingargs)




class CustomButton(Button):
    root_widget = ObjectProperty()

    def on_release(self, **kwargs):
        super().on_release(**kwargs)
        self.root_widget.btn_callback(self)


class scrollerPage(RecycleView):
    def __init__(self, **kwargs):
        super(scrollerPage,self).__init__(**kwargs)
        # Set the data for the RecycleView
        # self.data = [{'text': str(i["title"])} for i in file_list]
        self.data = [{'text': str(x["title"]), 'root_widget': self} for x in file_list]
        # self.mytestdata=[]
        # for i in file_list:
        #     self.mytestdata.append(i['title'])
        #
        # print(self.mytestdata)
        # self.view = RVButton(text=self.data['text']["title"])
        # self.view.bind(on_press=self.on_button_press)
        # self.viewclass = 'Button'
        # self.viewclass_args = {'size_hint_y': None, 'height': 30}

    def btn_callback(self, btn):

        index = btn.text.find('.')
        if index != -1:
            output_str = btn.text[:index]
        else:
            output_str = btn.text
        # print(output_str)
        printingargs[0]=output_str


class main(App):  # <- Main Class
    def build(self):
        Window.clearcolor = (0.5, 0.5, 0.5, 1.0)
        myapp=MyApp()
        myapp.ids.mybutton1.text=colorsname[0]
        # print(ImageColor.getcolor(colorsdisplaycolor[5], "RGB"))
        myapp.ids.mybutton1.background_color=(tuple( ti/255 for ti in ImageColor.getcolor(colorsdisplaycolor[0], "RGB")))
        # print(df.count())
        myapp.ids.mybutton37.bind(on_press=self.open_keypad)
        s = myapp.ids
        for a,i in enumerate(s):
            if str(i).startswith('m')== True:
                try:

                    # print(colorsname)
                    # getattr(myapp.ids, i).bind(on_press=self.savedata(self))
                    if colorsname[a]=='nan' or colorsname[a]=='Placeholder':

                        getattr(myapp.ids, i).text = ' '
                    else:


                        getattr(myapp.ids, i).text = colorsname[a]
                        getattr(myapp.ids, i).font_size=10
                    getattr(myapp.ids, i).background_normal = ''
                    getattr(myapp.ids, i).border = [10, 10, 10, 10]
                    #getattr(myapp.ids, i).background_color = (tuple(ti for ti in ImageColor.getcolor(colorsdisplaycolor[a], "RGBA")))
                    getattr(myapp.ids, i).background_color = (tuple(get_color_from_hex(colorsdisplaycolor[a])))
                    # print((tuple(ti for ti in ImageColor.getcolor(colorsdisplaycolor[a], "RGBA"))))
                    getattr(myapp.ids,i).color=(tuple(ti / 255 for ti in ImageColor.getcolor(textcolor[a], "RGBA")))
                except:
                    if colorsname[a] == 'nan':
                        print(colorsname[a])
                        getattr(myapp.ids, i).text = ' '
                        getattr(myapp.ids, i).background_color = ImageColor.getcolor("#c2c2c3", "RGBA")
                        getattr(myapp.ids, i).color = (tuple(ti / 255 for ti in ImageColor.getcolor("#000000", "RGB")))
                    else:
                        print(colorsname[a])
                        getattr(myapp.ids, i).text = str(colorsname[a])
                        getattr(myapp.ids, i).background_color = ImageColor.getcolor("#c2c2c3", "RGBA")
                        getattr(myapp.ids, i).color = (tuple(ti / 255 for ti in ImageColor.getcolor("#000000", "RGB")))


        Window.size = (800, 480)
        return myapp
    def savedata(self,button):
        # print(button.text)
        printingargs[2]=button.text

        pass
    def amountsavedata(self,button):
        printingargs[1] = button.text

    def open_keypad(self, button):
        def callback(text):
            button.text += text


        keypad_popup = KeypadPopup(callback=callback)
        keypad_popup.open()



if __name__ == "__main__":

    # Define the query to list all files
    query = "'root' in parents and trashed=false"

    # Get the list of all files in the root directory
    file_list = drive.ListFile({'q': query}).GetList()

    # Print the list of files
    if not file_list:
        print('No files found.')
    else:
        print('Files:')
 #       for file in file_list:
  #          print(f'{file["title"]} ({file["id"]})')
    main().run()
