# Redes da BCGov 
Redes públicas que podem ser utilizados para teste : 
1. http://test.bcovrin.vonx.io
1. http://greenlight.bcovrin.vonx.io
1. https://raw.githubusercontent.com/sovrin-foundation/sovrin/stable/sovrin/pool_transactions_sandbox_genesis


# Indyscan
O indyscan-daemon verifica o razão para novas transações. As transações são armazenadas no Elasticsearch. indyscan-api fornece um wrapper de API HTTP fácil de usar em torno do Elasticsearch. indyscan-webapp conversa com a api e exibe a transação do razão como páginas html.

O blockchain público IndyScan for Sovrin está implantado em :

1. https://indyscan.io/home/SOVRIN_MAINNET


# Von-network



** Personalização do navegador do Razão **<br>

É possível personalizar alguns dos aspectos do Ledger Browser em tempo de execução, usando as seguintes variáveis ​​de ambiente:

REGISTER_NEW_DIDS: se definido como True, ele habilitará a interface do usuário permitindo que novos proprietários de identidade gravem um DID no razão. O padrão é False.
LEDGER_INSTANCE_NAME: o nome da instância do razão à qual o Ledger Brwoser está conectado. O padrão é Navegador do razão.
INFO_SITE_URL: um URL que será exibido no cabeçalho e pode ser usado para fazer referência a outro site externo que contém detalhes / recursos na instância do navegador do razão atual.
INFO_SITE_TEXT: o texto de exibição usado para INFO_SITE_URL. Se não for especificado, o padrão será o valor definido para INFO_SITE_URL.
WEB_ANALYTICS_SCRIPT: o código JavaScript usado pelos servidores de análise da web. Preencha esta variável de ambiente se você deseja rastrear o uso do seu site com Matomo, Google Analytics ou qualquer outro rastreador baseado em JavaScript. Inclua toda a tag <script type = "text / javascript"> ... </script>, garantindo que as aspas sejam escapadas corretamente para o seu interpretador de linha de comando (por exemplo: bash, git bash, etc.).
LEDGER_CACHE_PATH: se definido, instruirá o razão a criar um cache em disco, em vez de em memória. A imagem fornece uma pasta para esse fim; $ HOME / .indy_client / ledger-cache. O arquivo deve ser colocado neste diretório (por exemplo: /home/indy/.indy-client/ledger-cache/ledger_cache_file ou $ HOME / .indy_client / ledger-cache / ledger_cache_file).
