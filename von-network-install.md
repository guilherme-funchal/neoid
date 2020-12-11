# Instalar a von-network no Ubuntu 18.04

1. instalar o indy
<pre>
pip3 install python3-indy
</pre>

2. Instalar o rockesdb
<pre>
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys CE7709D068DB5E88
sudo add-apt-repository "deb https://repo.sovrin.org/deb xenial master"

sudo apt-get update
sudo apt-get install libbz2-dev \
    zlib1g-dev \
    liblz4-dev \
    libsnappy-dev \
    rocksdb \
    liblz4-dev

</pre>
3. Instalar o indy-plenum
<pre>
pip3 install indy-plenum
</pre>

4. Alterar o /usr/local/lib/python3.7/dist-packages/plenum/common/util.py linha 349
remover linha 349 : 
<pre>
loop.call_soon(asyncio.async, callback(*args, **kwargs))
</pre>
Incluir :
<pre>
if hasattr(asyncio, 'ensure_future'):
  ensure_future = asyncio.ensure_future
else:
  ensure_future =  getattr(asyncio, "async")
loop.call_soon(ensure_future, callback(*args, **kwargs))
</pre>

5. Instalar o indy node
<pre>
pip3 install indy_node
</pre>

6.Incluir o script start_node no /usr/bin

<pre>
#!/usr/bin/python3.7

import sys


from indy_node.utils.node_runner import run_node
from indy_common.config_util import getConfig


if __name__ == "__main__":
    if len(sys.argv) < 6:
        raise Exception("Provide name and two pairs of IP/port for running the node "
                        "and client stacks in form 'node_name node_ip node_port client_ip client_port'")

    config = getConfig()
    self_name = sys.argv[1]
    run_node(config, self_name,
             node_ip=sys.argv[2], node_port=int(sys.argv[3]),
             client_ip=sys.argv[4], client_port=int(sys.argv[5]))

</pre>

7.Incluir o script von_generate_transactions  no /usr/bin

<pre>
#!/bin/bash

rm -rf /var/lib/indy/*

usage () {
  cat <<-EOF

    Used to generate a genesis transaction file.

    Usage:
        $0 [options]

    Options:
    -i <ip address>
        Specify the ip address to use in the genesis transaction file.
    -s <ip addresses>
        Specify a comma delimited list of addresses to use in the genesis transaction file.
    -n <node number>
        Specify the number to use for the given node.
    -h
        Display usage documentation.

    Examples:
        $0 -i x.x.x.x -n y
        $0 -s "a.a.a.a,b.b.b.b,c.c.c.c,d.d.d.d" -n x

        Use with Docker Compose:
        export DOCKERHOST=x.x.x.x
        $0 -n y
EOF
exit 1
}

options=':i:s:n:h'
while getopts $options option
do
    case $option in
        i  ) ipAddress=$OPTARG;;
        s  ) ipAddresses=$OPTARG;;
        n  ) nodeNum=$OPTARG;;
        h  ) usage; exit;;
        \? ) echo -e "Unknown option: -$OPTARG" >&2; exit 1;;
        :  ) echo -e "Missing option argument for -$OPTARG" >&2; exit 1;;
        *  ) echo -e "Unimplemented option: -$OPTARG" >&2; exit 1;;
    esac
done

genesisFileName=${genesisFileName:-pool_transactions_genesis}
genesisFileBackupName=${genesisFileBackupName:-${genesisFileName}.old}
genesisFileTemplateDir=${genesisFileTemplateDir:-/home/indy/.indy-cli/networks/sandbox}
genesisFileTemplatePath=${genesisFileTemplatePath:-${genesisFileTemplateDir}/${genesisFileName}}
genesisFileTemplateBackupPath=${genesisFileTemplateBackupPath:-${genesisFileTemplateDir}/${genesisFileBackupName}}

ledgerDir=${ledgerDir:-/home/indy/ledger}
genesisFileDir=${genesisFileDir:-${ledgerDir}/sandbox}
genesisFilePath=${genesisFilePath:-${genesisFileDir}/${genesisFileName}}

nodeArg=""
if [ ! -z "$nodeNum" ]; then
    # Only run this for nodes:
    nodeArg="--nodeNum $nodeNum"

    #echo -e \\n\\n"================================================================================================"
    #echo -e "Initializing Node $nodeNum:"
    #echo -e init_indy_keys --name "Node$nodeNum"
    #echo -e "------------------------------------------------------------------------------------------------"
    #init_indy_keys --name "Node$nodeNum"
    #echo -e "================================================================================================"
fi

if [ ! -z $ipAddresses ]; then
    ipsArg="$ipAddresses"
elif [ ! -z $ipAddress ]; then
    ipsArg="$ipAddress","$ipAddress","$ipAddress","$ipAddress"
else
    ipsArg="$DOCKERHOST","$DOCKERHOST","$DOCKERHOST","$DOCKERHOST"
fi

echo -e \\n\\n"================================================================================================"
echo -e "Generating genesis transaction file:"
echo -e "nodeArg: ${nodeArg}"
echo -e "ipAddresses: ${ipsArg}"
echo -e "genesisFilePath: ${genesisFilePath}"
echo -e "------------------------------------------------------------------------------------------------"
# Use supplied IP address
echo -e generate_indy_pool_transactions \
    --nodes 4 \
    --clients 0 \
    $nodeArg \
    --ips "$ipsArg" \
    \\n

generate_indy_pool_transactions \
    --nodes 4 \
    --clients 0 \
    $nodeArg \
    --ips "$ipsArg"

echo -e \\n"------------------------------------------------------------------------------------------------"
echo -e "Generated genesis transaction file; ${genesisFilePath}"\\n
cat ${genesisFilePath}

if [ ! -z "$remapPorts" ]; then
    echo -e \\n"------------------------------------------------------------------------------------------------"
    echo -e "Changing ports:"
    echo -e "- client_port => 80"
    echo -e "- node_port => 9418"\\n
    echo -e mv ${genesisFileTemplatePath} ${genesisFileTemplateBackupPath}
    mv ${genesisFileTemplatePath} ${genesisFileTemplateBackupPath}
    echo -e "cat ${genesisFileTemplateBackupPath} | sed 's~\(\"client_port\":\).\{4\}\(,\)~\180\2~g' | sed 's~\(\"node_port\":\).\{4\}\(,\)~\19418\2~g' > ${genesisFileTemplatePath}"
    cat ${genesisFileTemplateBackupPath} | sed 's~\(\"client_port\":\).\{4\}\(,\)~\180\2~g' | sed 's~\(\"node_port\":\).\{4\}\(,\)~\19418\2~g' > ${genesisFileTemplatePath}
fi

#echo -e \\n"------------------------------------------------------------------------------------------------"
#echo -e "Initial state of ${genesisFilePath}"\\n
#cat ${genesisFilePath}

#echo -e \\n"------------------------------------------------------------------------------------------------"
#echo -e "Overwriting ..."
#echo -e "cat ${genesisFileTemplatePath} > ${genesisFilePath}"
#cat ${genesisFileTemplatePath} > ${genesisFilePath}

#echo -e \\n"------------------------------------------------------------------------------------------------"
#echo -e "Final genesis transaction file; ${genesisFilePath}"\\n
#cat ${genesisFilePath}

echo -e "================================================================================================"\\n
</pre>

8. Inclusão de arquivos aml.json e taa.json no diretório "/home/indy/config/"

aml.json
<pre>
{
  "version": "1.0",
  "context": "http://aml-context-descr",
  "aml": {
     "product_eula": "The agreement was included in the software product’s terms and conditions as part of a license to the end user.",
     "service_agreement": "The agreement was included in the terms and conditions the user accepted as part of contracting a service.",
     "at_submission": "The agreement was reviewed by the user and accepted at the time of submission of this transaction.",
     "for_session": "The agreement was reviewed by the user and accepted at some point in the user’s session prior to submission.",
     "wallet_agreement": "The agreement was reviewed by the user and this affirmation was persisted in the user’s wallet for use during submission.",
     "on_file": "An authorized person accepted the agreement, and such acceptance is on file with the user’s organization."
  }
}
</pre>

taa.json
<pre>
{
  "version": "1.1",
  "text": "TAA Goes *Here*\n\n- got it",
  "ratification_ts": 1597654073
}
</pre>

