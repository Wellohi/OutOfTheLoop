from kivy.app import App
from kivy.uix.boxlayout import BoxLayout    # The layout to arrange widgets
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label            # For displaying text
from kivy.uix.button import Button          # For buttons
from kivy.uix.screenmanager import Screen

# --- Import da Logica do Jogo --- #
# Importa-se a função setup_game e a lista de palabras do arquivo app.py
# Garanta que o app.py esteja na mesma pasta que esse arquivo

from game_logic import setup_game, game_words

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
    