import random


current_number = '0'
game_started = False
can_use_card = False
host = ''
players = []


class Player:
    def __init__(self, username, number, second_number):
        self.username = username
        self.number = number
        self.second_number = second_number


async def handle_response(message, username, user_message) -> str:
    global game_started
    global host
    global can_use_card
    global current_number
    p_message = user_message.lower()

    if p_message == 'hello':
        return 'Hey there'

    if p_message == 'roll':
        return str(random.randint(1, 6))

    if p_message == 'start game':
        if game_started:
            return "```O jogo ja foi iniciado```"

        host = username
        game_started = True

        return "```md\n### Jogo iniciado ###\nDigite 'join' para participar```"

    if p_message == 'join':
        if not game_started:
            return ''

        for player in players:
            if player.username == username:
                return f"```{username} já está no jogo.```"

        existing_numbers = {player.number for player in players} | {player.second_number for player in players}
        while True:
            number = random.randint(1, 100)
            if number not in existing_numbers:
                break
        while True:
            second_number = random.randint(1, 100)
            if second_number not in existing_numbers:
                break

        if number > second_number:
            aux = number
            number = second_number
            second_number = aux

        player = Player(username, number, second_number)

        players.append(player)

        player_list = '\n'.join([f"{p.username}" for p in players])
        await message.author.send(f"```Seus números são {number} e {second_number}```")
        return f"```{username} entrou no jogo.\n\nJogadores atuais:\n{player_list}" \
               f"\n\nDigite 'pronto' para começar o jogo```"

    if p_message == 'pronto':
        if not game_started:
            return ''

        if username != host:
            return '```Apenas o host pode iniciar o jogo```'

        can_use_card = True

        return "```Digite 'jogar carta' para jogar sua carta\nJoguem suas cartas!!!```"

    if p_message == 'jogar carta':
        if not game_started or not can_use_card:
            return ''

        for player in players:
            showed_number = ''
            if player.number != '':
                showed_number = player.number
            else:
                showed_number = player.second_number

            if player.username == username:
                if player.number != '':
                    player.number = ''
                elif player.second_number != '':
                    players.remove(player)

                if int(showed_number) < int(current_number):
                    current_number = '0'
                    game_started = False
                    can_use_card = False
                    host = ''
                    players.clear()
                    return f'```CSS\n{username} falou seu número\nO número era [{showed_number}]' \
                           f'\n\nVocês perderam o jogo 🤣🤣🤣🫵🫵🫵```'

                current_number = showed_number

                if not players:
                    current_number = '0'
                    game_started = False
                    can_use_card = False
                    host = ''
                    players.clear()
                    return f'```CSS\n{username} falou seu número\nO número era [{showed_number}]' \
                           f'\n\nParabéns vocês ganharam o jogo 🥳🥳🥳```'

                return f'```CSS\n{username} falou seu número\nO número era [{showed_number}]```'

