import random

intervals = {
    1: "Segunda Menor",
    2: "Segunda Maior",
    3: "Terça Menor",
    4: "Terça Maior",
    5: "Quarta Justa",
    6: "Trítono", # ou Quarta Aumentada / Quinta Diminuta
    7: "Quinta Justa",
    8: "Sexta Menor",
    9: "Sexta Maior",
    10: "Sétima Menor",
    11: "Sétima Maior",
    12: "Oitava"
}

notes_order = ['D2', 'Dx2', 'E2', 'F2', 'Fx2', 'G2', 'Gx2', 'A2', 'Ax2', 'B2', 'C3', 'Cx3', 'D3', 'Dx3', 'E3', 'F3', 'Fx3', 'G3', 'Gx3', 'A3', 'Ax3', 'B3',
               'C4', 'Cx4', 'D4', 'Dx4', 'E4', 'F4', 'Fx4', 'G4', 'Gx4', 'A4', 'Ax4', 'B4', 'C5', 'Cx5', 'D5', 'Dx5', 'E5', 'F5', 'Fx5', 'G5', 'Gx5', 'A5', 'Ax5', 'B5', 'C6', 'Cx6']

def format_note(note_str: str) -> str:
    return note_str.replace('x', '#')[:-1] + ' ' + note_str[-1]

def rev_format_note(user_str: str) -> str:
    user_str = user_str.replace(' ', '')
    return user_str[0].upper() + user_str[1:].replace('#', 'x')

def interval(note1: str, note2: str) -> str:
    distance = notes_order.index(note2) - notes_order.index(note1)
    return intervals[distance]

def playable_scale(tonic: str, menu_choice: str) -> list:    # 1: major; 2: minor; 3: chromatic
    tonic_idx = notes_order.index(tonic)
    if menu_choice == '1':
        playable = [notes_order[tonic_idx+2], notes_order[tonic_idx+4], notes_order[tonic_idx+5], notes_order[tonic_idx+7],
                    notes_order[tonic_idx+9], notes_order[tonic_idx+11], notes_order[tonic_idx+12]]
    elif menu_choice == '2':
        playable = [notes_order[tonic_idx+2], notes_order[tonic_idx+3], notes_order[tonic_idx+5], notes_order[tonic_idx+7],
                    notes_order[tonic_idx+8], notes_order[tonic_idx+10], notes_order[tonic_idx+12]]
    elif menu_choice == '3':
        playable = notes_order[tonic_idx+1:tonic_idx+13]
    return playable

def random_tonic() -> str:
    global notes_order
    return random.choice(notes_order[:-12])