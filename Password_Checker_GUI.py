import re
import hashlib
import requests
import tkinter as tk # Biblioteca padrão do Python para interfaces gráficas
from tkinter import messagebox
from requests.exceptions import RequestException

def analise_complexidade(senha):
    """
    Avalia a força da senha com base em 5 critérios fundamentais.
    Retorna uma pontuação de 0 a 5 e uma lista de recomendações.
    """
    pontos = 0
    veredito = []

    # Verifica se a senha atinge o tamanho mínimo recomendado (12 caracteres)
    if len(senha) >= 12:
        pontos += 1
    else:
        veredito.append('- A senha deve conter pelo menos 12 caracteres!')

    # Verifica a presença de pelo menos uma letra maiúscula
    if re.search(r"[A-Z]", senha):
        pontos += 1
    else:
        veredito.append('- A senha deve conter caracteres maiúsculos!')

    # Verifica a presença de pelo menos uma letra minúscula
    if re.search(r"[a-z]", senha):
        pontos += 1
    else:
        veredito.append('- A senha deve conter caracteres minúsculos!')

    # Verifica a presença de pelo menos um número
    if re.search(r"\d", senha):
        pontos += 1
    else:
        veredito.append('- A senha deve conter números!')

    # Verifica a presença de pelo menos um caractere especial comum
    if re.search(r"[!@#$%&*(),.?{}|<>]", senha):
        pontos += 1
    else:
        veredito.append('- A senha deve conter caracteres especiais!')

    return pontos, veredito

def verificar_vazamento(senha):
    """
    Consulta a API do Have I Been Pwned utilizando o modelo de k-Anonymity.
    A senha real nunca é enviada pela rede.
    """
    # Gera o hash SHA-1 da senha e o converte para letras maiúsculas
    sha1_hash = hashlib.sha1(senha.encode('utf-8')).hexdigest().upper()
    
    # Divide o hash: os 5 primeiros caracteres vão para a API
    prefixo, sufixo = sha1_hash[:5], sha1_hash[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefixo}"

    try:
        # Timeout de 5 segundos para evitar travamento da interface
        resposta = requests.get(url, timeout=5)

        if resposta.status_code != 200:
            return "Erro: Falha ao consultar a base de vazamentos da API."

        # Compara o sufixo local com a resposta da API
        hashes = (linha.split(':') for linha in resposta.text.splitlines())
        for h, count in hashes:
            if h == sufixo:
                return f"ALERTA: A senha já foi exposta em vazamentos {count} vezes!"
                
        return "✅ Senha não encontrada em grandes vazamentos conhecidos."

    except RequestException:
        return "Erro de rede: Não foi possível o contato com servidor."

def executar_analise():
    """
    Função engatilhada pelo botão da interface para coletar o texto,
    rodar as funções de backend e atualizar os textos na tela.
    """
    senha = entrada_senha.get()
    
    if not senha:
        messagebox.showwarning("Aviso", "Por favor, digite uma senha para analisar.")
        return

    # Limpa resultados anteriores da tela
    label_recomendacoes.config(text="")
    label_vazamento.config(text="A verificar vazamentos globais...", fg="blue")
    janela.update() # Força a atualização da tela para mostrar a mensagem de carregamento

    # Executa a análise local
    pontos, recomendacoes = analise_complexidade(senha)

    # Atualiza a pontuação na interface
    label_pontuacao.config(text=f'Pontuação de complexidade: {pontos}/5')

    # Atualiza as recomendações
    if recomendacoes:
        texto_rec = "Recomendações:\n" + "\n".join(recomendacoes)
        label_recomendacoes.config(text=texto_rec, fg="#d9534f") # Vermelho suave
    else:
        label_recomendacoes.config(text="A sua senha está excelente!", fg="#5cb85c") # Verde

    # Executa a verificação na nuvem
    vazamento = verificar_vazamento(senha)
    
    # Formata a cor do resultado do vazamento com base na resposta
    if "ALERTA" in vazamento:
        label_vazamento.config(text=vazamento, fg="red")
    elif "Erro" in vazamento:
        label_vazamento.config(text=vazamento, fg="orange")
    else:
        label_vazamento.config(text=vazamento, fg="#5cb85c")

def alternar_visualizacao_senha():
    """
    Alterna o caractere de exibição do campo de senha.
    Se a caixa estiver marcada, remove o asterisco. Caso contrário, recoloca.
    """
    if var_mostrar_senha.get():
        entrada_senha.config(show="") # Mostra o texto normal
    else:
        entrada_senha.config(show="*") # Oculta com asteriscos

# ==========================================
# CONFIGURAÇÃO DA INTERFACE GRÁFICA (TKINTER)
# ==========================================

# Cria a janela principal
janela = tk.Tk()
janela.title("Analisador de Segurança de Senhas")
janela.geometry("450x500") # Aumentei um pouco a altura para acomodar o novo botão
janela.configure(padx=20, pady=20)

# Título da aplicação
titulo = tk.Label(janela, text="Verificador de Senhas", font=("Helvetica", 16, "bold"))
titulo.pack(pady=(0, 15))

# Campo de instrução
instrucao = tk.Label(janela, text="Digite a senha para ser analisada:")
instrucao.pack(anchor="w")

# Caixa de entrada da senha (o parâmetro show="*" substitui a digitação por asteriscos)
entrada_senha = tk.Entry(janela, width=40, font=("Helvetica", 12), show="*")
entrada_senha.pack(pady=5)

# Variável de controle e Checkbutton para mostrar/ocultar senha
var_mostrar_senha = tk.BooleanVar()
checkbox_mostrar = tk.Checkbutton(
    janela, 
    text="Mostrar senha", 
    variable=var_mostrar_senha, 
    command=alternar_visualizacao_senha
)
# Alinha o checkbox um pouco mais à esquerda para ficar abaixo do começo do campo de texto
checkbox_mostrar.pack(anchor="w", padx=30) 

# Botão para iniciar a análise
botao_analisar = tk.Button(janela, text="Analisar Senha", command=executar_analise, bg="#007bff", fg="white", font=("Helvetica", 10, "bold"))
botao_analisar.pack(pady=15)

# Elementos visuais para exibir os resultados (iniciam vazios)
label_pontuacao = tk.Label(janela, text="", font=("Helvetica", 12, "bold"))
label_pontuacao.pack(pady=5)

label_recomendacoes = tk.Label(janela, text="", justify="left", font=("Helvetica", 10))
label_recomendacoes.pack(pady=5, anchor="w")

label_vazamento = tk.Label(janela, text="", font=("Helvetica", 10, "bold"), wraplength=400)
label_vazamento.pack(pady=15)

# Inicia o loop (mantém a janela aberta)
janela.mainloop()