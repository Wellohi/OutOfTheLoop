import random


# uma lista de palavras para testar o jogo
game_words = {
    "Animal": ['Leão', 'Pato', 'Papagaio', 'Flamingo', 'Ornitorrinco', 'Tamanduá'],
    "Comida": ['Arroz carreteiro', 'Estrogonofe de frango', 'Macarrão', 'Panqueca', 'Almondegas', 'Bolo de cenoura com cobertura de chocolate'],
    "Objeto": ['Grampeador', 'Relogio de pendulo', 'Canivete', 'Lanterna', 'Garrafa térmica', 'Lampião']
}

def setup_game(player_names, chosen_category): # game_words
    """
    Configura um novo jogo de 'Fora da Rodada'(Out of the Loop).
    
    Args:
        player_names (list): Lista de strings com nomes dos jogadores.
        ### game_words (list): Lista de palavras disponíveis para o jogo.
        chosen_category (str): Categoria selecionada pelos jogadores.
        
    Returns:
        list: Lista de dicionarios, onde cada dicionario representa um jogador e contem seu papel e a palavra que veêm.
    """
    
    num_players = len(player_names)

    if num_players < 3:
        print("O jogo requer pelo menos 3 jogadores.")
        return None

    # Aleatoriamente seleciona um jogador para ficar fora da rodada
    out_of_the_loop_player_index = random.randint(0, num_players - 1)

    # Aleatoriamente seleciona a palavra secreta
    secret_word = random.choice(game_words[chosen_category])
    
    players = []
    
    for i, name in enumerate(player_names):
        if i == out_of_the_loop_player_index:
            # Esse jogador está fora da rodada
            player_info = {
                'name': name,
                'papel': 'Impostor',
                'palavra': ('Você está fora da rodada!\nTente não ser descoberto e descobrir a palavra secreta!')
            }
            
        else:
            # Jogador que está na rodada
            player_info = {
                'name': name,
                'papel': 'Jogador',
                'palavra': secret_word
            }
            
        players.append(player_info)
        
    print(f'\nA categoria é {chosen_category}\n')
    return players

# Exemplo de uso
if __name__ == '__main__':
    try:
        # Input do nome dos jogadores
        names_input = input("Coloque o nome dos jogadores, separados por vírgula: ")
        
        # Processa as strings na lista de nomes
        player_names = [name.strip() for name in names_input.split(',') if name.strip()]
        
        # Checa se existem jogadores o suficiente
        if len(player_names) < 3:
            print('O jogo precisa ter ao menos 3 jogadores')
        else:        
            print('\nEscolha uma categoria: ')
            # Cria uma lista dos nomes das categorias
            categories = list(game_words.keys())
            # Cria um loop que lista e printa cada categoria com um numero
            for i, category_name in enumerate(categories, start=1):
                print(f"{i} - {category_name}")
                
            chosen_category_index = -1
            # Continua pedindo categoria até ter um número válido
            while chosen_category_index < 0 or chosen_category_index >= len(categories):
                try:
                    choice = int(input(f"Escolha um número (1 - {len(categories)}): "))
                    # Subtrai 1 por conta dos índices começarem em 0
                    chosen_category_index = choice - 1
                    if chosen_category_index < 0 or chosen_category_index >= len(categories):
                        print("Número inválido. Tente novamente.")
                except ValueError:
                    print("Digite um númeto válido.")
            
            # Pega o nome da categoria escolhida pelo index
            nome_chosen_category = categories[chosen_category_index]                
                
            # Passa o game_state com os argumentos necessários     
            game_state = setup_game(player_names, nome_chosen_category)
            
            if game_state:
                print("Jogo configurado!\n")
                for jogador in game_state:
                    print(f"Jogador {jogador['name']}: Papel - {jogador['papel']}, Palavra - '{jogador['palavra']}'\n")
                
    except ValueError:
        print("Por favor, insira um número válido de jogadores.")