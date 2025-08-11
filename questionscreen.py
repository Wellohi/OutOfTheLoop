from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget # Import the generic Widget for spacing
from kivy.clock import Clock
import random

# --- Tela para gerenciar rodadas de perguntas --- #
class QuestionScreen(Screen):
    def __init__(self, **kwargs):
        super(QuestionScreen,self).__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.round_label = Label(text="", font_size='25sp')
        self.asker_label = Label(text="", font_size='30sp', bold=True)
        self.answerer_label = Label(text="", font_size='30sp', bold=True)
        self.question_label = Label(
            text="",
            font_size='25sp',
            halign='center',
            valign='middle'
            )
        
        self.question_label.bind(size=self.question_label.setter('text_size'))       
        
        navigation_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height=100) 
        
        self.back_button = Button(text='Pergunta Anterior', font_size='25sp', disabled=True)
        self.back_button.bind(on_press=self.previous_question)
        
        self.next_button = Button(text='Próxima Pergunta', font_size='25sp')
        self.next_button.bind(on_press=self.next_question)
        
        navigation_layout.add_widget(self.back_button)
        navigation_layout.add_widget(self.next_button)
                
        self.main_layout.add_widget(self.round_label)
        self.main_layout.add_widget(self.asker_label)
        self.main_layout.add_widget(Label(text='Pergunta para', font_size='25sp'))
        self.main_layout.add_widget(self.answerer_label)
        self.main_layout.add_widget(self.question_label)
        
        self.main_layout.add_widget(Widget()) 
        
        self.main_layout.add_widget(navigation_layout)
        
        self.main_layout.add_widget(Widget(size_hint_y=None, height=20))
        
        self.add_widget(self.main_layout)
        
        # Estado de rastrear variáveis
        self.question_pairs = []
        self.current_pair_index = 0
        self.local_question_deck = []
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
        
        self.local_question_deck = app.question_deck.copy()
        
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
        
        question_index = self.current_pair_index % len(self.local_question_deck)
        next_question = self.local_question_deck[question_index]
        self.question_label.text = f"'{next_question}'"
        
        self.back_button.disabled = (self.current_pair_index == 0)
                    
        # Muda o botão texto na ultima pergunta
        if self.current_pair_index == len(self.question_pairs) -1:
            self.next_button.text = "Ir Para Votação"
        else: 
            self.next_button.text = "Próxima Pergunta"
            
    def previous_question(self, instance):
        """
        Volta uma pergunta
        """
        if self.current_pair_index > 0:
            self.current_pair_index -= 1
            self.display_current_question()
            
    def next_question(self,instance):
        """
        Muda para a próxima pergunta ou transiciona para a tela de votação
        """
        self.current_pair_index += 1
        
        if self.current_pair_index < len(self.question_pairs):
            self.display_current_question()
        else:
            self.manager.current = 'voting'