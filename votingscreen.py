from kivy.app import App
from kivy.uix.boxlayout import BoxLayout    # The layout to arrange widgets
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label            # For displaying text
from kivy.uix.button import Button          # For buttons
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

# -- TELA DE VOTAÇÃO --- #
class VotingScreen(Screen):
    def __init__(self, **kwargs):
        super(VotingScreen, self).__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
    
        self.title_label = Label(
            text='',
            font_size='25sp',
            halign='center',
            valign='middle',
            bold=True
            )
        self.title_label.bind(size=self.title_label.setter('text_size')) 
            
        self.buttons_grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
                
        self.main_layout.add_widget(self.title_label)
        self.main_layout.add_widget(self.buttons_grid)
        self.add_widget(self.main_layout)
        
        # Rastreamento do processo de votação
        self.game_state = None # Armazena o estado do jogo para uso dos métodos
        self.player_names = None
        self.current_voter_index = 0
        self.votes = {}
        
    def on_enter(self):
        """
        Agenda a tela setup para rodar no próximo frame, prevenindo flicker. 
        """
        Clock.schedule_once(self.setup_screen)
        
    def setup_screen(self,dt):
        """
        Esse método contem a lógica que é usada para estar no on_enter.
        """
        app = App.get_running_app()
        # Armazena o estado do jogo na instância da tela
        self.game_state = app.game_state
        self.player_names = app.player_names
        
        # Reseta o voting state para a nova rodada
        self.current_voter_index = 0
        self.votes = {name: 0 for name in self.player_names}
        
        self.update_for_next_voter()
                
    def update_for_next_voter(self):
        """
        Atualiza a tela para mostrar de quem é a vez de votar
        """
        self.buttons_grid.clear_widgets()

        voter_name = self.player_names[self.current_voter_index]
        self.title_label.text = f"{voter_name}, quem você acha que é o impostor?"
        
        # Cria um botão para cada jogar que pode ser votado
        for player in self.game_state:
            # Um jogador não pode votar em sí mesmo
            if player['name'] != voter_name:
                btn = Button(text=player['name'], font_size='40sp')
                btn.bind(on_press=lambda instance, p=player: self.cast_vote(p))
                self.buttons_grid.add_widget(btn)
                
    def cast_vote(self, voted_player_data):
        """
        Grava o voto e move para o próximo jogador ou finaliza a votação
        """
        voted_name = voted_player_data['name']
        self.votes[voted_name] += 1
        
        self.current_voter_index += 1
    
        if self.current_voter_index < len(self.player_names):
            # Se houver mais votos, atualiza a tela para o próximo voto
            self.update_for_next_voter()
        else:
            # Se não houver mais votantes, diz ao main app para calcular os resultados
            App.get_running_app().calculate_and_show_results(self.votes)
    
