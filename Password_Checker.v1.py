import re
import hashlib
import requests
import stdiomask
from requests.exceptions import RequestException

def analise_complexidade(senha):
    """
    Avalia a força da senha com base em 5 critérios fundamentais.
    Retorna uma pontuação de 0 a 5 e uma lista de recomendações caso a senha falhe em algum critério.
    """
    pontos = 0
    veredito = []

    # Verifica se a senha atinge o tamanho mínimo recomendado (12 caracteres)
    if len(senha) >= 12:
        pontos += 1
    else:
        veredito.append('# - A senha deve conter pelo menos 12 caracteres!')

    # Verifica a presença de pelo menos uma letra maiúscula
    if re.search(r"[A-Z]", senha):
        pontos += 1
    else:
        veredito.append('# - A senha deve conter caracteres maiúsculos!')

    # Verifica a presença de pelo menos uma letra minúscula
    if re.search(r"[a-z]", senha):
        pontos += 1
    else:
        veredito.append('# - A senha deve conter caracteres minúsculos!')

    # Verifica a presença de pelo menos um número
    if re.search(r"\d", senha):
        pontos += 1
    else:
        veredito.append('# - A senha deve conter números!')

    # Verifica a presença de pelo menos um caractere especial comum
    if re.search(r"[!@#$%&*(),.?{}|<>]", senha):
        pontos += 1
    else:
        veredito.append('# - A senha deve conter caracteres especiais!')

    return pontos, veredito


def verificar_vazamento(senha):
    """
    Consulta a API do Have I Been Pwned utilizando o modelo de k-Anonymity.
    A senha real nunca é enviada pela rede, apenas os 5 primeiros caracteres do seu hash SHA-1.
    """
    # Gera o hash SHA-1 da senha e o converte para letras maiúsculas
    sha1_hash = hashlib.sha1(senha.encode('utf-8')).hexdigest().upper()
    
    # Divide o hash: os 5 primeiros caracteres vão para a API, o restante é verificado localmente
    prefixo, sufixo = sha1_hash[:5], sha1_hash[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefixo}"

    try:
        # Adicionado timeout de 5 segundos para evitar que o script congele caso a rede caia
        resposta = requests.get(url, timeout=5)

        # Se a API não retornar sucesso (código 200), aborta a verificação
        if resposta.status_code != 200:
            return "Erro: Falha ao consultar a base de vazamentos da API."

        # A API retorna uma lista de sufixos correspondentes ao prefixo enviado.
        # Comparamos o nosso sufixo local com a lista retornada.
        hashes = (linha.split(':') for linha in resposta.text.splitlines())
        for h, count in hashes:
            if h == sufixo:
                return f"ALERTA: A senha já foi exposta em vazamentos {count} vezes!"
                
        return "✅ Senha não encontrada em grandes vazamentos conhecidos."

    except RequestException:
        # Captura erros de DNS, falha de internet ou timeout da biblioteca requests
        return "Erro de rede: Não foi possível o contato com servidor para verificar vazamentos."


if __name__ == "__main__":
    # stdiomask.getpass oculta a digitação no terminal (como acontece no Linux)
    senha_analisada = stdiomask.getpass("Digite a senha para ser analisada: ")
    
    # Executa a análise de complexidade local
    pontos, recomendacoes = analise_complexidade(senha_analisada)

    # Exibe o feedback estrutural
    if recomendacoes:
        print("\nAlgumas recomendações:")
        for x in recomendacoes:
            print(x)
    else:
        print("\nA sua senha está excelente!")

    # Exibe a pontuação final de complexidade
    print(f'Pontuação de complexidade: {pontos}/5\n')

    # Bloco condicional mantido da versão anterior (apenas reforça a impressão da nota se for >= 3)
    if pontos >= 3:
        print(f'Pontuação de complexidade: {pontos}/5\n')

    # A verificação na nuvem agora é executada sempre, independentemente de ser uma senha fraca ou forte
    print("A verificar vazamentos globais...")
    vazamento = verificar_vazamento(senha_analisada)
    print(vazamento)