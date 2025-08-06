from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

# --- Tela de resultados finais --- #

class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.title_label = Label(text="Os resultados são...", font_size='50sp', bold=True)
        self.result_label = Label(text="", font_size='35sp', halign='center')
        # Cria dois botões separados para os dois estados.
        self.reveal_impostor_button = Button(text = 'Mostrar Impostor', font_size='45sp')
        self.reveal_impostor_button.bind(on_press=self.show_final_results)
        # Botão deJogar novamente
        self.play_again_button = Button(text="Jogar Novamente", font_size='45sp')
        self.play_again_button.bind(on_press=self.play_again)
        
        self.main_layout.add_widget(self.title_label)
        self.main_layout.add_widget(self.result_label)
        self.main_layout.add_widget(self.play_again_button)
        self.add_widget(self.main_layout)
        
    def on_enter(self):
        """
        Esse método contem a lógica que é usada para estar no on_enter.
        """
        Clock.schedule_once(self.setup_screen)
        
    def setup_screen(self, dt):
        """
        Método que lida com reveal state inicial.
        """
        app = App.get_running_app()
        
        # Cria o texto de resultado()
        result_text = f"O mais votado foi: \n\n[b]{app.most_voted_name}[/b]\n\n"
        self.result_label.text = result_text
        self.result_label.markup = True
        
        # Garante que o layout esta no estado correto para iniciar a revelação
        if self.play_again_button.parent:
            self.main_layout.remove_widget(self.play_again_button)
        if not self.reveal_impostor_button.parent:
            self.main_layout.add_widget(self.reveal_impostor_button)
        # Remove qualquer botão que possa esta alí vindo do jogo anterior
    def show_final_results(self, instance):
        """
        Esse método lida com o estado final de revelação
        """    
        app = App.get_running_app()
        
        result_text = f"Mas na verdado, o impostor era: \n\n[b]{app.impostor_name}[/b]\n\n"
        
        # Determina o vencedor
        if app.most_voted_name == app.impostor_name:
            result_text += "Os jogadores venceram!"
        else:
            result_text += "O impostor venceu!"
            
        self.result_label.text = result_text

        self.main_layout.remove_widget(self.reveal_impostor_button)
        self.main_layout.add_widget(self.play_again_button)
        
    def play_again(self, instance):
        App.get_running_app().restart_game()