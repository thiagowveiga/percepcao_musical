import customtkinter as ctk
import audio_manager
import musical_logic
import random
import sys
import os

# --- 1. PREPARAÇÃO DO ÁUDIO ---
def obter_caminho_recursos(nome_pasta):
    try:
        caminho_base = sys._MEIPASS
    except Exception:
        caminho_base = os.path.abspath(".")
    return os.path.join(caminho_base, nome_pasta)

pasta_certa = obter_caminho_recursos('stratocaster')
audio_manager.load_sounds(pasta_certa)

# --- 2. CONFIGURAÇÃO DA JANELA PRINCIPAL ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.geometry("1000x600")
janela.title("Percepção Musical")

# Variáveis para guardar as opções escolhidas e o estado do jogo
modo_var = ctk.StringVar(value="1")   # 1: Fixa, 2: Aleatória
escala_var = ctk.StringVar(value="1") # 1: Maior, 2: Menor, 3: Cromática
tonica_atual = ""
relativa_atual = ""
intervalo_atual = ""

# Criamos dois "contêineres" invisíveis (Frames) para alternar as telas
menu_frame = ctk.CTkFrame(janela, fg_color="transparent")
jogo_frame = ctk.CTkFrame(janela, fg_color="transparent")

# =======================================================
# --- LÓGICA DAS TELAS ---
# =======================================================

def mostrar_menu():
    """Esconde o jogo e mostra o menu principal"""
    jogo_frame.pack_forget()
    menu_frame.pack(fill="both", expand=True, padx=20, pady=20)

def iniciar_jogo():
    """Esconde o menu, captura a tônica manual (se houver) e mostra o jogo"""
    global tonica_atual
    tonica_atual = "" 
    
    # Verifica se o usuário digitou uma tônica manual no modo 1
    if modo_var.get() == "1":
        digitado = entry_tonica.get().strip()
        if digitado:
            try:
                # Usa a sua função original para formatar (tira espaço, põe maiúscula, troca # por x)
                formatado = musical_logic.rev_format_note(digitado)
                # Verifica se a nota existe e não está nas últimas oitavas (que não tem margem pra calcular)
                if formatado in musical_logic.notes_order[:-12]:
                    tonica_atual = formatado
            except Exception:
                pass # Se o usuário digitar algo inválido (ex: "Z9"), o código ignora e sorteia aleatório
                
    menu_frame.pack_forget()
    jogo_frame.pack(fill="both", expand=True, padx=20, pady=20)
    preparar_novo_intervalo()

def preparar_novo_intervalo():
    """Sorteia as notas usando o musical_logic e atualiza os textos"""
    global tonica_atual, relativa_atual, intervalo_atual

    modo = modo_var.get()
    escala = escala_var.get()

    # Se for Tônica Fixa e ainda não tivermos sorteado (ou se o usuário deixou em branco)
    if modo == "1" and not tonica_atual: 
        tonica_atual = musical_logic.random_tonic()
    elif modo == "2": # Se for Aleatória, sempre sorteia uma tônica nova
        tonica_atual = musical_logic.random_tonic()

    # Sorteia a relativa baseada na escala
    playable = musical_logic.playable_scale(tonica_atual, escala)
    relativa_atual = random.choice(playable)
    intervalo_atual = musical_logic.interval(tonica_atual, relativa_atual)

    # Esconde a resposta anterior
    lbl_resposta.configure(text="???", text_color="gray")
    
    # Atualiza o título do jogo para mostrar a tônica (se for fixa)
    texto_tonica = f"Tônica Base: {musical_logic.format_note(tonica_atual)}" if modo == "1" else "Modo: Tônica Aleatória"
    lbl_info_jogo.configure(text=texto_tonica)

    # Toca o som automaticamente ao gerar
    tocar_intervalo()

def tocar_intervalo():
    """Toca os sons sem congelar a interface usando janela.after()"""
    btn_ouvir.configure(state="disabled") # Desativa o botão para evitar cliques duplos
    
    audio_manager.play(tonica_atual)
    
    # O comando .after() agenda a segunda nota para tocar 1000ms depois, deixando a tela livre
    janela.after(1000, lambda: audio_manager.play(relativa_atual))
    
    # Reativa o botão de ouvir depois que o som terminar (aprox 2.6s)
    janela.after(2600, lambda: btn_ouvir.configure(state="normal"))

def revelar_resposta():
    """Mostra o gabarito na tela"""
    texto = f"{musical_logic.format_note(relativa_atual)} - {intervalo_atual}"
    if modo_var.get() == "2":
        texto = f"{musical_logic.format_note(tonica_atual)} ➔ {texto}"
        
    lbl_resposta.configure(text=texto, text_color="white")


# =======================================================
# --- DESENHANDO A TELA DE MENU ---
# =======================================================

lbl_titulo_menu = ctk.CTkLabel(menu_frame, text="PERCEPÇÃO MUSICAL", font=("Arial", 24, "bold"))
lbl_titulo_menu.pack(pady=(10, 20))

# Seção de Modo
lbl_modo = ctk.CTkLabel(menu_frame, text="Modo:", font=("Arial", 22))
lbl_modo.pack(anchor="w", padx=20)

# Criamos um "Frame" interno só para colocar o RadioButton e o Campo de Texto lado a lado
frame_fixa = ctk.CTkFrame(menu_frame, fg_color="transparent")
frame_fixa.pack(anchor="w", padx=40, pady=5)

ctk.CTkRadioButton(frame_fixa, text="Tônica Fixa", font=("Arial", 20), variable=modo_var, value="1").pack(side="left")

# O campo onde você pode digitar a tônica
entry_tonica = ctk.CTkEntry(frame_fixa, placeholder_text="Ex: C#3 (vazio = aleatório)", font=("Arial", 16), width=230)
entry_tonica.pack(side="left", padx=20)

ctk.CTkRadioButton(menu_frame, text="Tônica Mudando", font=("Arial", 20), variable=modo_var, value="2").pack(anchor="w", padx=40, pady=5)

# Seção de Escala
lbl_escala = ctk.CTkLabel(menu_frame, text="Escala:", font=("Arial", 22))
lbl_escala.pack(anchor="w", padx=20, pady=(15, 0))
ctk.CTkRadioButton(menu_frame, text="Maior", font=("Arial", 20), variable=escala_var, value="1").pack(anchor="w", padx=40, pady=5)
ctk.CTkRadioButton(menu_frame, text="Menor", font=("Arial", 20), variable=escala_var, value="2").pack(anchor="w", padx=40, pady=5)
ctk.CTkRadioButton(menu_frame, text="Cromática", font=("Arial", 20), variable=escala_var, value="3").pack(anchor="w", padx=40, pady=5)

btn_iniciar = ctk.CTkButton(menu_frame, text="INICIAR TREINO", font=("Arial", 16, "bold"), height=40, command=iniciar_jogo)
btn_iniciar.pack(pady=30)


# =======================================================
# --- DESENHANDO A TELA DE JOGO ---
# =======================================================

lbl_info_jogo = ctk.CTkLabel(jogo_frame, text="Tônica: ...", font=("Arial", 26, "bold"), text_color="#1f6aa5")
lbl_info_jogo.pack(pady=(10, 20))

btn_ouvir = ctk.CTkButton(jogo_frame, text="Ouvir Intervalo", font=("Arial", 20, "bold"), height=60, command=tocar_intervalo)
btn_ouvir.pack(pady=10, fill="x", padx=50)

btn_revelar = ctk.CTkButton(jogo_frame, text="Revelar Resposta", font=("Arial", 20, "bold"), height=60, fg_color="transparent", border_width=2, command=revelar_resposta)
btn_revelar.pack(pady=10, fill="x", padx=50)

lbl_resposta = ctk.CTkLabel(jogo_frame, text="???", font=("Arial", 34, "bold"))
lbl_resposta.pack(pady=20)

btn_proximo = ctk.CTkButton(jogo_frame, text="Próximo Intervalo", font=("Arial", 20, "bold"), height=60, fg_color="#28a745", hover_color="#218838", command=preparar_novo_intervalo)
btn_proximo.pack(pady=10, fill="x", padx=50)

btn_voltar = ctk.CTkButton(jogo_frame, text="Voltar ao Menu", font=("Arial", 20, "bold"), height=60, fg_color="transparent", text_color="gray", hover_color="#333333", command=mostrar_menu)
btn_voltar.pack(pady=(20, 0))


# --- INICIA O APLICATIVO ---
mostrar_menu() # Garante que o Menu é a primeira coisa que aparece
janela.mainloop()