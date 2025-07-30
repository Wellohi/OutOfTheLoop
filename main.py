from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition

# --- Import da Logica do Jogo --- #
# Importa-se a função setup_game e a lista de palabras do arquivo app.py
# Garanta que o app.py esteja na mesma pasta que esse arquivo

from game_logic import setup_game, game_words
# Importa as telas do aplicativo de seus respectivos arquivos
from setupscreen import SetupScreen
from revealscreen import RevealScreen
from votingscreen import VotingScreen

        
# --- Classe Principal do App --- #
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
            # Pega os nomes da lista de widgets input
            name_widgets = self.setup_screen.name_inputs
            # Vai para o próximo para cada widget, removerndo caracteres desnecessários no começo e fim (stripping)
            player_names = [widget.text.strip() for widget in name_widgets]
            
            # Validação é baseada checando caixas de nome vazias
            if any(not name for name in player_names):
                self.setup_screen.status_label.text = 'Pelo menos 3 caixas de jogador devem ser preenchidas.'
                return
            
            if len(player_names) < 3:
                self.setup_screen.status_label.text = 'O jogo requer no mínimo 3 jogadores.'
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
        # É necessário limpar e recriar os inputs para o próximo jogo
        setup_screen = self.sm.get_screen('setup')
        setup_screen.names_layout.clear_widgets()      
        setup_screen.name_inputs.clear()      
        for i in range(3):
            setup_screen.add_player_input()
        self.setup_screen.status_label.text = ""
            
# Rodar a aplicação                
if __name__ == '__main__':
    ForaDaRodada().run()
