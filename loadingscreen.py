#from  loadingscreen.py
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

class LoadingScreen(Screen):
    """
    Uma simples tela preta, por enquanto, para atuar como um buffer entre transições
    Apenas espera um frame e então troca para a tela real
    """
    def on_enter(self, *args):
        """
        É chamado quando a tela se torna visível
        É imediatamente agendado o switch para o verdadeiro setup screen 
        """
        Clock.schedule_once(self.switch_to_title, 0)
        
    def switch_to_setup(self,dt):
        """
        Muda o screen manager, para o setup screen
        """        
        self.manager.current = 'title'

    
    