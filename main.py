from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
# from kivy.clock import Clock
import random
# Importa as telas do aplicativo de seus respectivos arquivos
from setupscreen import SetupScreen
from revealscreen import RevealScreen
from votingscreen import VotingScreen
from categoryscreen import CategoryScreen
from resultsscreen import ResultsScreen
from questionscreen import QuestionScreen
from loadingscreen import LoadingScreen

# --- Import da Logica do Jogo --- #
# Importa-se a função setup_game e a lista de palabras do arquivo app.py
# Garanta que o app.py esteja na mesma pasta que esse arquivo

from game_logic import setup_game
from categories import game_words
from questions import game_questions

        
# --- Classe Principal do App --- #
# Todas aplicações Kivy são construidas a partir de uma classe que herda da "Kivy's App class".
class OutOfTheLoopApp(App):
        # Define o método build
    # Esse método é automaticamente chamado pelo kivy quando o app inicia.
    # Deve retornar a 'aplicação raiz' da aplicação, a qual é o conteiner principal para todos os outros elementos de USER INTERFACE (UI)
    def build(self):
        # Armazena as palavras no app instance para que outras partes possam acessala
        self.game_words = game_words
        self.game_questions = game_questions
        self.sm = ScreenManager(transition=FadeTransition())
        # Cria instancia para as telas
        self.setup_screen = SetupScreen(name='setup')
        self.category_screen = CategoryScreen(name='category')
        self.reveal_screen = RevealScreen(name='reveal')
        self.question_screen = QuestionScreen(name='question')
        self.voting_screen = VotingScreen(name='voting')
        self.results_screen = ResultsScreen(name='results')
        self.loading_screen = LoadingScreen(name='loading')
        
        # Adiciona as telas ao gerenciador
        self.sm.add_widget(self.setup_screen)
        self.sm.add_widget(self.category_screen)
        self.sm.add_widget(self.reveal_screen)
        self.sm.add_widget(self.question_screen)
        self.sm.add_widget(self.voting_screen)
        self.sm.add_widget(self.results_screen)
        self.sm.add_widget(self.loading_screen)
        
        
        # Propriedade de manter o número de rounds
        self.num_rounds = 0
        self.chosen_category = None
        self.question_pairs = []
        
        # a aplicação vai manter o game_state central e manter os nomes entre telas
        self.game_state = None
        self.player_names = None
        self.most_voted_name = None
        self.impostor_name = None
        
        return self.sm
        
    # Essa função é chamada quando o start_button é pressionado
    def start_game(self):
        """
        Adiquire as configurações da UI, chama a lógica núcleo do jogo e troca para revelar tela.
        """        
        try:
            # Nome de jogadores agora são lidos do app property
            player_names = self.player_names
            # Categoria é lido da instancia category_screen
            chosen_category = self.chosen_category
            self.num_rounds = self.num_rounds
            
            self.game_state = setup_game(player_names, chosen_category)
            
            if self.game_state:
                self.generate_question_rounds()
                self.sm.current = 'reveal'
            else:
                # Esse case idealmente não deve ser ativado por conta da valiodação no SetupScreen,
                # Mas é uma boa prática ter um retorno
                self.setup_screen.status_label.text = "An error occurred. Please restart."
        except Exception as e:
            print(f'Erro ao iniciar jogo: {e}')
            
    def generate_question_rounds(self):
        """
        Cria a lista de quem pergunta para quem pelas rodadas
        """
        self.question_pairs = []
        players = self.player_names.copy()
        
        for _ in range(self.num_rounds):
            random.shuffle(players)
            # Cria a 'cadeia': p1 -> p2, p2 -> p3 ... até todos terem perguntado e respondido      
            for i in range(len(players)):
                asker = players[i]
                # Quem responde é o próximo da lista, envolvendo até o final
                answerer = players[(i + 1) % len(players)]
                self.question_pairs.append({'asker': asker, 'answerer': answerer})

              
    def calculate_and_show_results(self, votes):
        """
        Processa os votos e prepara o dado para a tela de resultado
        """
        # Encontra o jogador com mais votos
        self.most_voted_name = max(votes, key=votes.get)
        
        # Encontra o verdadeiro impostor
        for player in self.game_state:
            if player['papel'] == 'Impostor':
                self.impostor_name = player['name']
                break
            
        # Muda para a tela de resultados
        self.sm.current = 'results'
        
                        
    def restart_game(self):
        """
        Reinicia o jogo e retorna a tela inicial
        """
        self.game_state = None
        self.player_names = None
        self.most_voted_name = None
        self.impostor_name = None
        self.num_rounds = 0 # Reseta o número de rounds
        self.chosen_category = None
        self.question_pairs = []
        
        self.setup_screen.names_layout.clear_widgets()
        self.setup_screen.name_inputs.clear()
        for i in range(3):
            self.setup_screen.add_player_input()
        self.setup_screen.status_label.text = ""
        
        # Clock.schedule_once(self.switch_to_setup, 0)

        self.sm.current = 'setup'

                           
    # def switch_to_setup(self, dt):
    #     """This helper function is called by the Clock to perform the screen switch."""
    #     self.sm.current = 'setup'
                 
# Rodar a aplicação                
if __name__ == '__main__':
    OutOfTheLoopApp().run()
