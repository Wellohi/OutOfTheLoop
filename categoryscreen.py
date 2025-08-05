from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.utils import get_color_from_hex
 
# --- Tela para seleção de categoria --- #
class CategoryScreen(Screen):
    def __init__(self, **kwargs):
        super(CategoryScreen, self).__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=30)
        
        title_label = Label(text="Configurações do Jogo", font_size='24sp', bold=True)

        category_label = Label(text="Escolha uma categoria", size_hint_y=None, height=30)
        self.category_grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        self.category_grid.bind(minimum_height=self.category_grid.setter('height'))
        
        rounds_label = Label(text="Selecione Quantas Rodadas de Perguntas", size_hint_y=None, height=30)
        self.rounds_grid = GridLayout(cols=3, spacing=10, size_hint_y=None)
        self.rounds_grid.bind(minimum_height=self.rounds_grid.setter('height'))
        
        self.selected_category = None
        self.selected_round = None
        self.category_buttons = []
        self.round_buttons = []
                
        # Pega a lista da instancia main app para popular o spinner
        game_words = App.get_running_app().game_words
        for category_name in game_words.keys():
            btn = Button(text=category_name, size_hint_y=None, height=50, background_normal='')
            btn.bind(on_press=self.select_category)
            self.category_buttons.append(btn)
            self.category_grid.add_widget(btn)
            
        for round_num in ['1', '2', '3']:
            btn = Button(text=round_num, size_hint_y=None, height=50, background_normal='')
            btn.bind(on_press=self.select_round)
            self.round_buttons.append(btn)
            self.rounds_grid.add_widget(btn)
        
        # Botão de voltar telas
        navigation_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        
        back_button = Button(text="Voltar", font_size='20sp')
        back_button.bind(on_press=self.go_back)
        
        # Botão para iniciar o jogo
        continue_button = Button(text='Iniciar Jogo', font_size='20sp', size_hint_y=None, height=50)
        continue_button.bind(on_press=self.start_game_button_pressed)
        
        navigation_layout.add_widget(back_button)
        navigation_layout.add_widget(continue_button)
        
        self.status_label = Label(text="", color=(1,0,0,1), font_size='16sp', size_hint_y=None, height=30)
        
        main_layout.add_widget(title_label)
        main_layout.add_widget(category_label)
        main_layout.add_widget(self.category_grid)
        main_layout.add_widget(rounds_label)
        main_layout.add_widget(self.rounds_grid)
        main_layout.add_widget(navigation_layout)
        main_layout.add_widget(self.status_label)
        
        self.add_widget(main_layout)
        
        self.reset_button_colors()
        
    def on_pre_enter(self, *args):
        """
        Reseta a seleção quando a tela aparece
        """
        self.selected_category =None
        self.selected_round = None
        self.status_label.text = ""
        self.reset_button_colors()
        
    def reset_button_colors(self):
        """
        Função ajudante que 'seta' todos botões para suas cores padrao
        """
        default_color = get_color_from_hex("#34495e")
        for btn in self.category_buttons:
            btn.background_color = default_color
        for btn in self.round_buttons:
            btn.background_color = default_color            
        
    def select_category(self, instance):
        """
        lida com a logica do botão de seleção de categoria
        """
        self.selected_category = instance.text
        # Dá um feedback visual para a seleção
        for btn in self.category_buttons:
            if btn == instance:
                # Seleciona a cor do botão
                btn.background_color = get_color_from_hex("#3498db")
            else:
                # Cor padrão
                btn.background_color = get_color_from_hex("#34495e")

    def select_round(self, instance):
        """
        Lidacom a lógica do botão de seleção de round
        """
        self.selected_round = int(instance.text)
        for btn in self.round_buttons:
            if btn == instance:
                btn.background_color = get_color_from_hex("#3498db")
            else:
                # Cor padrão
                btn.background_color = get_color_from_hex("#34495e")
                
        
        
    def start_game_button_pressed(self, instance):
        """
        Valida as seleções e diz para o app principal para iniciar o jogo
        """
        if not self.selected_category:
            self.status_label.text = "Selecione uma categoria"
            return
        if not self.selected_round:
            self.status_label.text = "Selecione o número de rodadas"
            return
        
        # Diz ao main app para iniciar a logica do jogo
        # Função que vai chamar o método start_game principal do app  
        # 'self.manager.parent' é uma forma de acessar a instancia proincipal do APP de uma tela

        app = App.get_running_app() 
        # Passa as seleções para a instancia main app
        app.chosen_category = self.selected_category
        app.num_rounds = self.selected_round

        app.start_game()        
        
    def go_back(self, instance):
        """
        Função que lida com o botão voltar
        """
        self.manager.current = 'setup'
