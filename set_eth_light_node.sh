wget https://gethstore.blob.core.windows.net/builds/geth-linux-386-1.10.8-26675454.tar.gz
tar -xvf geth-linux-386-1.10.8-26675454.tar.gz
mv geth-linux-386-1.10.8-26675454 geth
CURRDIR=$(pwd)
cd
echo "PATH=$PATH:$CURRDIR/geth" >> .bashrc
PATH=$PATH:$CURRDIR/geth
export PATH
cd $CURRDIR
nohup geth --rpc --rpcport 8550 --http --syncmode light &
jobs -i
