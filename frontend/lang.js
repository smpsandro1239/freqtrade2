const translations = {
    'pt-PT': {
        title: 'Gráficos TradingView-like com Indicadores',
        settings: 'Configurações',
        symbol: 'Par de Moedas:',
        interval: 'Intervalo:',
        loadChart: 'Carregar Gráfico',
        indicators: 'Indicadores',
        tradingAutomation: 'Automação de Trading',
        startTrading: 'Iniciar Trading',
        stopTrading: 'Parar Trading',
        balance: 'Saldo',
        minute: 'Minuto',
        minutes: 'Minutos',
        hour: 'Hora',
        hours: 'Horas',
        day: 'Dia',
        tradingStarted: 'Trading iniciado!',
        tradingStopped: 'Trading parado!',
        tradeHistory: 'Histórico de Trades',
        noTrades: 'Nenhum trade realizado',
        errorLoading: 'Erro ao carregar',
        paperTrade: 'Paper',
        realTrade: 'Real'
    },
    'en': {
        title: 'TradingView-like Charts with Indicators',
        settings: 'Settings',
        symbol: 'Symbol:',
        interval: 'Interval:',
        loadChart: 'Load Chart',
        indicators: 'Indicators',
        tradingAutomation: 'Trading Automation',
        startTrading: 'Start Trading',
        stopTrading: 'Stop Trading',
        balance: 'Balance',
        minute: 'Minute',
        minutes: 'Minutes',
        hour: 'Hour',
        hours: 'Hours',
        day: 'Day',
        tradingStarted: 'Trading started!',
        tradingStopped: 'Trading stopped!',
        tradeHistory: 'Trade History',
        noTrades: 'No trades performed',
        errorLoading: 'Loading error',
        paperTrade: 'Paper',
        realTrade: 'Real'
    }
};

let currentLang = 'pt-PT';

function setLanguage(lang) {
    currentLang = lang;
    updateTexts();
}

function t(key) {
    return translations[currentLang][key] || key;
}

function updateTexts() {
    document.querySelector('h1').textContent = t('title');
    document.querySelector('h4').textContent = t('settings');
    document.querySelector('label[for="symbol"]').textContent = t('symbol');
    document.querySelector('label[for="interval"]').textContent = t('interval');
    document.querySelector('button[onclick="loadChart()"]').textContent = t('loadChart');
    document.querySelectorAll('h4')[1].textContent = t('indicators');
    document.querySelectorAll('h4')[2].textContent = t('tradingAutomation');
    document.querySelector('button[onclick="startTrading()"]').textContent = t('startTrading');
    document.querySelector('button[onclick="stopTrading()"]').textContent = t('stopTrading');
    document.querySelector('h5').textContent = t('balance');

    // Update interval options
    const intervalSelect = document.getElementById('interval');
    if (intervalSelect) {
        intervalSelect.options[0].textContent = `1 ${t('minute')}`;
        intervalSelect.options[1].textContent = `5 ${t('minutes')}`;
        if (intervalSelect.options[2]) intervalSelect.options[2].textContent = `15 ${t('minutes')}`;
        intervalSelect.options[intervalSelect.options.length - 3].textContent = `1 ${t('hour')}`;
        if (intervalSelect.options.length > 4) intervalSelect.options[intervalSelect.options.length - 2].textContent = `4 ${t('hours')}`;
        intervalSelect.options[intervalSelect.options.length - 1].textContent = `1 ${t('day')}`;
    }

    // Update trade history title
    const tradeHistoryTitle = document.getElementById('trade-history-title');
    if (tradeHistoryTitle) {
        tradeHistoryTitle.textContent = t('tradeHistory');
    }
}

// Language selector
function createLanguageSelector() {
    const selector = document.createElement('select');
    selector.className = 'form-control mb-3';
    selector.onchange = (e) => setLanguage(e.target.value);

    const ptOption = document.createElement('option');
    ptOption.value = 'pt-PT';
    ptOption.textContent = 'Português';
    ptOption.selected = true;

    const enOption = document.createElement('option');
    enOption.value = 'en';
    enOption.textContent = 'English';

    selector.appendChild(ptOption);
    selector.appendChild(enOption);

    const container = document.querySelector('.container-fluid');
    container.insertBefore(selector, container.firstChild.nextSibling);
}

document.addEventListener('DOMContentLoaded', () => {
    createLanguageSelector();
    updateTexts();
});
