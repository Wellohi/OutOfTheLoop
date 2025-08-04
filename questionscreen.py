from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
import random

# --- Tela para gerenciar rodadas de perguntas --- #
class QuestionScreen(Screen):
    def __init__(self, **kwargs):
        super(QuestionScreen,self).__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.round_label = Label(text="", font_size='20sp')
        self.asker_label = Label(text="", font_size='24sp', bold=True)
        self.answerer_label = Label(text="", font_size='24sp', bold=True)
        self.question_label = Label(text="", font_size='22sp', halign='center')
        
        self.next_button = Button(text='Próxima Pergunta', font_size='20sp')
        self.next_button.bind(on_press=self.next_question)
        
        self.main_layout.add_widget(self.round_label)
        self.main_layout.add_widget(self.asker_label)
        self.main_layout.add_widget(Label(text='Pergunta para', font_size='24sp'))
        self.main_layout.add_widget(self.answerer_label)
        self.main_layout.add_widget(self.question_label)
        self.main_layout.add_widget(self.next_button)
        
        self.add_widget(self.main_layout)
        
        # Estado de rastrear variáveis
        self.question_pairs = []
        self.current_pair_index = 0
        self.questions_for_category = []
        self.chosen_category = ''
        
    def on_enter(self):
        """
        Agenda a screen setup para rodar no próximo frame.
        """
        Clock.schedule_once(self.setup_screen)
        
    def setup_screen(self, dt):
        """
        Seta a tela para a primeira pergunta
        """
        app = App.get_running_app()
        self.question_pairs = app.question_pairs
        self.chosen_category = app.chosen_category
        self.questions_for_category = app.game_questions[self.chosen_category]
        
        self.current_pair_index = 0
        self.display_current_question()
        
    def display_current_question(self):
        """
        Atualiza as labels com a pergunta atual e jogadores
        """
        
        # Calcula a rodada atual e o número de perguntas
        num_players = len(App.get_running_app().player_names)
        current_round = (self.current_pair_index // num_players) + 1
        
        self.round_label.text = f"Rodada {current_round} de {App.get_running_app().num_rounds}"
        
        # Pega o número atual de jogadores
        current_pair = self.question_pairs[self.current_pair_index]
        asker = current_pair['asker']
        answerer = current_pair['answerer']
        
        self.asker_label.text = asker
        self.answerer_label.text = answerer
        
        # Pega uma pergunta aleatória
        self.question_label.text = f"'{random.choice(self.questions_for_category)}'"
        
        # Muda o botão texto na ultima pergunta
        if self.current_pair_index == len(self.question_pairs) -1:
            self.next_button.text = "Ir Para Votação"
        else: 
            self.next_button.text = "Próxima Pergunta"
            
    def next_question(self,instance):
        """
        Muda para a próxima pergunta ou transiciona para a tela de votação
        """
        self.current_pair_index += 1
        
        if self.current_pair_index < len(self.question_pairs):
            self.display_current_question()
        else:
            self.manager.current = 'voting'