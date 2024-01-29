// const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));
const BINANCE_API_URL = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT';
const EXCHANGE = ["binance", "bybit"];
const SYMBOL = "BTC";
const WALLET = { "USDT": 1000000, "BTC": 0 };
const STARTWALLET = WALLET["USDT"];
const RANGE = 10000;
let range = 10
const start_time = Date.now();
const seconds_in_a_week = 7 * 24 * 60 * 60;

// Renvoie un fichien JSON contenant le résultat de la requete
async function get_request(url) {
    return fetch(url)
        .then(response => response.json())
        .catch(error => console.error(`Erreur lors de la requete url : ${error.message}`));
}
// Renvoie le prix du token sur l'exchange
async function get_price_symbol(exchange, symbol) {
    try {
        // BINANCE
        if (exchange === "binance") {
            const url = `https://api.binance.com/api/v3/ticker/price?symbol=${symbol}USDT`;
            const data = await get_request(url);
            let last_price = data.price;
            last_price = parseFloat(last_price).toFixed(2)
            // difference entre le prix actuel et le prix de départ
            price.textContent = last_price;

            return last_price;
            // BYBIT
        } else if (exchange === "bybit") {
            const url = `https://api.bybit.com/v2/public/tickers?symbol=${symbol}USDT`;
            const data = await get_request(url);
            let last_price = data.result[0].last_price;
            last_price = parseFloat(last_price).toFixed(2)
            // difference entre le prix actuel et le prix de départ
            price.textContent = last_price;

            return last_price;
        }
    } catch (e) {
        console.log("Erreur lors de la récupération du prix :");
        console.log(e);
    }
}

// Achat d'un token
async function buy_token(token, last_price) {
    try {
        console.log("####################")
        console.log("######  BUY  #######")
        let amountDollars = WALLET["USDT"]; // On récupère le montant de dollars dans le portefeuille
        let amountToken = amountDollars / last_price; // On calcule le montant de token que l'on peut acheter
        WALLET["USDT"] -= amountDollars; // On retire les dollars du portefeuille
        WALLET[token] += amountToken; // On ajoute les tokens au portefeuille
        console.log(WALLET);
        console.log("####################")
        console.log("\n")
    } catch (e) {
        console.log("Erreur lors de l'achat :");
        console.log(e);
    }
}
async function sell_token(token, last_price) {
    try {
        console.log("####################")
        console.log("###### SELL ########")
        let amountToken = WALLET[token]; // On récupère le montant de token dans le portefeuille
        let amountDollars = amountToken * last_price; // On calcule le montant de dollars que l'on peut vendre
        WALLET["USDT"] += amountDollars; // On ajoute les dollars au portefeuille
        WALLET[token] -= amountToken; // On retire les tokens du portefeuille
        console.log(WALLET);
        const diff = parseFloat(WALLET["USDT"] - STARTWALLET).toFixed(2); // On calcule la différence entre le portefeuille actuel et le portefeuille de départ
        console.log(diff > 0 ? `Gain : ${diff} USDT` : `Perte : ${diff} USDT`) // On affiche le gain ou la perte
        gain.textContent = diff > 0 ? `Gain : ${diff} USDT` : `Perte : ${diff} USDT`;
        console.log("####################")
        console.log("\n")
    } catch (e) {
        console.log("Erreur lors de la vente :");
        console.log(e);
    }
}
// Attend un certain temps
async function wait(timer) {
    return new Promise(resolve => {
        setTimeout(resolve, timer);
    });
}
async function randomBuySell() {
    try {
        let last_price = await get_price_symbol(EXCHANGE[0], SYMBOL); // On récupère le prix du token sur l'exchange
        buy_token(SYMBOL, last_price); // On achète le token
        await wait(range * 1000); // On attend un certain temps
        last_price = await get_price_symbol(EXCHANGE[0], SYMBOL); // On récupère le prix du token sur l'exchange
        sell_token(SYMBOL, last_price); // On vend le token
    } catch (e) {
        console.log("Erreur lors de l'achat ou de la vente :");
        console.log(e);
    }
}

async function main() {
    try {
        while (Date.now() - start_time < seconds_in_a_week * 1000) { // Tant que le temps n'est pas écoulé
            await randomBuySell(); // On achète et on vend le token
        }
        console.log("Fin de la simulation");
        console.log(`Gain : ${WALLET["USDT"] - STARTWALLET} USDT`);
    } catch (e) {
        console.log("Erreur lors du main :");
        console.log(e);
    }
}

main();