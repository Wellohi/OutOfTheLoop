import random


# uma lista de palavras para testar o jogo
game_words = {
    "Animal": ['Leão', 'Pato', 'Papagaio', 'Flamingo', 'Ornitorrinco', 'Tamanduá'],
    "Comida": ['Arroz carreteiro', 'Estrogonofe de frango', 'Macarrão', 'Panqueca', 'Almondegas', 'Bolo de cenoura com cobertura de chocolate'],
    "Objeto": ['Grampeador', 'Relogio de pendulo', 'Canivete', 'Lanterna', 'Garrafa térmica', 'Lampião']
}

def setup_game(numero_jogadores, game_words, categoria_escolhida):
    """
    Configura um novo jogo de 'Fora da Rodada'(Out of the Loop).
    
    Args:
        numero_jogadores (int): Número de jogadores participando do jogo.
        game_words (list): Lista de palavras disponíveis para o jogo.
        categoria_escolhida (str): Categoria selecionada pelos jogadores.
        
    Returns:
        list: Lista de dicionarios, onde cada dicionario representa um jogador e contem seu papel e a palavra que veêm.
    """
    
    

    if numero_jogadores < 3:
        print("O jogo requer pelo menos 3 jogadores.")
        return None

    # Aleatoriamente seleciona um jogador para ficar fora da rodada
    jogador_fora_rodada = random.randint(0, numero_jogadores - 1)
    
    # 'Seta' a categoria escolhida
    categoria = categoria_escolhida

    # Aleatoriamente seleciona uma categoria e palavra secreta
    palavra_secreta = random.choice(game_words[categoria])
    
    jogadores = []
    for i in range(numero_jogadores):
        if i == jogador_fora_rodada:
            # Esse jogador está fora da rodada
            jogador_info = {
                'id_jogador': i+1,
                'papel': 'Impostor',
                'palavra': ('Você esta fora da rodada!\nTente não ser descoberto e descobrir a palavra secreta!')
            }
            
        else:
            # Jogador que está na rodada
            jogador_info = {
                'id_jogador': i+1,
                'papel': 'Jogador',
                'palavra': palavra_secreta
            }
            
        jogadores.append(jogador_info)
        
    print(f'\nA categoria é {categoria}\n')
    return jogadores

# Exemplo de uso
if __name__ == '__main__':
    try:
        numero_jogadores = int(input("Digite o número de jogadores (pelo menos 3):"))
        
        print('\nEscolha uma categoria: ')
        # Cria uma lista dos nomes das categorias
        categorias = list(game_words.keys())
        
        # Cria um loop que lista e printa cada categoria com um numero
        for i, nome_categoria in enumerate(categorias, start=1):
            print(f"{i} - {nome_categoria}")
               
        categoria_escolhida_index = -1
        # Continua pedindo categoria até ter um número válido
        while categoria_escolhida_index < 0 or categoria_escolhida_index >= len(categorias):
            try:
                choice = int(input(f"Escolha um número (1 - {len(categorias)}): "))
                # Subtrai 1 por conta dos índices começarem em 0
                categoria_escolhida_index = choice - 1
                if categoria_escolhida_index < 0 or categoria_escolhida_index >= len(categorias):
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Digite um númeto válido.")
        
        # Pega o nome da categoria escolhida pelo index
        nome_categoria_escolhida = categorias[categoria_escolhida_index]                
             
        # Passa o game_state com os argumentos necessários     
        game_state = setup_game(numero_jogadores, game_words, nome_categoria_escolhida)
        
        if game_state:
            print("Jogo configurado!\n")
            
            for jogador in game_state:
                print(f"Jogador {jogador['id_jogador']}: Papel - {jogador['papel']}, Palavra - '{jogador['palavra']}'\n")
                
    except ValueError:
        print("Por favor, insira um número válido de jogadores.")