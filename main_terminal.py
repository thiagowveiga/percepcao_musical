import random
import audio_manager
import musical_logic

guitar_samples = 'C:/Users/Ana Veiga/OneDrive/Área de Trabalho/code/percepcao_musical/stratocaster'
audio_manager.load_sounds(guitar_samples)

print('PERCEPÇÃO MUSICAL\n\nMENU:\n1. Tônica fixa\n2. Tônica mudando\n')
mode = input('Escolha o modo (1/2): ')
print('\n1. Escala maior\n2. Escala menor\n3. Escala cromática\n')
scale_choice = input('Escolha a escala (1/2/3): ')

if mode == '1':

    tonic = input('\n1. Escolher tônica (D 2 - C# 5) - digite a nota\n2. Tônica aleatória - digite qualquer outra coisa\n')
    tonic = musical_logic.rev_format_note(tonic)
    if tonic not in musical_logic.notes_order[:-12]:
        tonic = musical_logic.random_tonic()
    
    playable = musical_logic.playable_scale(tonic, scale_choice)

    print(f'\nIniciando com a tônica: {musical_logic.format_note(tonic)}...\nDigite x para sair\n')
    again = True
    while again:

        relative = random.choice(playable)
        interval = musical_logic.interval(tonic, relative)

        audio_manager.play(tonic)
        audio_manager.wait(1000)
        audio_manager.play(relative)
        audio_manager.wait(1600)

        input('Pressione ENTER para revelar')
        print(f'{musical_logic.format_note(relative)} - {interval}')
        exit = input('\nENTER: continuar // x: sair\n')

        if exit == 'x':
            again = False

elif mode == '2':

    print('\nIniciando treinamento sem tônica fixa...\n')

    again = True
    while again:

        tonic = musical_logic.random_tonic()
        playable = musical_logic.playable_scale(tonic, scale_choice)
        relative = random.choice(playable)
        interval = musical_logic.interval(tonic, relative)

        audio_manager.play(tonic)
        audio_manager.wait(1000)
        audio_manager.play(relative)
        audio_manager.wait(1600)

        input('Pressione ENTER para revelar')
        print(f'{musical_logic.format_note(tonic)} > {musical_logic.format_note(relative)} - {interval}')
        exit = input('\nENTER: continuar // x: sair\n')

        if exit == 'x':
            again = False