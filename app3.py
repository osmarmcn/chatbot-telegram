

# 7339844257:AAExECWw4_UWhwxXU67VjMaf1nxAKUdesXM


# 7339844257:AAExECWw4_UWhwxXU67VjMaf1nxAKUdesXM

# https://web.telegram.org/a/#7176261902




import requests  # Importa a biblioteca requests para fazer solicitações HTTP
import os  # Importa o módulo os para manipulação de funcionalidades dependentes do sistema operacional

class TelegramBot:  # Define uma classe chamada TelegramBot
    def __init__(self):  # Define o método inicializador da classe
        self.token = '7496061516:AAFK89P9dz_Q2izyTxWAgWZIEvx4IPHimow'  # Define o token do bot do Telegram
        self.url_base = f'https://api.telegram.org/bot{self.token}/'  # Define a URL base da API do Telegram usando o token
        self.menu = {  # Define um dicionário com o menu do restaurante
            '1': {'nome': 'FabzBurguer Classic', 'preco': 20.00},
            '2': {'nome': 'FabzCheeseBacon Burguer', 'preco': 25.00},
            '3': {'nome': 'FabzTriploBMT Burguer', 'preco': 30.00},
            '4': {'nome': 'FabzFries', 'preco': 15.00}
        }
        self.pedidos = {}  # Inicializa um dicionário vazio para armazenar os pedidos dos clientes

    def iniciar(self):  # Define o método para iniciar o bot
        update_id = None  # Inicializa o ID da atualização como None
        while True:  # Loop infinito para ficar constantemente verificando por novas mensagens
            updates = self.obter_mensagens(update_id)  # Obtém as mensagens mais recentes
            mensagens = updates['result']  # Extrai as mensagens do resultado da atualização
            for mensagem in mensagens:  # Loop pelas mensagens recebidas
                update_id = mensagem['update_id']  # Obtém o ID da atualização para evitar processar a mesma mensagem novamente
                chat_id = mensagem['message']['from']['id']  # Obtém o ID do chat de onde a mensagem veio
                resposta = self.criar_resposta(mensagem, chat_id)  # Cria uma resposta com base na mensagem recebida
                self.responder(resposta, chat_id)  # Envia a resposta para o chat de origem da mensagem

    def obter_mensagens(self, update_id):  # Define o método para obter as mensagens do Telegram
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'  # Define a URL da requisição para obter as atualizações
        if update_id:  # Se houver um ID de atualização, adiciona o parâmetro offset para obter apenas novas atualizações
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)  # Faz uma solicitação GET para obter as atualizações
        return resultado.json()  # Retorna o conteúdo da resposta da solicitação como um objeto JSON

    def criar_resposta(self, mensagem, chat_id):  # Define o método para criar uma resposta com base na mensagem recebida
        mensagem_texto = mensagem['message']['text']  # Extrai o texto da mensagem
        if mensagem_texto.lower() in ('oi', 'ola', 'tudo bem?') or mensagem_texto.lower() == 'menu' or mensagem_texto.lower() == '/start':
            # Se a mensagem for uma saudação, solicitação de menu ou comando /start, retorna o menu
            return f'''Olá, bem-vindo ao FabzBurguer!{os.linesep}
                      Por favor, escolha uma de nossas belezuras abaixo:{os.linesep}
                      1 - FabzBurguer Classic{os.linesep}
                      2 - FabzCheeseBacon Burguer{os.linesep}
                      3 - FabzTriploBMT Burguer{os.linesep}
                      4 - FabzFries{os.linesep}
                      5 - Verificar pedido.'''
        
        elif mensagem_texto in self.menu.keys():
            # Se a mensagem corresponder a uma opção de menu, confirma o pedido
            return self.confirmar_pedido(mensagem_texto, chat_id)
        
        elif mensagem_texto.lower() in ('s', 'sim') and chat_id in self.pedidos:
            # Se a mensagem for uma confirmação de pedido e houver um pedido registrado para o chat, solicita o método de pagamento
            return 'Qual será o método de pagamento? (Cartão de Crédito / Pix)'
        
        elif mensagem_texto.lower() in ('cartão', 'cartão de crédito', 'crédito', 'credito', 'cartao') and chat_id in self.pedidos:
            # Se o método de pagamento for cartão de crédito e houver um pedido registrado para o chat, confirma o pedido
            self.pedidos[chat_id]['confirmado'] = True
            return 'Pedido confirmado! Seu pedido foi armazenado.'
        
        elif mensagem_texto.lower() == 'pix' and chat_id in self.pedidos:
            # Se o método de pagamento for Pix e houver um pedido registrado para o chat, confirma o pedido
            self.pedidos[chat_id]['confirmado'] = True
            return 'Pedido confirmado! Seu pedido foi armazenado.'
        
        elif mensagem_texto.lower() == '5':
            # Se a mensagem for para verificar o pedido, retorna os pedidos do cliente
            return self.verificar_pedido(chat_id)

        else:
            # Se a mensagem não for reconhecida, solicita ao cliente
            return 'Desculpe, não entendi. Gostaria de acessar o menu? Digite "menu".'

    def confirmar_pedido(self, item, chat_id):
    # Verifica se o chat_id não está registrado nos pedidos e, se não estiver, cria uma entrada para ele
        if chat_id not in self.pedidos:
            self.pedidos[chat_id] = {'itens': [], 'confirmado': False}
        # Adiciona o item selecionado aos pedidos do chat_id
        self.pedidos[chat_id]['itens'].append({'nome': self.menu[item]['nome'], 'preco': self.menu[item]['preco']})
        # Retorna uma mensagem confirmando o pedido e solicitando o método de pagamento
        return f'''Pedido confirmado! Por favor, confirme o método de pagamento para o item 
        {self.menu[item]["nome"]} - R${self.menu[item]["preco"]:.2f} (Cartão de Crédito ou Pix)'''

    def verificar_pedido(self, chat_id):
        # Verifica se o chat_id está registrado nos pedidos e se o pedido está confirmado
        if chat_id in self.pedidos and self.pedidos[chat_id]['confirmado']:
            pedidos_usuario = self.pedidos[chat_id]['itens']  # Obtém os pedidos do usuário
            if len(pedidos_usuario) > 0:  # Se houver pedidos registrados
                mensagem = 'Seus pedidos:'  # Inicia a mensagem com os pedidos do usuário
                for i, pedido in enumerate(pedidos_usuario, start=1):
                    # Para cada pedido, adiciona o nome e o preço formatados à mensagem
                    mensagem += f'\n{i}. {pedido["nome"]} - R${pedido["preco"]:.2f}'
                return mensagem  # Retorna a mensagem com os pedidos do usuário
            else:
                return 'Você não tem pedidos registrados.'  # Se não houver pedidos registrados, retorna uma mensagem informando isso
        else:
            return 'Seu pedido não foi confirmado'  # Se o pedido não foi confirmado, retorna uma mensagem informando isso

    def responder(self, resposta, chat_id):
        # Constrói o link para enviar a mensagem de resposta usando a API do Telegram
        link = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        # Envia a mensagem de resposta para o chat especificado
        requests.get(link)

bot = TelegramBot()
bot.iniciar()


            





# import requests
# import os

# class TelegramBot:
#     def __init__(self) -> None:
#         self.token = '7496061516:AAFK89P9dz_Q2izyTxWAgWZIEvx4IPHimow'
#         self.url_base = 'https://api.telegram.org/bot{self.token}/'
#         self.menu = {
#             '1': {'nome': 'PyBurguer Classic', 'preco':20.00},
#             '2': {'nome': 'PyBurguer Bacon', 'preco':28.00},
#             '3': {'nome': 'PyBurguer Vegano', 'preco':25},
#             '4': {'nome': 'PyBurguer Royal', 'preco':34.50}
        
#         }

#         self.pedidos = {}


#         def iniciar(self):
#             updated_id = None

#             while True:
#                 updates = self.obter_mensagens(updated_id)
#                 mensagens = updates['results']
#                 for mensagem in mensagens:
#                     updated_id = mensagem['updated_id']

#                     chat_id = mensagem['message']['from']['id']

#                     resposta = self.criar_resposta(mensagem, chat_id)

#                     self.responder(resposta, chat_id)
#                 # update = self.obter_atualizacoes(update_id)

#         def obter_mensagem(self, update_id):
#             link_requisicao = f'{self.url_base}getUpdates?timeout=100'

#             if update_id:
#                 link_requisicao = f'{link_requisicao}&offset={update_id + 1}'

#             resultado = requests.get(link_requisicao)

#             return resultado.json()
        
#         def criar_respsota(self, mensagem, chat_id):
#             mensagem_texto = mensagem['message']['text']

#             if mensagem_texto.lower() in ('oi', 'olá', 'tudo bem?') == 'menu' or mensagem_texto.lower() == mensagem_texto.lower() == '/start':
#                 return f"""
#                     Olá, bem vindo ao Burger factory!{os.linesep}
#                     Escolha uma das opções abaixo:{os.linesep}
#                 1 - PyBurguer Classic{os.linesep}
#                 2 - PyBurguer Bacon{os.linesep}
#                 3 - PyBurguer Vegano{os.linesep}
#                 4 - PyBurguer Royal{os.linesep}
#                 5 - verficar pedido"""

#             elif mensagem_texto in self.menu.keys():
#                 return self.corfimar_pedido(mensagem_texto, chat_id)
            
#             elif mensagem_texto.lower() in ('s', 'sim') and chat_id in self.pedidos:
#                 return 'Qual será o metodo de pagamento? (Cartão ou pix)'
            
#             elif mensagem_texto.lower() in ('cartão' , 'cartão de credito', 'debito', 'cartao') and chat_id in self.pedidos:
#                 self.pedidos[chat_id]['confirmado']  = True
#                 return 'pedido confirmado! seu pedido está na fila.'
            
#             elif mensagem_texto.lower() in ('pix') and chat_id in self.pedidos:
#                 self.pedidos[chat_id]['confirmado']  = True
#                 return 'pedido confirmado! seu pedido está na fila.'
            
#             elif mensagem_texto == '4':
#                 return self.verificar_pedido(chat_id)
                
#             else:
#                 return 'Opção inválida! Gostaria de acessar o menu? digite "menu". '
        
#         def verificar_pedido(self, chat_id):
#             if chat_id in self.pedidos and self.pedidos['chat_id']['confirmado']:
#                 pedidos_usuario = self.pedidos[chat_id]['items']
#                 if len(pedidos_usuario) > 0:
#                     mensagem = 'seus pedidos'
#                     for i, pedido in enumerate(pedidos_usuario, start=1):
#                         mensagem += f'\n{i} - {pedido["nome"]} - R${pedido['preco']}'
#                         return mensagem
#                 else:
#                     return 'Você não tem pedidos'
                
#             else:
#                 return 'seu pedido não foi confirmado'
            
#         def responder(self, resposta, chat_id):
#             link = f'{self.url_base}sendMessagw?chat_id={chat_id}&text={resposta}'

#         def confirmar_pedido(self,item, chat_id):
#             if chat_id not in self.pedidos:
#                 self.pedidos[chat_id] = {'items':[], 'confirmado':False}
#             self.pedidos[chat_id]['items'].append({'nome':self.menu[item]['nome'], 'preco':self.menu[item]['preco']})