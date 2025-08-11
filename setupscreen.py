from kivy.app import App
from kivy.uix.boxlayout import BoxLayout    # The layout to arrange widgets
from kivy.uix.label import Label            # For displaying text
from kivy.uix.textinput import TextInput    # For user text input
from kivy.uix.button import Button          # For buttons
from kivy.uix.scrollview import ScrollView  # To allow scrolling 
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window   
# from kivy.clock import Clock

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
        main_layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        # Criar as widgets necessárias
        # Título da label
        title_label = Label(
            text="Digite o nome dos jogadores",
            font_size='30sp', 
            bold=True, 
            size_hint_y=None, 
            height=40,
            halign='center',
            valign='middle'
            )
        title_label.bind(size=title_label.setter('text_size'))
        
        # --- Sessão Name Input Dinãmico --- #
        # Um ScrollView é necessário caso haja muitos jogadores adicionados
        scroll_view = ScrollView(size_hint=(1,1))
        # Esse layout vai conter os TextInputs e vai se colocado dentro do ScrollView
        self.names_layout = BoxLayout(orientation='vertical', spacing=20, size_hint_y=None)
        # Essa linha é importante: Faz com que o layout cresça verticalmente enquanto as widgets são adicionadas
        self.names_layout.bind(minimum_height=self.names_layout.setter('height'))
        scroll_view.add_widget(self.names_layout)
        # Essa lista vai armazenar o objeto TextInput widget atual
        self.name_inputs = []
        # --- Botões Adicionar / Remover caixas --- #
        button_layout = BoxLayout(size_hint_y=None, height=100, spacing=50)
        
        
        add_button = Button(text='Adicionar Jogador', font_size='25sp', halign='center' ,valign='middle')
        add_button.bind(size=add_button.setter('text_size'))
        add_button.bind(on_press=self.add_player_input)
        
        self.remove_button = Button(text='Remover Jogador', disabled=True, font_size='25sp', halign='center' ,valign='middle') # Inicia desabilitado
        self.remove_button.bind(size=self.remove_button.setter('text_size'))
        self.remove_button.bind(on_press=self.remove_player_input)
        
        button_layout.add_widget(add_button)
        button_layout.add_widget(self.remove_button)
        
        navigation_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, spacing=50)
        
        back_button = Button(text='Voltar', font_size='40sp', halign='center' ,valign='middle')
        back_button.bind(size=back_button.setter('text_size'))
        back_button.bind(on_press=self.go_back)
        # --- Seleção de Categoria --- #
        # Um label e um spinner para escolher a categoria
        continue_button = Button(text="Continuar", font_size='40sp', halign='center' ,valign='middle')
        continue_button.bind(size=continue_button.setter('text_size'))
        continue_button.bind(on_press=self.proceed_to_category)
        
        navigation_layout.add_widget(back_button)
        navigation_layout.add_widget(continue_button)
        
        self.status_label = Label(
            text="", 
            color=(1, 0, 0, 1),
            font_size='16sp',
            size_hint_y=None, 
            height=50,
            halign='center',
            valign='middle'
            )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        
        # Adicionar os widgets ao layout na ordem que queremos que apareça
        main_layout.add_widget(title_label)
        main_layout.add_widget(scroll_view)
        main_layout.add_widget(button_layout)
        main_layout.add_widget(navigation_layout)
        main_layout.add_widget(self.status_label)
        # Finalmente, adicionar o layout a screen 
        self.add_widget(main_layout)
       
    def on_pre_enter(self, *args):
        """
        Esse método checa se o jogador já existe de um jogo anterior
        """
        self.names_layout.clear_widgets()
        self.name_inputs.clear()
        self.status_label.text = ""
        
        app = App.get_running_app()
        
        if app.player_names:
            for name in app.player_names:
                self.add_player_input(text_to_set=name)
        else:
            for i in range(3):
                self.add_player_input()
        
    def add_player_input(self, instance=None, text_to_set=""):
        """
        Cria um novo TextInput para cada nome de jogador e adiciona na tela
        """
        if len(self.name_inputs) < 10: # Adiciona um limite máximo de jogadores
            new_input = TextInput(
                text=text_to_set,
                hint_text=f"Jogador {len(self.name_inputs) + 1}",
                size_hint_y=None,
                height=200,
                font_size='40sp'         
            )
            
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
            self.status_label.text = "Todas caixas deves ser preenchidas"
            return     
    
        app = App.get_running_app()
        app.player_names = player_names
        # Mudar para próxima tela
        self.manager.current = 'category'
   
    def go_back(self, instance):
       """
       Essa função liga com o botão voltar
       """
       self.manager.current = "title"