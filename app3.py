






import requests 
import os  

class TelegramBot: 
    def __init__(self):  
        self.token = '7496061516:AAFK89P9dz_Q2izyTxWAgWZIEvx4IPHimow'  
        self.url_base = f'https://api.telegram.org/bot{self.token}/'  
        self.menu = {  
            '1': {'nome': 'FabzBurguer Classic', 'preco': 20.00},
            '2': {'nome': 'FabzCheeseBacon Burguer', 'preco': 25.00},
            '3': {'nome': 'FabzTriploBMT Burguer', 'preco': 30.00},
            '4': {'nome': 'FabzFries', 'preco': 15.00}
        }
        self.pedidos = {} 

    def iniciar(self):  
        update_id = None  
        while True:  
            updates = self.obter_mensagens(update_id)  
            mensagens = updates['result']  
            for mensagem in mensagens: 
                update_id = mensagem['update_id']  
                chat_id = mensagem['message']['from']['id']  
                resposta = self.criar_resposta(mensagem, chat_id)  
                self.responder(resposta, chat_id) 

    def obter_mensagens(self, update_id):  
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'  
        if update_id:  
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)  
        return resultado.json()  

    def criar_resposta(self, mensagem, chat_id):  
        mensagem_texto = mensagem['message']['text']  
        if mensagem_texto.lower() in ('oi', 'ola', 'tudo bem?') or mensagem_texto.lower() == 'menu' or mensagem_texto.lower() == '/start':
         
            return f'''Olá, bem-vindo ao FabzBurguer!{os.linesep}
                      Por favor, escolha uma de nossas belezuras abaixo:{os.linesep}
                      1 - FabzBurguer Classic{os.linesep}
                      2 - FabzCheeseBacon Burguer{os.linesep}
                      3 - FabzTriploBMT Burguer{os.linesep}
                      4 - FabzFries{os.linesep}
                      5 - Verificar pedido.'''
        
        elif mensagem_texto in self.menu.keys():
           
            return self.confirmar_pedido(mensagem_texto, chat_id)
        
        elif mensagem_texto.lower() in ('s', 'sim') and chat_id in self.pedidos:
            
            return 'Qual será o método de pagamento? (Cartão de Crédito / Pix)'
        
        elif mensagem_texto.lower() in ('cartão', 'cartão de crédito', 'crédito', 'credito', 'cartao') and chat_id in self.pedidos:
           
            self.pedidos[chat_id]['confirmado'] = True
            return 'Pedido confirmado! Seu pedido foi armazenado.'
        
        elif mensagem_texto.lower() == 'pix' and chat_id in self.pedidos:
          
            self.pedidos[chat_id]['confirmado'] = True
            return 'Pedido confirmado! Seu pedido foi armazenado.'
        
        elif mensagem_texto.lower() == '5':
           
            return self.verificar_pedido(chat_id)

        else:
           
            return 'Desculpe, não entendi. Gostaria de acessar o menu? Digite "menu".'

    def confirmar_pedido(self, item, chat_id):
   
        if chat_id not in self.pedidos:
            self.pedidos[chat_id] = {'itens': [], 'confirmado': False}
      
        self.pedidos[chat_id]['itens'].append({'nome': self.menu[item]['nome'], 'preco': self.menu[item]['preco']})
       
        return f'''Pedido confirmado! Por favor, confirme o método de pagamento para o item 
        {self.menu[item]["nome"]} - R${self.menu[item]["preco"]:.2f} (Cartão de Crédito ou Pix)'''

    def verificar_pedido(self, chat_id):
       
        if chat_id in self.pedidos and self.pedidos[chat_id]['confirmado']:
            pedidos_usuario = self.pedidos[chat_id]['itens']  
            if len(pedidos_usuario) > 0:  
                mensagem = 'Seus pedidos:'  
                for i, pedido in enumerate(pedidos_usuario, start=1):
                   
                    mensagem += f'\n{i}. {pedido["nome"]} - R${pedido["preco"]:.2f}'
                return mensagem 
            else:
                return 'Você não tem pedidos registrados.' 
        else:
            return 'Seu pedido não foi confirmado'  

    def responder(self, resposta, chat_id):
       
        link = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
     
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