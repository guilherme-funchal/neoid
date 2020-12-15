# Glossary

   -    Node: Uma máquina física que executa uma réplica por instância de protocolo. Os nós são conhecidos entre si.
      
   -    Instance:Uma construção lógica que se estende por todos os nós, consistindo em uma réplica de cada nó. Apenas uma instância é `Master` por vez. O resto são todos chamados de `Backup`
   
   -    Replica: Representante de um único nó para uma instância. Uma réplica vive na interseção de um nó e uma instância de protocolo. Ele reside em um nó e é dedicado a uma e apenas uma instância.
   
   -    Pool: A coleção de nós executando o protocolo de consenso
    
   -    View: Uma configuração do pool com líderes designados para cada instância. Cada visualização é conhecida por um número inteiro exclusivo.

   -    View change: Processo de escolha de uma nova réplica primária para cada instância de protocolo, quando a taxa de transferência do mestre atual ou outras métricas de desempenho são inferiores em certos limites do que de outras instâncias de protocolo
    
   -    Election: Processo para decidir qual réplica em uma instância de protocolo seria a principal
   
   -    Request: Uma mensagem enviada pelo cliente para escrever ou consultar o razão. Cada solicitação tem um campo chamado `operação` que é a carga útil da solicitação. A `operação` contém um campo` tipo` que indica a intenção da solicitação.
   
   -    Request Digest: Um hash sha256 dos dados de solicitação serializados.
   
   -    Request ordering: Conclusão bem-sucedida do processo de consenso sobre uma solicitação.
   
   -    Transaction: Uma solicitação de gravação processada com êxito (solicitada) pelo pool. Cada transação possui um campo chamado `tipo` que indica a intenção da transação.
   
   -    Ledger: Um registro ordenado de transações. Cada nó hospeda vários livros que servem a propósitos diferentes. Cada razão é identificado exclusivamente por um id de razão. Cada nó correto hospeda o mesmo razão que qualquer outro nó correto. O livro-razão atribui a cada transação um número inteiro positivo único e monotonicamente crescente denominado número de sequência.
   
   -    State: Uma projeção do livro-razão. Expõe um armazenamento de valor-chave como a API, pode fornecer prova de presença de chaves com valores no merkle. Atualmente usa um Merkle Patricia Trie sob o capô.
   
   -    Catchup: O processo de um nó sincronizando um razão com outros nós. Usado quando um nó é iniciado ou fica atrás de outros.
   
   -    Ledger Manager: Contém lógica para catchup. Permite o registro de livros a serem sincronizados e os callbacks a serem chamados em eventos diferentes.
   
   -    Request Handler: Uma classe que contém a lógica de processamento de solicitações de certo `tipo`. Para solicitações de gravação, atualiza o razão e pode atualizar o estado também. 
   
   -    Client:Lógica genérica para o envio de solicitações a nó (s), tratamento de novas tentativas, confirmações, respostas, etc. Permite registrar retornos de chamada que são chamados assim que uma solicitação foi processada com sucesso pelo pool.
   
   -    Wallet: Armazena chaves privadas e outros segredos. Também contém código para agir em solicitações processadas com sucesso.
   
   
   Fonte : https://github.com/hyperledger/indy-plenum/edit/master/docs/source/glossary.md
