from kivy.app import App
from kivy.uix.boxlayout import BoxLayout    # The layout to arrange widgets
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label            # For displaying text
from kivy.uix.textinput import TextInput    # For user text input
from kivy.uix.button import Button          # For buttons
from kivy.uix.spinner import Spinner        # For dropdown-style selection
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

# --- Import da Logica do Jogo --- #
# Importa-se a função setup_game e a lista de palabras do arquivo app.py
# Garanta que o app.py esteja na mesma pasta que esse arquivo

from game_logic import setup_game, game_words

# ---  Tela de configurração --- #
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
        players_label = Label(text="Digite o nome dos jogadores (Separado por vírgula): ")
        # Armazena o próximo input em 'self_players_input' para acessar o valor depois
        self.names_input = TextInput(multiline=False)
        # Um label e um spinner para escolher a categoria
        category_label = Label(text="Escolha uma Categoria: ")
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
        main_layout.add_widget(players_label)
        main_layout.add_widget(self.names_input)
        main_layout.add_widget(category_label)
        main_layout.add_widget(self.categoria_spinner)
        main_layout.add_widget(start_button)
        main_layout.add_widget(self.status_label)
        # Finalmente, adicionar o layout a screen 
        self.add_widget(main_layout)
        
    def start_game_button_pressed(self, instance):
        # Função que vai chamar o método start_game principal do app  
        # 'self.manager.parent' é uma forma de acessar a instancia proincipal do APP de uma tela
        App.get_running_app().start_game()
        
# --- Tela de revelação --- #        
class RevealScreen(Screen):
    def __init__(self, **kwargs):
        super(RevealScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        # Esses são os widgets que vão ser mostrados e escondidos
        self.info_label = Label(text="", font_size='24sp', halign='center')
        self.action_button = Button(text="Toque para Revelar", font_size='20sp')
        self.action_button.bind(on_press=self.handle_action)
        self.layout.add_widget(self.info_label)
        self.layout.add_widget(self.action_button)
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
        self.action_button.disabled = False
        # Reseta o botão para seu estado inicial toda vez que a tela é exibida
        # Remove a vinculação com a função 'go_to_voting' (a partir da segunda rodada de jogo)
        self.action_button.unbind(on_press=self.go_to_voting)
        # Garente que a vinculação correta em 'handle_action' esteja ativa
        self.action_button.bind(on_press=self.handle_action)
        # Seta a tela para o primeiro jogador
        self.update_display_for_next_player()
        
    def update_display_for_next_player(self):
        player_name = self.game_state[self.current_player_index]['name']
        self.info_label.text = f"Jogador {player_name}, sua vez. \n\n Passe o celular para ele."
        self.action_button.text = "Toque para Revelar"
        self.word_is_hidden = True
        
    def handle_action(self, instance):
        if self.word_is_hidden:
            # Revela a palavra
            player_data = self.game_state[self.current_player_index]
            self.info_label.text = f"A palavra é: \n\n[b]{player_data['palavra']}[/b]"
            self.info_label.markup = True # Diz ao label para processar as tags
            self.action_button.text = "Aperte para esconder"
            self.word_is_hidden = False
        else:
            # Esconde a palavra e muda para o próximo jogador
            self.info_label.narkup = False # Desativa o markup para texto normal
            self.current_player_index += 1
            if self.current_player_index < len(self.game_state):
                # Há mais jogadores
                self.update_display_for_next_player()
            else:
                # Todos jogadores viram a palavra
                self.info_label.text = "Todos jogadores viram a palavra!\n\n Que começe a rodada de perguntas"
                # Botão para levar a tela de votação
                self.action_button.text = "Ir para a Votação"
                self.action_button.unbind(on_press=self.handle_action) # Desvincula a função antiga
                self.action_button.bind(on_press=self.go_to_voting) # Vincula a nova função
                
    def go_to_voting(self, instance):
        # função para trocar para tela de votação
        self.manager.current = 'voting'

# -- TELA DE VOTAÇÃO --- #
class VotingScreen(Screen):
    def __init__(self, **kwargs):
        super(VotingScreen, self).__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
    
        self.title_label = Label(text='Quem é o impostor?', font_size='24sp', bold=True)
        self.buttons_grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        self.result_label = Label(text='', font_size='20sp')
        self.play_again_button = Button(text='Jogar Novamente', font_size='20sp')
        self.play_again_button.bind(on_press=self.play_again)
        
        self.main_layout.add_widget(self.title_label)
        self.main_layout.add_widget(self.buttons_grid)
        self.main_layout.add_widget(self.result_label)
        self.main_layout.add_widget(self.play_again_button)
        self.add_widget(self.main_layout)
        self.game_state = None # Armazena o estado do jogo para uso dos métodos
        
    def on_enter(self):
        """
        Este método pe chamado quando a tela aparece. É aqui que os botões são criados. 
        """
        self.buttons_grid.clear_widgets() # Limpa os botões de jogos anteriores
        self.result_label.text = "" # limpa o resultado anterior.
        # Armazena o estado do jogo na instância da tela
        self.game_state = App.get_running_app().game_state
        
        # Loop para criar um botão para cada jogador
        for player in self.game_state:
            player_name = player['name']
            btn = Button(text=f"Jogador {player_name}", font_size='18sp')
            # 'lambda' permite passar o jogador específico para a função de voto
            btn.bind(on_press=lambda instance, p=player: self.cast_vote(p))
            self.buttons_grid.add_widget(btn)
            
    def cast_vote(self, player_data):
        """
        Chamado quando um botão de jogadore é pressionado
        """
        self.buttons_grid.clear_widgets() #remove botões de voto
        
        role = player_data['papel']
        player_name = player_data['name']
        
        if role == 'Impostor':
            self.result_label.text = f"Jogador {player_name} é o impostor! \n\n Os jogadores venceram!"
        else:
            impostor_id = None
            for player in self.game_state:
                if player['papel'] == 'Impostor':
                    impostor_id = player['name']
                    break # Encontrou o impostor, pode parar o loop
                
            self.result_label.text = f"Jogador {player_name} não era o impostor! \n\n O impostor era o Jogador {impostor_id}"
            
    def play_again(self, instance):
        App.get_running_app().restart_game()
        
        
# Criar a aplicação principal
# Todas aplicações Kivy são construidas a partir de uma classe que herda da "Kivy's App class".
class ForaDaRodada(App):
    # Define o método build
    # Esse método é automaticamente chamado pelo kivy quando o app inicia.
    # Deve retornar a 'aplicação raiz' da aplicação, a qual é o conteiner principal para todos os outros elementos de USER INTERFACE (UI)
    def build(self):
        
        self.sm = ScreenManager(transition=FadeTransition())
        # Cria instancia para as telas
        self.setup_screen = SetupScreen(name='setup')
        self.reveal_screen = RevealScreen(name='reveal')
        self.voting_screen = VotingScreen(name='voting')
        # Adiciona as telas ao gerenciador
        self.sm.add_widget(self.setup_screen)
        self.sm.add_widget(self.reveal_screen)
        self.sm.add_widget(self.voting_screen)
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
            # Logica para separar nomes por vírgula
            names_text = self.setup_screen.names_input.text
            # Separa por virgula e remove espaços dos nomes
            player_names = [name.strip() for name in names_text.split(',') if name.strip()]
            
            # Validação é baseada no número de nomes inseridos
            if len(player_names) < 3:
                self.setup_screen.status_label.text = 'O jogo requer no mínimo 3 jogadores'
                return
            
            chosen_category = self.setup_screen.categoria_spinner.text
            # Pode-se chamar agora a função setup_game original
            self.game_state = setup_game(player_names, chosen_category)
            
            if self.game_state:
                print('\n --- Jogo Iniciado! Trocando de tela... ---')
                # Diz ao gerenciador de telas para trocar para tela de revelação
                self.sm.current = 'reveal'

        except Exception as e:
            self.setup_screen.status_label.text = 'Um erro ocorreu. Por Favor, cheque os nomes.'
            print(f'Erro ao iniciar jogo: {e}')
                        
    def restart_game(self):
        # Função para reiniciar jogo
        self.game_state = None
        self.sm.current = 'setup'
        self.setup_screen.players_input.text = ""
        self.setup_screen.status_label.text = ""
            
# Rodar a aplicação                
if __name__ == '__main__':
    ForaDaRodada().run()
