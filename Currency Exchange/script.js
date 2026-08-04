const countryList = {
  AED: "AE",
  AFN: "AF",
  XCD: "AG",
  ALL: "AL",
  AMD: "AM",
  ANG: "AN",
  AOA: "AO",
  AQD: "AQ",
  ARS: "AR",
  AUD: "AU",
  AZN: "AZ",
  BAM: "BA",
  BBD: "BB",
  BDT: "BD",
  XOF: "BE",
  BGN: "BG",
  BHD: "BH",
  BIF: "BI",
  BMD: "BM",
  BND: "BN",
  BOB: "BO",
  BRL: "BR",
  BSD: "BS",
  NOK: "BV",
  BWP: "BW",
  BYR: "BY",
  BZD: "BZ",
  CAD: "CA",
  CDF: "CD",
  XAF: "CF",
  CHF: "CH",
  CLP: "CL",
  CNY: "CN",
  COP: "CO",
  CRC: "CR",
  CUP: "CU",
  CVE: "CV",
  CYP: "CY",
  CZK: "CZ",
  DJF: "DJ",
  DKK: "DK",
  DOP: "DO",
  DZD: "DZ",
  ECS: "EC",
  EEK: "EE",
  EGP: "EG",
  ETB: "ET",
  EUR: "FR",
  FJD: "FJ",
  FKP: "FK",
  GBP: "GB",
  GEL: "GE",
  GGP: "GG",
  GHS: "GH",
  GIP: "GI",
  GMD: "GM",
  GNF: "GN",
  GTQ: "GT",
  GYD: "GY",
  HKD: "HK",
  HNL: "HN",
  HRK: "HR",
  HTG: "HT",
  HUF: "HU",
  IDR: "ID",
  ILS: "IL",
  INR: "IN",
  IQD: "IQ",
  IRR: "IR",
  ISK: "IS",
  JMD: "JM",
  JOD: "JO",
  JPY: "JP",
  KES: "KE",
  KGS: "KG",
  KHR: "KH",
  KMF: "KM",
  KPW: "KP",
  KRW: "KR",
  KWD: "KW",
  KYD: "KY",
  KZT: "KZ",
  LAK: "LA",
  LBP: "LB",
  LKR: "LK",
  LRD: "LR",
  LSL: "LS",
  LTL: "LT",
  LVL: "LV",
  LYD: "LY",
  MAD: "MA",
  MDL: "MD",
  MGA: "MG",
  MKD: "MK",
  MMK: "MM",
  MNT: "MN",
  MOP: "MO",
  MRO: "MR",
  MTL: "MT",
  MUR: "MU",
  MVR: "MV",
  MWK: "MW",
  MXN: "MX",
  MYR: "MY",
  MZN: "MZ",
  NAD: "NA",
  XPF: "NC",
  NGN: "NG",
  NIO: "NI",
  NPR: "NP",
  NZD: "NZ",
  OMR: "OM",
  PAB: "PA",
  PEN: "PE",
  PGK: "PG",
  PHP: "PH",
  PKR: "PK",
  PLN: "PL",
  PYG: "PY",
  QAR: "QA",
  RON: "RO",
  RSD: "RS",
  RUB: "RU",
  RWF: "RW",
  SAR: "SA",
  SBD: "SB",
  SCR: "SC",
  SDG: "SD",
  SEK: "SE",
  SGD: "SG",
  SKK: "SK",
  SLL: "SL",
  SOS: "SO",
  SRD: "SR",
  STD: "ST",
  SVC: "SV",
  SYP: "SY",
  SZL: "SZ",
  THB: "TH",
  TJS: "TJ",
  TMT: "TM",
  TND: "TN",
  TOP: "TO",
  TRY: "TR",
  TTD: "TT",
  TWD: "TW",
  TZS: "TZ",
  UAH: "UA",
  UGX: "UG",
  USD: "US",
  UYU: "UY",
  UZS: "UZ",
  VEF: "VE",
  VND: "VN",
  VUV: "VU",
  YER: "YE",
  ZAR: "ZA",
  ZMK: "ZM",
  ZWD: "ZW",
};




// just for the headbar
const currencyPairs = [
    { from: "USD", to: "EUR" },
    { from: "GBP", to: "USD" },
    { from: "USD", to: "JPY" },
    { from: "USD", to: "PKR" },
    { from: "EUR", to: "GBP" },
    { from: "USD", to: "AED" },
    { from: "USD", to: "INR" },
    { from: "AUD", to: "USD" },
    { from: "USD", to: "EUR" },
    { from: "GBP", to: "USD" },
    { from: "USD", to: "JPY" },
    { from: "USD", to: "PKR" },
    { from: "EUR", to: "GBP" },
    { from: "USD", to: "AED" },
    { from: "USD", to: "INR" },
    { from: "AUD", to: "USD" }
];




// Updating the headbar live rates
let headBar = document.querySelector(".ticker-track");

async function getUpdatedAmounts() {
    for(let el of currencyPairs) {
        const span = document.createElement("span");
        span.textContent = `${el.from} / ${el.to} `;
        span.classList.add("ticker-item");
        const b = document.createElement("b");
        const URL = `https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/${el.from.toLowerCase()}.json`;
        let response = await fetch(URL);
        let data = await response.json();
        let rate = data[el.from.toLowerCase()][el.to.toLowerCase()];
        b.textContent = rate.toFixed(3);
        span.append(b);
        headBar.append(span);
    }
}

getUpdatedAmounts();




// Adding all the available country and currency codes 
let dropdowns = document.querySelectorAll("main select");

for(let select of dropdowns) {
    for(let currCode in countryList) {
        let newOption = document.createElement("option");
        newOption.innerText = currCode;
        newOption.value = currCode;
        if(select.id === "currency-from" && currCode === "USD") {
            newOption.selected = "selected";
        }
        else if(select.id === "currency-to" && currCode === "PKR") {
            newOption.selected = "selected";
        }
        select.append(newOption);
    }
}




// Making quick amounts functional
let quickAmount = document.querySelector(".quick-amounts");

function updateQuickAmount(event) {
    let amount = document.querySelector("#amount-from");
    amount.value = event;
}

quickAmount.addEventListener("click", (evt) => {
    updateQuickAmount(evt.target.dataset.amount);
});




// Updating flags according to the countries selected
let selectto = document.querySelector("#currency-to");
let selectFrom = document.querySelector("#currency-from");

function updateFlagTo(event) {
    let currCode = event.value;
    let countryCode = countryList[currCode];
    let newSRC = `https://flagsapi.com/${countryCode}/flat/64.png`;
    let img = document.querySelector("#flag-to");
    img.src = newSRC;
}

function updateFlagFrom(event) {
    let currCode = event.value;
    let countryCode = countryList[currCode];
    let newSRC = `https://flagsapi.com/${countryCode}/flat/64.png`;
    let img = document.querySelector("#flag-from");
    img.src = newSRC;
}

selectto.addEventListener("change", (evt) => {
    updateFlagTo(evt.target);
});

selectFrom.addEventListener("change", (evt) => {
    updateFlagFrom(evt.target);
});


// The main logic for conversion and calling API
let fromCurr = document.querySelector("#currency-from");
let toCurr = document.querySelector("#currency-to");
let btn = document.querySelector("#convert-btn");
let convertedAmount = document.querySelector("#amount-to");

btn.addEventListener("click", async (evt) => {
    evt.preventDefault();
    let amount = document.querySelector("#amount-from");
    let amtVal = amount.value;
    if(amtVal === "" || amtVal < 1) {
        amtVal = 1;
        amount.value = "1";
    }
    const URL = `https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/${fromCurr.value.toLowerCase()}.json`;
    let response = await fetch(URL);
    let data = await response.json();
    let rate = data[fromCurr.value.toLowerCase()][toCurr.value.toLowerCase()];
    let finalAmount = amtVal * rate;
    convertedAmount.value = finalAmount;
});



// Updating the rate strip at the last
async function usd_pkr() {
    let rateStrip = document.querySelector("#rate-strip");
    const span = document.createElement("span");
    span.id = "rate-display";
    span.classList.add("rate-eq");
    const URL = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json";
    let response = await fetch(URL);
    let data = await response.json();
    let rate = data["usd"]["pkr"];
    span.textContent = `1 USD = ${rate.toFixed(2)} PKR`;
    rateStrip.prepend(span);
}

usd_pkr();
