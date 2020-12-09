# Instalar a von-network no Ubuntu 18.04

1. instalar o indy
<pre>
pip3 install python3-indy
</pre>

2. Instalar o rockesdb
<pre>
$ apt-get install build-essential libsnappy-dev zlib1g-dev libbz2-dev libgflags-dev liblz4-dev
$ git clone https://github.com/facebook/rocksdb.git
$ cd rocksdb
$ mkdir build && cd build
$ cmake ..
$ make
$ cd ..
$ export CPLUS_INCLUDE_PATH=${CPLUS_INCLUDE_PATH}${CPLUS_INCLUDE_PATH:+:}`pwd`/include/
$ export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}${LD_LIBRARY_PATH:+:}`pwd`/build/
$ export LIBRARY_PATH=${LIBRARY_PATH}${LIBRARY_PATH:+:}`pwd`/build/

$ apt-get install python-virtualenv python-dev
$ virtualenv pyrocks_test
$ cd pyrocks_test
$ . bin/active
$ pip install python-rocksdb
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
<pre>

4. Instalar o indy node
<pre>
pip3 install indy_node
</pre>

5.Incluir o script start_node no /usr/bin

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

6.Incluir o script von_generate_transactions  no /usr/bin

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
