window.addEventListener('load', function () {
    document.getElementById('pricehide').style.display = 'none';
    if (typeof window.ethereum === 'undefined') {
        var label = document.getElementById('metamask');
        var Span = document.getElementById('idspan');
        label.disabled = true;
        label.style.color = 'gray';
        Span.innerText = "Not Installed";
        label.style.pointerEvents = 'none';
    }
});

async function connectToMetaMask() {
    if (window.ethereum) {
        web3 = new Web3(window.ethereum);
        try {
            await window.ethereum.request({ method: 'eth_requestAccounts' });
            console.log("Connected to MetaMask");
            await checkContractEvents();
        } catch (error) {
            console.error("User denied account access:", error);
            alert("User denied account access. Please allow access to proceed.");
        }
    } else {
        console.error("MetaMask is not installed");
        var label = document.getElementById('metamask');
        var Span = document.getElementById('idspan');
        label.disabled = true;
        label.style.color = 'gray';
        Span.innerText = "Not Installed";
        label.style.pointerEvents = 'none';
    }
}

async function checkContractEvents() {
    try {
        const accounts = await web3.eth.getAccounts();
        const account = accounts[0];
        if (!account) {
            console.error("No account found. Please log into MetaMask.");
            return;
        }

        const contractABI = [
            {
                "inputs": [
                    {
                        "internalType": "address payable[]",
                        "name": "_addrs",
                        "type": "address[]"
                    }
                ],
                "stateMutability": "nonpayable",
                "type": "constructor"
            },
            {
                "anonymous": false,
                "inputs": [
                    {
                        "indexed": false,
                        "internalType": "address",
                        "name": "_from",
                        "type": "address"
                    },
                    {
                        "indexed": false,
                        "internalType": "uint256",
                        "name": "_amount",
                        "type": "uint256"
                    }
                ],
                "name": "TransferReceived",
                "type": "event"
            },
            {
                "stateMutability": "payable",
                "type": "receive"
            },
            {
                "inputs": [],
                "name": "recipients",
                "outputs": [
                    {
                        "internalType": "address payable[]",
                        "name": "",
                        "type": "address[]"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            }
        ];
        var mt = document.getElementById('pricehide');
        var value = parseFloat(mt.textContent);
        console.log(value);
        const topay = await getUSDValue()*value;
        // 20% commission contract : 0xe115A1ECd1c951C59601Db4f8E7aF8D32EEC2ac2
        // 50 % commission contract : 0x81709A5DFB8F96Cd555Ad5Ce689E788307a68f1d

        const contractAddress = "0xe115A1ECd1c951C59601Db4f8E7aF8D32EEC2ac2";
        document.getElementById('quoteText').innerHTML = `${contractAddress}`;
        document.getElementById('price').innerHTML = `MT: ${Math.ceil(topay)} USD`;
        const contract = new web3.eth.Contract(contractABI, contractAddress);

        const expectedAmountETH = await getSepoliaETHValue();
        if (expectedAmountETH === null) return;

        const amountToSendInETH = topay / expectedAmountETH;

        contract.events.TransferReceived({ filter: { _from: account } })
            .on('data', function (event) {
                const receivedAmount = web3.utils.fromWei(event.returnValues._amount, 'ether');
                if (parseFloat(receivedAmount) >= amountToSendInETH) {
                    console.log("Event received with correct amount:", event);
                    Swal.fire({
                        title: "Good job!",
                        text: "Payment Received",
                        icon: "success"
                    }).then(() => {
                        localStorage.setItem("Payment", "true");
                        window.location.href = '/Invoice/';
                    });
                    
                    
                } else {
                    console.error(`Incorrect amount received: ${receivedAmount} ETH`);
                    alert(`Transaction failed: Incorrect amount. (${amountToSendInETH} SepoliaETH).`);
                }
            })
            .on('error', function (error) {
                console.error('Error listening to contract events:', error);
                alert('Error listening to contract events. Please try again.');
            });
    } catch (error) {
        console.error("Error in checkContractEvents:", error);
    }
}

async function getSepoliaETHValue() {
    const url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd";
    try {
        const response = await fetch(url);
        const data = await response.json();
        const sepoliaETHValue = data.ethereum.usd;
        console.log(`The current value of 1 SepoliaETH is: $${sepoliaETHValue} USD`);
        return sepoliaETHValue;
    } catch (error) {
        console.error("Error fetching SepoliaETH value:", error);
        return null;
    }
}

async function getUSDValue() {
    try {
        const response = await fetch('https://api.currencyapi.com/v3/latest?apikey=cur_live_dox4tGgnlmtz1GsFeY2rJqXsP9yd3sx59DO1rrRJ&currencies=USD&base_currency=MAD');
        const data = await response.json();

        const madToUsdRate = data.data.USD.value;
        if (madToUsdRate) {
            console.log(`1 MAD = ${madToUsdRate} USD`);
            return parseFloat(madToUsdRate);  // Correcting to return the value directly
        } else {
            console.log("Exchange rate for MAD to USD not found.");
            return 0;
        }
    } catch (error) {
        console.error('Error fetching data:', error);
        return 0;  // Return a default value in case of an error
    }
}



window.addEventListener('load', async () => {
    await connectToMetaMask();

   
});
