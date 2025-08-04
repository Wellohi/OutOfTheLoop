from kivy.app import App
from kivy.uix.boxlayout import BoxLayout    # The layout to arrange widgets
from kivy.uix.label import Label            # For displaying text
from kivy.uix.button import Button          # For buttons
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

# --- Tela de revelação --- #        

class RevealScreen(Screen):
    def __init__(self, **kwargs):
        super(RevealScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        # Esses são os widgets que vão ser mostrados e escondidos
        self.info_label = Label(text="", font_size='24sp', halign='center')
        # Cria dois botões separados
        self.action_button = Button(text="Toque para Revelar", font_size='20sp')
        self.action_button.bind(on_press=self.handle_action)
        
        self.layout.add_widget(self.info_label)
        self.layout.add_widget(self.action_button)
        
        self.add_widget(self.layout)
        # É preciso manter o estado do jogador atual e o game_state
        self.game_sate = None
        self.current_player_index = 0
        self.word_is_hidden = True
        self.reveal_phase_complete = False
    
    # Esse método é chamado pelo Kiby quando trocamos para essa tela
    def on_enter(self):
        """
        Esse método agenda o setup screen para rodar no próximo frame.
        Isso previne a tela dar folickering com contexyo anteriores durante a transição.
        O argumento 'dt' é requirido pelo Clock, mas não é usado.
        """
        Clock.schedule_once(self.setup_screen)
        
        
    def setup_screen(self,dt):
        """
        Esse método contem toda a logica que é usada para no on_enter.
        """
        # Pega o game_state da instância do app principal
        self.game_state = App.get_running_app().game_state
        self.current_player_index = 0
        self.word_is_hidden = True
        self.reveal_phase_complete = False
        
        self.update_display_for_next_player()
            
    def update_display_for_next_player(self):
        player_name = self.game_state[self.current_player_index]['name']
        self.info_label.text = f"Jogador {player_name}, sua vez. \n\n Passe o celular para ele."
        self.action_button.text = "Toque para Revelar"
        self.word_is_hidden = True
        
    def handle_action(self, instance):
        """
        Essa função lida com todas as açoes para essa tela, checando o estado da flag 'reveal_phase_complete'
        """
        if self.reveal_phase_complete:
            self.manager.current = 'question'
            return
        
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
                self.action_button.text = "Iniciar Rodada de Perguntas"
                self.reveal_phase_complete = True
                # self.layout.remove_widget(self.action_button) # Desvincula a função antiga
                # self.layout.add_widget(self.go_to_voting_button) # Vincula a nova função
                
    # def go_to_voting(self, instance):
    #     # função para trocar para tela de votação
    #     self.manager.current = 'voting'
