from random import randint
from kivy import Config

Config.set('graphics', 'width', 600)
Config.set('graphics', 'height', 300)


from kivy.core.window import Keyboard
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.spinner import Spinner
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput


Window.size = (dp(600), dp(300))
DICES = [2, 3, 4, 6, 8, 10, 12, 20, 100]
modifier = 0
numero_de_tiradas = 1

Dice4 = CheckBox(group=True, color=(255, 0, 0, 3))
lista_num = Spinner(size_hint_y=0.5, text="1", values=("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"))
lista_mod = Spinner(size_hint_y=0.3, text="0", values=("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"))

change_num = TextInput(text=lista_num.text, size_hint=(0.5, 0.5), multiline=False)
change_mod = TextInput(text=lista_mod.text, size_hint=(0.5, 0.4), multiline=False)

Builder.load_string('''


<RV>:
    viewclass: 'Label'

    RecycleBoxLayout:

        default_size: None, dp(20)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')


"""class hola(RecycleBoxLayout):

    def __init__(self, **kwargs):
        super(hola, self).__init__(**kwargs)

        self.default_size = (None, dp(20))
        self.default_size_hint = (1, None)
        self.size_hint_y: None
        self.height: self.minimum_height
        self.viewclass = "Label"
        self.orientation = "vertical"
        """


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)


class Boton(CheckBox):

    def __init__(self, **kwargs):
        super(Boton, self).__init__(**kwargs)
        self.color = (255, 0, 0, 3)
        self.dice = 0


class LoginScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        self.modifier = 0
        self.number_of_dices = 1
        self.type_dice = 0
        self.registro = 0
        self.orientation = "vertical"
        self.calculo_resultado = 0
        self.mod_is_negative = 1
        self.cb_list = []
        self.critical = ""

        Window.bind(on_key_up=self.read_key)

        # Añadiendo Widgets

        cuadricula_inicial = GridLayout()
        cuadricula_inicial.cols = 9
        cuadricula_inicial.rows = 2
        self.add_widget(cuadricula_inicial)

        # añadiendo primera cara textos y checkboxes

        for i in DICES:
            cuadricula_inicial.add_widget(Label(text="1d{0}".format(i), size_hint=(1, None), font_size=14, height=20))

        for i in DICES:
            cb = CheckBox(group=True, color=(255, 0, 0, 3), id=str(i))
            cb.bind(active=self.update_type_dice)
            cuadricula_inicial.add_widget(cb)
            self.cb_list.append(cb)

        # Segunda Caja:

        caja_de_modificadores = BoxLayout(orientation="horizontal")
        self.add_widget(caja_de_modificadores)

        # 2.1
        caja_num = StackLayout()
        caja_de_modificadores.add_widget(caja_num)
        caja_num.add_widget(Label(text="Dice Number", size_hint=(0.5, 0.5)))
        caja_num.add_widget(change_num)
        change_num.bind(text=self.input_number)
        caja_num.add_widget(lista_num)
        lista_num.bind(text=self.cuantas_lanzadas)

        # 2.2
        caja_mod = StackLayout()
        caja_de_modificadores.add_widget(caja_mod)
        caja_mod.add_widget(Label(text="Modifier", size_hint=(0.5, 0.4)))
        caja_mod.add_widget(change_mod)
        change_mod.bind(text=self.input_modifier)
        caja_mod.add_widget(Label(text="Negativo", size_hint=(0.5, 0.3)))
        self.cb_negative = CheckBox(size_hint=(0.5, 0.3))
        caja_mod.add_widget(self.cb_negative)
        self.cb_negative.bind(active=self.negative_modifier)
        caja_mod.add_widget(lista_mod)
        lista_mod.bind(text=self.cuanto_es_modificador)

        # 2.3
        self.btn = Button(text="Lanzar", font_size=18, )
        self.btn.bind(on_press=self.lanzar_dados)
        caja_de_modificadores.add_widget(self.btn)

        # Tercera caja

        self.resultado = Label(text="Esperando Lanzamiento de dados", color=(1, 0, 0, 0.8))
        self.add_widget(self.resultado)

        # Cuarta caja

        self.lista_registro = RV()
        self.add_widget(self.lista_registro)

        # xxxxxxxxxxxxxxxxxx

    def update_type_dice(self, obj, active):

        if active:
            self.type_dice = int(obj.id)

    # LANZAMIENTO DE LOS DADOS

    def lanzar_dados(self, obj):
        try:
            self.calculo_resultado = 0
            if self.registro > 0:
                self.lista_registro.data.insert(0, {
                    "text": "Lanzamiento Nº{} ".format(len(self.lista_registro.data) + 1) + self.resultado.text})

            for i in range(self.number_of_dices):
                self.calculo_resultado += randint(1, self.type_dice)
                if self.type_dice == 20 and self.number_of_dices == 1 and self.calculo_resultado == 20:
                    self.critical = " ES CRITICO"
                else:
                    self.critical = ""

            self.calculo_resultado += self.modifier * self.mod_is_negative

            if self.mod_is_negative == -1:
                self.resultado.text = "El resultado de {2}d{1} -{3} = {0}".format(
                    self.calculo_resultado, self.type_dice, self.number_of_dices, self.modifier) + self.critical
            else:
                self.resultado.text = "El resultado de {2}d{1} +{3} = {0}".format(
                    self.calculo_resultado, self.type_dice, self.number_of_dices, self.modifier) + self.critical

            self.registro = 1

            if {"text": "Esperando Lanzamiento de dados"} in self.lista_registro.data:
                self.lista_registro.data.remove({"text": "Esperando Lanzamiento de dados"})

        except ValueError:
            self.resultado.text = "NO SE HA SELECCIONADO NINGUN DADO"

    def cuanto_es_modificador(self, obj, text):

        self.modifier = int(text)
        change_mod.text = text

    # INPUT LISTA num de dados

    def cuantas_lanzadas(self, obj, text):

        self.number_of_dices = int(text)
        change_num.text = text

    def negative_modifier(self, obj, active):

        if obj.active:
            self.mod_is_negative = -1
        else:
            self.mod_is_negative = 1

    # ESCRIBIR MODIFICADOR

    def input_modifier(self, obj, text):

        if obj.text == "":
            pass

        elif obj.text == "-":

            obj.text = ""
            self.cb_negative.active = True

        elif obj.text == "+":

            obj.text = ""
            self.cb_negative.active = False
        elif "n" in obj.text:

            obj.text = lista_mod.text

        elif obj.text.isdigit():
            lista_mod.text = text
        else:

            obj.text = lista_mod.text

    # ESCRIBIR NUMERO DE DADOS

    def input_number(self, obj, text):

        if obj.text == "":

            pass

        elif "m" in obj.text:

            obj.text = lista_num.text

        elif obj.text.isdigit():

            lista_num.text = obj.text
        else:
            obj.text = lista_num.text

            # LECTURA DE TECLADO

    # LEECTURA DE TECLADO

    def read_key(self, obj, keycode, something):

        #  print((Keyboard.keycode_to_string(obj, keycode)))

        if (Keyboard.keycode_to_string(obj, keycode)) == "right":

            if not change_mod.focus and not change_num.focus:
                if self.type_dice == 100:
                    self.cb_list[DICES.index(self.type_dice)].active = False
                    self.cb_list[0].active = True
                elif self.type_dice == 0:
                    self.cb_list[0].active = True
                else:
                    self.cb_list[DICES.index(self.type_dice)].active = False
                    self.cb_list[DICES.index(self.type_dice) + 1].active = True

        if (Keyboard.keycode_to_string(obj, keycode)) == "left":
            if not change_mod.focus and not change_num.focus:
                if self.type_dice == 2:
                    self.cb_list[DICES.index(self.type_dice)].active = False
                    self.cb_list[len(self.cb_list) - 1].active = True
                elif self.type_dice == 0:
                    self.cb_list[0].active = True
                else:
                    self.cb_list[DICES.index(self.type_dice)].active = False
                    self.cb_list[DICES.index(self.type_dice) - 1].active = True

        if (Keyboard.keycode_to_string(obj, keycode)) == "enter":
            self.lanzar_dados(self.btn)
        if (Keyboard.keycode_to_string(obj, keycode)) == "up":

            if change_num.focus:
                change_num.focus = False
                change_mod.focus = True
            else:
                change_num.focus = True
                change_mod.focus = False
        if (Keyboard.keycode_to_string(obj, keycode)) == "down":
            change_num.focus = False
            change_mod.focus = False
        if (Keyboard.keycode_to_string(obj, keycode)) == "r":
            change_num.text = "1"
            change_mod.text = "0"
        if (Keyboard.keycode_to_string(obj, keycode)) == "n":
            change_num.focus = True
            change_num.text = ""
        if (Keyboard.keycode_to_string(obj, keycode)) == "m":
            change_mod.focus = True
            change_mod.text = ""
        if (Keyboard.keycode_to_string(obj, keycode)) == "spacebar":
            change_num.focus = False
            change_mod.focus = False


class DicesApp(App):

    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    DicesApp().run()
