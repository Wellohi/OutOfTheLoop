from kivy.app import App
from kivy.uix.boxlayout import BoxLayout    # The layout to arrange widgets
from kivy.uix.label import Label            # For displaying text
from kivy.uix.textinput import TextInput    # For user text input
from kivy.uix.button import Button          # For buttons
from kivy.uix.spinner import Spinner        # For dropdown-style selection
from kivy.uix.screenmanager import ScreenManager, Screen

# --- Import da Logica do Jogo --- #
# Importa-se a função setup_game e a lista de palabras do arquivo app.py
# Garanta que o app.py esteja na mesma pasta que esse arquivo

from game_logic import setup_game, game_words

# --- Tela 1: Tela de configurração --- #
# Transformando o layout em uma classe Screen aprorpriada
class SetupScreen(Screen):
    # O 'self' em __init__ referencia a instância SetupScreen
    # O **kwargs é importante para capturar todos os outros Kivy argumentos
    def __init__(self, **kwargs):
        # Deve-se chamar o método pai do __init__
        super(SetupScreen, self).__init__(**kwargs)

        # O layout principal vai manter todas as widgets
        # Uma BoxLayout vertical, então o widgets são adicionados de cima para baixo
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        # Criar as widgets necessárias
        # Título da label
        titulo_label = Label(text="Fora da Rodada", font_size='24sp', bold=True)
        # A label e o input do texto para o número de jogadores
        jogadores_label = Label(text="Número de Jogadores: ")
        # Armazena o próximo input em 'self_players_input' para acessar o valor depois
        self.players_input = TextInput(multiline=False, input_filter='int')
        # Um label e um spinner para escolher a categoria
        categoria_label = Label(text="Escolha uma Categoria: ")
        # O spinner mostra o valor padrão e permite escolher da lista;
        # Pegamos esse nome da categoria diretamente da importação do dicionário 'game_words'
        self.categoria_spinner = Spinner(
            text=list(game_words.keys())[0],
            values=list(game_words.keys())
        )
    
        # Botão para iniciar o jogo
        start_button = Button(text='Iniciar Jogo', font_size='20sp')
        
        # Essa é a chave: 'vincular' os botões em evento 'on_press' para o método self.start_game 
        # Quando o botão é pressionado,Kivy vai automaticamente chamar essa função
        start_button.bind(on_press=self.start_game_button_pressed)
        
        # Label para mostrar mensagens de erro ao usuário.
        self.status_label = Label(text="", color=(1, 0, 0, 1), font_size='16sp') # Texto em vermelho

        
        # Adicionar os widgets ao layout na ordem que queremos que apareça
        main_layout.add_widget(titulo_label)
        main_layout.add_widget(jogadores_label)
        main_layout.add_widget(self.players_input)
        main_layout.add_widget(categoria_label)
        main_layout.add_widget(self.categoria_spinner)
        main_layout.add_widget(start_button)
        main_layout.add_widget(self.status_label)
        
        # Finalmente, adicionar o layout a screen 
        self.add_widget(main_layout)
        
    def start_game_button_pressed(self, instance):
        # Função que vai chamar o método start_game principal do app  
        # 'self.manager.parent' é uma forma de acessar a instancia proincipal do APP de uma tela
        App.get_running_app().start_game()
        
# --- Tela 2: Tela de revelação --- #        
class RevealScreen(Screen):
    def __init__(self, **kwargs):
        super(RevealScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # Esses são os widgets que vão ser mostrados e escondidos
        self.info_label = Label(text="", font_size='24sp', halign='center')
        self.reveal_button = Button(text="Toque para Revelar", font_size='20sp')
        self.reveal_button.bind(on_press=self.reveal_word)
        
        self.layout.add_widget(self.info_label)
        self.layout.add_widget(self.reveal_button)
        self.add_widget(self.layout)
        
        # É preciso manter o estado do jogador atual e o game_state
        self.game_sate = None
        self.current_player_index = 0
        self.word_is_hidden = True
    
    # Esse método é chamado pelo Kiby quando trocamos para essa tela
    def on_enter(self):
        # Pega o game_state da instância do app principal
        self.game_state = App.get_running_app().game_state
        self.current_player_index = 0
        self.word_is_hidden = True
        # Seta a tela para o primeiro jogador
        self.update_display_for_next_player()
        
    def update_display_for_next_player(self):
        player_id = self.game_state[self.current_player_index]['id_jogador']
        self.info_label.text = f"Jogador {player_id}, sua vez. \n\n Passe o celular para ele."
        self.reveal_button.text = "Toque para Revelar"
        self.word_is_hidden = True
        
    def reveal_word(self, instance):
        if self.word_is_hidden:
            # Revela a palavra
            player_data = self.game_state[self.current_player_index]
            self.info_label.text = f"A palavra é: \n\n[b]{player_data['palavra']}[/b]"
            self.reveal_button.text = "Aperte para esconder"
            self.word_is_hidden = False
        else:
            # Esconde a palavra e muda para o próximo jogador
            self.current_player_index +=1
            if self.current_player_index < len(self.game_state):
                # Há mais jogadores
                self.update_display_for_next_player()
            else:
                # Todos jogadores viram a palavra
                self.info_label.text = "Todos jogadores viram a palavra!\n\n Que começe a rodada de perguntas"
                self.reveal_button.text = "Iniciar Jogo"
                self.reveal_button.disabled = True 


# Criar a aplicação principal
# Todas aplicações Kivy são construidas a partir de uma classe que herda da "Kivy's App class".
class ForaDaRodada(App):
    # Define o método build
    # Esse método é automaticamente chamado pelo kivy quando o app inicia.
    # Deve retornar a 'aplicação raiz' da aplicação, a qual é o conteiner principal para todos os outros elementos de USER INTERFACE (UI)
    def build(self):
        
        self.sm = ScreenManager()
        
        # Cria instancia para as telas
        self.setup_screen = SetupScreen(name='setup')
        self.reveal_screen = RevealScreen(name='reveal')
        
        # Adiciona as telas ao gerenciador
        self.sm.add_widget(self.setup_screen)
        self.sm.add_widget(self.reveal_screen)
        
        # a aplicação vai manter o game_state central
        self.game_state = None

        return self.sm
        
    # Essa função é chamada quando o start_button é pressionado
    def start_game(self):
        """
        Adiquire as configurações da UI, chama a lógica núcleo do jogo e troca para revelar tela.
        """
        
        # Limpa mensagens de erro anteriores
        self.setup_screen.status_label.text = ""

        # Pega os valores do input widgets
        try:
            numero_jogadores = int(self.setup_screen.players_input.text)
            categoria_escolhida = self.setup_screen.categoria_spinner.text

            # Pode-se chamar agora a função setup_game original
            self.game_state = setup_game(numero_jogadores, game_words, categoria_escolhida)
            
            if self.game_state:
                print('\n --- Jogo Iniciado! Trocando de tela... ---')
                # Diz ao gerenciador de telas para trocar para tela de revelação
                self.sm.current = 'reveal'
                
            else: 
                self.setup_screen.status_label.text = 'O jogo reque pelo menos 3 jogadores.'
                                    
        except ValueError:
            print("Por favor, insira um número válido de jogadores.")    
            self.setup_screen.status_label.text = "Por favor, insira um número válido."  
            self.setup_screen.players_input.text = '' # Limpa o input de jogadores  
            
# Rodar a aplicação                
if __name__ == '__main__':
    ForaDaRodada().run()
