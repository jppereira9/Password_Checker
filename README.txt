PT-BR
🛡️ Python Password Checker

Um verificador de senhas construído em Python que avalia a segurança de uma senha utilizando duas abordagens: Análise de Complexidade Local e Verificação de Vazamentos Globais (utilizando a API do Have I Been Pwned).
Esta ferramenta foi desenhada com foco em privacidade. Em nenhum momento a sua senha trafega em texto claro pela rede.

O projeto agora conta com duas versões: uma para o Terminal (CLI) com ocultação nativa de digitação e outra com Interface Gráfica (GUI).

✨ Funcionalidades:

Análise de Heurística Local: Verifica a força estrutural da senha com base em regras modernas de higiene cibernética (comprimento mínimo de 12 caracteres, uso de maiúsculas, minúsculas, números e símbolos).

Proteção de Privacidade com k-Anonymity: Utiliza o modelo k-Anonymity para verificar se a senha já foi exposta em vazamentos de dados públicos.

Feedback Direcionado: Fornece pontuação (Score 0-5) e dicas pontuais de como melhorar a estrutura da senha informada.

Entrada Segura de Dados: A versão de terminal utiliza a biblioteca stdiomask para ocultar a senha enquanto é digitada (evitando exposição na tela). A versão gráfica utiliza o tkinter com mascaramento nativo de caracteres (*).

🔒 Como a Verificação de Vazamento Funciona?

Para garantir a sua segurança, o script não envia a sua senha para a internet. Em vez disso, ele faz o seguinte:

Calcula o hash SHA-1 da sua senha localmente.

Extrai os 5 primeiros caracteres desse hash (o prefixo).

Envia apenas o prefixo para a API do Have I Been Pwned.

A API retorna uma lista de todos os hashes comprometidos que começam com esse prefixo (geralmente centenas ou milhares).

O script compara localmente o restante do seu hash (o sufixo) com a lista recebida para determinar se houve um vazamento.

🚀 Como Usar

Pré-requisitos:
Certifique-se de ter o Python 3 instalado em sua máquina. A versão com interface gráfica utiliza o tkinter (que já vem embutido no Python padrão). Para as demais bibliotecas, instale as dependências:

Clone o repositório ou faça o download dos arquivos Python.

Instale as dependências executando:
pip install requests stdiomask

Execução:

No terminal, navegue até a pasta onde os scripts estão localizados e escolha a versão que deseja rodar:

Para a versão de Terminal (CLI):
python Password_Checker.v1.py

Para a versão com Interface Gráfica (GUI):
python Password_Checker_GUI.py

⚠️ Aviso Legal (Disclaimer):

Este projeto tem fins educacionais para demonstrar boas práticas na validação de senhas e integração segura de APIs.
Embora o script seja seguro devido ao uso do k-Anonymity e do mascaramento de digitação, evite testar senhas reais ou críticas em ambientes não confiáveis, pois a sua máquina pode estar suscetível a keyloggers ou malwares no seu ambiente de desenvolvimento.

EN
🛡️ Python Password Checker

A Python-based password checker that evaluates password security using a dual-layered approach: Local Complexity Analysis and Global Leak Verification (via the Have I Been Pwned API).

This tool is designed with a privacy-first mindset. Your plaintext password is never transmitted over the network.

The project now features two versions: a Command Line Interface (CLI) with native input masking, and a Graphical User Interface (GUI).

✨ Features:

Local Heuristic Analysis: Checks the structural strength of the password based on modern cyber hygiene rules (minimum length of 12 characters, mix of uppercase, lowercase, numbers, and symbols).

Privacy Protection via k-Anonymity: Uses the k-Anonymity model to check if the password has been exposed in public data breaches without revealing the password itself.

Actionable Feedback: Provides a numerical rating (Score 0-5) along with specific tips on how to improve the provided password's structure.

Secure Data Input: The CLI version uses the stdiomask library to hide the password as it is typed (preventing screen exposure). The GUI version uses tkinter with native character masking (*).

🔒 How Does the Leak Verification Work?:

To guarantee your safety, the script does not send your actual password over the internet. Instead, it performs the following steps:

Calculates the SHA-1 hash of your password locally.

Extracts the first 5 characters of this hash (the prefix).

Sends only the prefix to the Have I Been Pwned API.

The API returns a list of all compromised hashes that start with that specific prefix (usually hundreds or thousands of results).

The script locally compares the remainder of your hash (the suffix) against the downloaded list to determine if a breach occurred.

🚀 Getting Started:

Prerequisites:
Ensure you have Python 3 installed on your system. The GUI version relies on tkinter (which comes pre-installed with standard Python). For the other modules, install the required dependencies:

Clone the repository or download the Python files.

Install the required dependencies by running:
pip install requests stdiomask

Usage:

Open your terminal, navigate to the directory containing the scripts, and choose which version you want to run:

To run the Terminal (CLI) version:
python Password_Checker_CLI.py

To run the Graphical Interface (GUI) version:
python Password_Checker_GUI.py

⚠️ Disclaimer:

This project is intended for educational purposes to demonstrate best practices in password validation and secure API integration.
Although the script itself is secure due to the use of k-Anonymity and input masking, avoid testing your real, critical passwords in untrusted environments, as your machine might be susceptible to keyloggers or malware running in your development environment.