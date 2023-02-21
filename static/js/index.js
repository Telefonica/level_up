let base_add = '{{base_address}}';
let abi = JSON.parse('{{abi_base | tojson | safe}}');

async function Web3Prov(){
    const provider = new ethers.providers.Web3Provider(window.ethereum); 
    await provider.send("eth_requestAccounts", []);
    const address = await provider.getSigner().getAddress();
    const add = document.getElementById('link_to_user');
    add.href = "/playerOptions?user_address=" + address;

    base = new ethers.Contract(
        base_add,
        abi,
        provider.getSigner(0)
    );

    window.base = base;
    window.player = address;
}

function help(){
    console.table({player:'Devuelve la dirección pública del jugador',
    base:'Acceso a contrato base del juego',
    contract:'Interactúa con el contrato cuando lo despliegues'});
}

// REVIEW THIS
window.userWalletAddress = null;
const connectWallet = document.getElementById('connectWallet');
const walletAddress = document.getElementById('walletAddress');
const walletBalance = document.getElementById('walletBalance');


function checkInstalled() {
    if (typeof window.ethereum == 'undefined') {
        connectWallet.innerText = 'MetaMask isnt installed, please install it'
        connectWallet.classList.remove()
        connectWallet.classList.add()
        return false
    }
}

async function connectWalletwithMetaMask() {
    const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' })
    .catch((e) => {
    console.error(e.message)
    return
    })

    if (!accounts) { return }

    window.userWalletAddress = accounts[0]
    window.player = accounts[0]
    walletAddress.innerText = window.userWalletAddress

    connectWallet.innerText = 'Sign Out'
    connectWallet.removeEventListener('click', connectWalletwithMetaMask)
    setTimeout(() => {
        connectWallet.addEventListener('click', signOutOfMetaMask)
    }, 200)
}

function signOutOfMetaMask() {
    window.userwalletAddress = null
    walletAddress.innerText = ''
    connectWallet.innerText = 'Connect Wallet'

    connectWallet.removeEventListener('click', signOutOfMetaMask)
    setTimeout(() => {
        connectWallet.addEventListener('click', connectWalletwithMetaMask)
    }, 200 )
}

async function checkBalance() {
    let balance = await window.ethereum.request({ method: "eth_getBalance",
    params: [
        window.userWalletAddress,
        'latest'
    ]
    }).catch((err)=> {
        console.log(err)
    })

    console.log(parseFloat((balance) / Math.pow(10,18)))

    walletBalance.innerText = parseFloat((balance) / Math.pow(10,18))
}

window.addEventListener('DOMContentLoaded', () => {
    checkInstalled()
})
