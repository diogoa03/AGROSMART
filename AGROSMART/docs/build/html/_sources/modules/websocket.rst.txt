WebSocket Server
==============

Sistema de comunicação em tempo real do AgroSmart.

.. automodule:: src.websocket_server
   :members:
   :undoc-members:
   :show-inheritance:

Características
-------------
* Comunicação bidirecional em tempo real
* Suporte a múltiplos clientes
* Notificações automáticas
* Baixa latência

Exemplos de Uso
-------------
.. code-block:: python

   # Inicializar o servidor WebSocket
   websocket = WebSocketServer()
   
   # Configurar callbacks
   @websocket.on_message
   async def handle_message(message):
       # Processar mensagem recebida
       pass