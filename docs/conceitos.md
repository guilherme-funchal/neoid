# Conceitos

**Agentes**<br>
Um agente hospedado na nuvem. Ele normalmente opera em um dispositivo de computação sobre o qual o Proprietário da identidade não tem controle físico direto ou acesso. Mutuamente exclusivo com o Edge Agent. Um Agente em Nuvem requer uma Carteira e normalmente tem um Terminal de Serviço. Os agentes de nuvem podem ser hospedados por uma agência

**Credencial**<br>
Uma declaração digital que contém um conjunto de reivindicações feitas por uma entidade sobre si mesma ou outra entidade. Credenciais são um subconjunto de dados de identidade. Uma credencial é baseada em uma definição de credencial. A Entidade descrita pelas Reivindicações é chamada de Assunto da Credencial. A entidade que cria a credencial é chamada de emissor. A Entidade que detém a Credencial emitida é denominada Titular. Se a credencial for compatível com provas de conhecimento zero, o titular também é chamado de provedor. A Entidade para a qual uma Credencial é apresentada é geralmente chamada de Parte Confiante e, especificamente, de Verificador se a Credencial for uma Credencial Verificável. Uma vez emitida, uma credencial é normalmente armazenada por um Agente. 

**Conexão**<br>
Um canal de comunicação criptograficamente verificável estabelecido usando um Protocolo Agente a Agente entre dois DIDs representando duas Entidades e seus Agentes associados. As conexões podem ser de ponta a ponta ou de nuvem a nuvem. As conexões podem ser usadas para trocar credenciais verificáveis ou para qualquer outro propósito de comunicação. As conexões podem ser criptografadas e descriptografadas usando as Chaves Públicas e Chaves Privadas para cada DID. Uma Conexão pode ser temporária ou pode durar enquanto as duas Entidades desejarem mantê-la. Duas Entidades podem ter várias Conexões entre elas, no entanto, cada Conexão deve estar entre um par exclusivo de DIDs. Um relacionamento entre mais de duas Entidades pode ser modelado como conexões Pairwise entre todas as Entidades (Peering) ou cada Entidade pode formar uma Conexão com uma Entidade que representa um Grupo.

**Node**<br>
Um servidor de rede de computadores executando uma instância do código necessário para operar um razão distribuído ou blockchain. 
Na infraestrutura do Sovrin, um nó é operado por um administrador executando uma instância do código-fonte aberto do Sovrin para manter o Ledger do Sovrin. 
Um Nó deve ser um Nó Validador ou Nó Observador.

**Base de Código**<br>
A base de código é administrada Conselho de Governança Técnica Sovrin e distribuída sob uma Licença de Código Aberto para operar nós, carteiras e agentes. O Código-fonte aberto Sovrin é atualmente mantido principalmente no Projeto Hyperledger Indy gerenciado pela Linux Foundation e, secundariamente, no Repositório de Código Sovrin gerenciado pela Fundação Sovrin.

**Hyperledger**<br>
Um projeto de código aberto sob a égide do Hyperledger para identidade auto-soberana descentralizada. O código-fonte do Hyperledger Indy foi contribuído originalmente para a Linux Foundation pela Sovrin Foundation. Sovrin Stewards executa o software Hyperledger Indy Node para operar seus Nodes. A página inicial do Hyperledger Indy é https://wiki.hyperledger.org/display/indy.

**DID**<br>
Um identificador globalmente exclusivo desenvolvido especificamente para sistemas descentralizados conforme definido pela especificação W3C DID. Os DIDs permitem o gerenciamento de identidade autossoberana e descentralizada e interoperável. Um DID está associado a exatamente um Documento DID. 

**Proof**<nr>
Verificação criptográfica de uma reivindicação ou credencial. Uma assinatura digital é uma forma simples de prova. Um hash criptográfico também é uma forma de prova. As Provas de Conhecimento Zero permitem a divulgação seletiva das informações em uma Credencial.

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

**Protocolo de concenso**<br>
O protocolo tolerante a falhas bizantino usado para se comunicar entre os nós para manter os Ledgers.

**Ledger**<br>
Livro razão verificável.

**Governança**<br>
O próximo passo na escada do fortalecimento e aumento da confiança é estabelecer uma Autoridade de Governança formal e publicar uma Estrutura de Governança oficial. Este é o passo que a Fundação Sovrin deu a partir de setembro de 2016, com sua incorporação formal, após a qual o Grupo de Trabalho da Estrutura de Governança do Sovrin tem trabalhado desde então.

**Zero Knowledge Proof**<br>
Uma prova que usa criptografia especial e um segredo de link para oferecer suporte à divulgação seletiva de informações sobre um conjunto de reivindicações de um conjunto de credenciais. A Zero Knowledge Proof fornece prova criptográfica sobre alguns ou todos os dados em um conjunto de credenciais sem revelar os dados reais ou qualquer informação adicional, incluindo a identidade do provador.

**Issuer**<br>
A entidade que emite uma credencial a um titular. Com base na definição fornecida pelo Grupo de Trabalho de Reivindicações Verificáveis do W3C

**Revocation**<br>
O ato de um Emissor revogar a validade de uma Reivindicação ou Credencial. Com o Protocolo Sovrin e o Razão Sovrin, a revogação é realizada usando um Registro de Revogação.

**Identidade SSI**<br>
Uma arquitetura de sistema de identidade baseada no princípio básico de que os Proprietários de Identidade têm o direito de controlar permanentemente um ou mais Identificadores junto com o uso dos Dados de Identidade associados. A Estrutura de Governança do Sovrin especifica dois tipos de Proprietários de Identidade: Independentes, que não precisam depender de nenhuma autoridade administrativa externa; e Dependentes, que precisam contar com um Guardião.

**Schema**<br>
Uma definição legível por máquina da semântica de uma estrutura de dados. Os esquemas são usados para definir os atributos usados em uma ou mais definições de credencial.

**Von-network**<br>
Uma rede Indy Node de nível de desenvolvimento, incluindo um navegador Ledger. O Navegador do Razão (por exemplo, o Razão do BC Gov para o aplicativo de demonstração GreenLight) permite que um usuário veja o status dos nós de uma rede e navegue / pesquise / filtre as transações do razão. A von-network está sendo desenvolvida como parte da Verifiable Organizations Network (VON). 
Fonte : https://github.com/bcgov/von-network

**Wallet**<br>
Um módulo de software e, opcionalmente, um módulo de hardware associado, para armazenar e acessar com segurança Chaves Privadas, Segredos de Link, outro material 
de chave criptográfica sensível e outros Dados Privados usados por uma Entidade. Uma Carteira é acessada por um Agente. Na infraestrutura do Sovrin, as carteiras 
implementam os padrões DKMS emergentes para gerenciamento de chaves criptográficas descentralizadas e interoperáveis.

Origem : https://raw.githubusercontent.com/sovrin-foundation/sovrin/stable/sovrin/pool_transactions_live_genesis

Fonte : https://docs.google.com/document/d/1gfIz5TT0cNp2kxGMLFXr19x1uoZsruUe_0glHst2fZ8/edit#
