from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget

# --- Tela de título --- #
class TitleScreen(Screen):
    def __init__(self, **kwargs):
        super(TitleScreen, self).__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Um layout simples para mostrar o titulo fo jogo
        title_label = Label(text="Out of the Loop", font_size='50sp', bold=True)
        start_button = Button(text='Iniciar Jogo', font_size='40sp', size_hint=(1, None), height=100)
        start_button.bind(on_press=self.go_to_setup)
        
        # Usa espaços flexiveis para centralizar o título
        main_layout.add_widget(Widget())
        main_layout.add_widget(title_label)
        main_layout.add_widget(Widget())
        main_layout.add_widget(start_button)
        
        self.add_widget(main_layout)
        
    def go_to_setup(self, instance):
        """
        Troca para a tela de adicionar jogadores
        """
        self.manager.current = 'setup'