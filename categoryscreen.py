from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.app import App

# --- Import da Logica do Jogo --- #
# Importa-se a função setup_game e a lista de palabras do arquivo app.py
# Garanta que o app.py esteja na mesma pasta que esse arquivo
from game_logic import setup_game, game_words

 
# --- Tela para seleção de categoria --- #
class CategoryScreen(Screen):
    def __init__(self, **kwargs):
        super(CategoryScreen, self).__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', padding=30, spacing=30)
        
        title_label = Label(text="Escolha uma categoria")

        # Pega a lista da instancia main app para popular o spinner
        game_words = App.get_running_app().game_words
        # O spinner mostra o valor padrão e permite escolher da lista;
        # Pegamos esse nome da categoria diretamente da importação do dicionário 'game_words'
        self.category_spinner = Spinner(
            text=list(game_words.keys())[0],
            values=list(game_words.keys()),
            size_hint_y=None,
            height=44
        )
        # Botão para iniciar o jogo
        start_button = Button(text='Iniciar Jogo', font_size='20sp')
        # Essa é a chave: 'vincular' os botões em evento 'on_press' para o método self.start_game 
        # Quando o botão é pressionado,Kivy vai automaticamente chamar essa função
        start_button.bind(on_press=self.start_game_button_pressed)
        
        main_layout.add_widget(title_label)
        main_layout.add_widget(self.category_spinner)
        main_layout.add_widget(start_button)
        
        self.add_widget(main_layout)
        
    def start_game_button_pressed(self, instance):
        # Diz ao main app para iniciar a logica do jogo
        # Função que vai chamar o método start_game principal do app  
        # 'self.manager.parent' é uma forma de acessar a instancia proincipal do APP de uma tela
        App.get_running_app().start_game()