# Conceitos

**Node**<br>
Um servidor de rede de computadores executando uma instância do código necessário para operar um razão distribuído ou blockchain. 
Na infraestrutura do Sovrin, um nó é operado por um administrador executando uma instância do código-fonte aberto do Sovrin para manter o Ledger do Sovrin. 
Um Nó deve ser um Nó Validador ou Nó Observador.

**Steward**<br>
Uma organização aprovada pela Fundação Sovrin para operar um Nó. Um Administrador deve atender às qualificações definidas nas Políticas de Negócios de Administrador 
e aos requisitos técnicos definidos nas Políticas Técnicas de Administrador (consulte o Apêndice A do Documento Principal da Estrutura de Governança do Sovrin). 
Um administrador também deve executar o Acordo de administrador do Sovrin.

**Rede SSI**<br>
Uma versão genérica da rede Sovrin que suporta o protocolo SSI e a pilha SSI. Usando padrões abertos interoperáveis e estruturas de governança, 
várias redes SSI podem trabalhar juntas para formar uma camada SSI unificada.

**Trustees**<br>
Um Proprietário de identidade com responsabilidades específicas de controle de identidade por outro Proprietário de identidade ou responsabilidades de governança 
específicas por uma Estrutura de governança.

**Genesis**<br>
As primeiras Transações gravadas em um razão ou blockchain que estabelecem as condições iniciais das quais depende toda a evolução futura do estado do razão. 
As Transações Genesis para o livro razão da Rede Principal Sovrin foram escritas em 31 de julho de 2017 e definiram o conjunto inicial de Trustees, Stewards, 
e Nodes.

**Credencial**<br>
Uma credencial que inclui uma prova do emissor. Normalmente, essa prova é na forma de uma assinatura digital. Na Infraestrutura do Sovrin, uma Credencial Verificável
usa Provas de Conhecimento Zero por padrão e geralmente pode ser verificada pela Chave Pública do Emissor armazenada na Definição de Credencial no Razão do Sovrin. 
Com base na definição fornecida pelo Grupo de Trabalho de Reivindicações Verificáveis do W3C.

**Governança**
O próximo passo na escada do fortalecimento e aumento da confiança é estabelecer uma Autoridade de Governança formal e publicar uma Estrutura de Governança oficial. Este é o passo que a Fundação Sovrin deu a partir de setembro de 2016, com sua incorporação formal, após a qual o Grupo de Trabalho da Estrutura de Governança do Sovrin tem trabalhado desde então.

**Issuer**
A entidade que emite uma credencial a um titular. Com base na definição fornecida pelo Grupo de Trabalho de Reivindicações Verificáveis do W3C

**Wallet**<br>
Um módulo de software e, opcionalmente, um módulo de hardware associado, para armazenar e acessar com segurança Chaves Privadas, Segredos de Link, outro material 
de chave criptográfica sensível e outros Dados Privados usados por uma Entidade. Uma Carteira é acessada por um Agente. Na infraestrutura do Sovrin, as carteiras 
implementam os padrões DKMS emergentes para gerenciamento de chaves criptográficas descentralizadas e interoperáveis.

Origem : https://raw.githubusercontent.com/sovrin-foundation/sovrin/stable/sovrin/pool_transactions_live_genesis

Fonte : https://docs.google.com/document/d/1gfIz5TT0cNp2kxGMLFXr19x1uoZsruUe_0glHst2fZ8/edit#

# Redes da BCGov 
Redes públicas que podem ser utilizados para teste : 
1. http://test.bcovrin.vonx.io
1. http://greenlight.bcovrin.vonx.io
1. https://raw.githubusercontent.com/sovrin-foundation/sovrin/stable/sovrin/pool_transactions_sandbox_genesis


# Indyscan
O indyscan-daemon verifica o razão para novas transações. As transações são armazenadas no Elasticsearch. indyscan-api fornece um wrapper de API HTTP fácil de usar em torno do Elasticsearch. indyscan-webapp conversa com a api e exibe a transação do razão como páginas html.

O blockchain público IndyScan for Sovrin está implantado em :

1. https://indyscan.io/home/SOVRIN_MAINNET
