curl -X POST https://bsc-dataseed1.ninicoin.io/ -H "Content-Type: application/json" --data '
{
	  "jsonrpc": "2.0",
	    "method": "eth_getBalance",
	      "params": ["0x2465176C461AfB316ebc773C61fAEe85A6515DAA", "latest"],
	        "id": 1
	}
'
echo ""
