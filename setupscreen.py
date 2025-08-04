from kivy.app import App
from kivy.uix.boxlayout import BoxLayout    # The layout to arrange widgets
from kivy.uix.label import Label            # For displaying text
from kivy.uix.textinput import TextInput    # For user text input
from kivy.uix.button import Button          # For buttons
from kivy.uix.scrollview import ScrollView  # To allow scrolling 
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window   
# from kivy.clock import Clock

# --- Import da Logica do Jogo --- #
# Importa-se a função setup_game e a lista de palabras do arquivo app.py
# Garanta que o app.py esteja na mesma pasta que esse arquivo


# ---  Tela de configurração --- #
# Transformando o layout em uma classe Screen aprorpriada
     
class SetupScreen(Screen):
    # O 'self' em __init__ referencia a instância SetupScreen
    # O **kwargs é importante para capturar todos os outros Kivy argumentos
    def __init__(self, **kwargs):
        # Deve-se chamar o método pai do __init__
        super(SetupScreen, self).__init__(**kwargs)
        # Isso faz a janela se adaptar quando o teclado aparecer
        Window.softinput_mode = 'below_target'
        # O layout principal vai manter todas as widgets
        # Uma BoxLayout vertical, então o widgets são adicionados de cima para baixo
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        # Criar as widgets necessárias
        # Título da label
        title_label = Label(text="Digite o nome dos jogadores", font_size='24sp', bold=True, size_hint_y=None, height=40)
        # --- Sessão Name Input Dinãmico --- #
        # Um ScrollView é necessário caso haja muitos jogadores adicionados
        scroll_view = ScrollView(size_hint=(1,1))
        # Esse layout vai conter os TextInputs e vai se colocado dentro do ScrollView
        self.names_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        # Essa linha é importante: Faz com que o layout cresça verticalmente enquanto as widgets são adicionadas
        self.names_layout.bind(minimum_height=self.names_layout.setter('height'))
        scroll_view.add_widget(self.names_layout)
        # Essa lista vai armazenar o objeto TextInput widget atual
        self.name_inputs = []
        # --- Botões Adicionar / Remover caixas --- #
        button_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        add_button = Button(text='Adicionar Jogador')
        add_button.bind(on_press=self.add_player_input)
        self.remove_button = Button(text='Remover Jogador', disabled=True) # Inicia desabilitado
        self.remove_button.bind(on_press=self.remove_player_input)
        button_layout.add_widget(add_button)
        button_layout.add_widget(self.remove_button)
        # --- Seleção de Categoria --- #
        # Um label e um spinner para escolher a categoria
        continue_button = Button(text="Continuar", font_size='20sp', size_hint_y=None, height=50)
        continue_button.bind(on_press=self.proceed_to_category)
        self.status_label = Label(text="", color=(1, 0, 0, 1), font_size='16sp', size_hint_y=None, height=30)
        # Adicionar os widgets ao layout na ordem que queremos que apareça
        main_layout.add_widget(title_label)
        main_layout.add_widget(scroll_view)
        main_layout.add_widget(button_layout)
        main_layout.add_widget(continue_button)
        main_layout.add_widget(self.status_label)
        # Finalmente, adicionar o layout a screen 
        self.add_widget(main_layout)
        
        for i in range(3):
            self.add_player_input()
        
    # def on_enter(self):
    #     """
    #     Agenda a screen setup para rodar no próximo frame.
    #     """
    #     Clock.schedule_once(self.reset_screen)
        
    # def reset_screen(self, dt):
    #     """
    #     Reseta a tela para o padrão para não ter probema de race condition
    #     """
    #     # É necessário limpar e recriar os inputs para o próximo jogo
    #     self.names_layout.clear_widgets()
    #     self.name_inputs.clear()
    #     for i in range(3):
    #         self.add_player_input()
    #     self.status_label.text = ""
    
    # def on_pre_enter(self, *args):
    #     """
    #     Esse método é chamado antes da tela transicionar. 
    #     """
    #     self.names_layout.clear_widgets()
    #     self.name_inputs.clear()
    #     for i in range(3):
    #         self.add_player_input()
    #     self.status_label.text=""
        
    def add_player_input(self, instance=None):
        """
        Cria um novo TextInput para cada nome de jogador e adiciona na tela
        """
        if len(self.name_inputs) < 9: # Adiciona um limite máximo de jogadores
            new_input = TextInput(hint_text=f"Player {len(self.name_inputs) + 1}", size_hint_y=None, height=40)
            self.names_layout.add_widget(new_input)
            self.name_inputs.append(new_input)
            # Habilita o botão remover se houer mais de 3 jogadores
            self.remove_button.disabled = len(self.name_inputs) <= 3
            
    def remove_player_input(self, instance=None):
        """
        Remove o ultimo TextInput de jogador da tela
        """
        if len(self.name_inputs) > 3:
            input_to_remove = self.name_inputs.pop()
            self.names_layout.remove_widget(input_to_remove)
            # Desabilita o botão de remover se tivermos o mínimo de 3
            self.remove_button.disabled = len(self.name_inputs) <= 3
            
    def proceed_to_category(self, instance):
        """
        Valida nomes, salva eles no app e troca de tela
        """
        self.status_label.text = ""        
        player_names = [widget.text.strip() for widget in self.name_inputs]
        
        if any(not name for name in player_names):
            self.status_label.text = "Ao menos 3 jogadores devem ser adicionados"
            return     
    
        app = App.get_running_app()
        app.player_names = player_names
        
        # Mudar para próxima tela
        self.manager.current = 'category'
   