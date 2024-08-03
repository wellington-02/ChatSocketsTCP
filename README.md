# ChatSocketsTCP

## Server
* O servidor é TCP multi-threaded que assim permite a comunicação com múltiplos clientes simultaneamente. Utilizando a classe ClientHandler, cada conexão de cliente é gerenciada em uma thread separada, permitindo que o servidor continue aceitando novas conexões enquanto processa mensagens de clientes conectados. A classe MultiTCPServer gerencia as conexões, possibilitando o envio de mensagens para clientes específicos e a listagem dos clientes conectados. O servidor pode ser encerrado de forma segura ao digitar 'exit' quando solicitado a enviar uma mensagem, garantindo que todas as conexões sejam fechadas adequadamente.

## Client
* O cliente TCP simples se conecta a um servidor e permite a troca de mensagens. A classe SimpleTCPClient gerencia a conexão com o servidor e inicia uma thread separada, ReceiveMessages, para receber e exibir mensagens enviadas pelo servidor. Mensagens enviadas pelo servidor são identificadas pela palavra-chave "server:". O cliente pode enviar mensagens ao servidor e desconectar-se ao digitar 'exit'. A comunicação é mantida até que o cliente encerre a conexão.
