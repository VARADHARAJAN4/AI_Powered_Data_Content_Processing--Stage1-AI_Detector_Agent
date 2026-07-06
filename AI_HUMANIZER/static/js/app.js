const inputText = document.getElementById('inputText');
const outputText = document.getElementById('outputText');
const analyzeBtn = document.getElementById('analyzeBtn');
const clearBtn = document.getElementById('clearBtn');
const copyBtn = document.getElementById('copyBtn');
const status = document.getElementById('status');
const spinner = document.getElementById('spinner');
const resultsSection = document.getElementById('resultsSection');
const originalScore = document.getElementById('originalScore');
const rewrittenScore = document.getElementById('rewrittenScore');
const similarityScore = document.getElementById('similarityScore');
const readabilityGrade = document.getElementById('readabilityGrade');
const grammarScore = document.getElementById('grammarScore');
const aiSourceResult = document.getElementById('aiSourceResult');
const sourceTypeResult = document.getElementById('sourceTypeResult');
const wordCount = document.getElementById('wordCount');
const charCount = document.getElementById('charCount');
const processingTime = document.getElementById('processingTime');
const downloadLink = document.getElementById('downloadLink');
let metricsChart = null;
const chkOriginal = document.getElementById('chkOriginal');
const chkRewritten = document.getElementById('chkRewritten');
const chkSimilarity = document.getElementById('chkSimilarity');
const chkGrammar = document.getElementById('chkGrammar');
const toggleStacked = document.getElementById('toggleStacked');
const clearHistoryBtn = document.getElementById('clearHistory');
const historySizeSelect = document.getElementById('historySize');

const STORAGE_KEY = 'ai_humanizer_history_v1';
let history = [];
let stacked = false;

function loadHistory() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) history = JSON.parse(raw);
  } catch (e) { history = []; }
}

function saveHistory() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(history)); } catch (e) {}
}

function pushToHistory(item) {
  const maxLen = parseInt(historySizeSelect.value || '20', 10);
  history.push(item);
  if (history.length > maxLen) history = history.slice(-maxLen);
  saveHistory();
}

function buildDatasets() {
  const labels = history.map((h, i) => h.label || (new Date(h.ts)).toLocaleTimeString());
  const originalData = history.map(h => h.original_score || 0);
  const rewrittenData = history.map(h => h.rewritten_score || 0);
  const similarityData = history.map(h => h.similarity_score || 0);
  const grammarData = history.map(h => h.grammar_score || 0);

  const datasets = [];
  if (chkOriginal.checked) datasets.push({ label: 'Original AI-likeness', data: originalData, backgroundColor: '#2563eb' });
  if (chkRewritten.checked) datasets.push({ label: 'Rewritten AI-likeness', data: rewrittenData, backgroundColor: '#16a34a' });
  if (chkSimilarity.checked) datasets.push({ label: 'Similarity', data: similarityData, backgroundColor: '#f59e0b' });
  if (chkGrammar.checked) datasets.push({ label: 'Grammar', data: grammarData, backgroundColor: '#ef4444' });

  return { labels, datasets };
}

function updateChartFromHistory() {
  const { labels, datasets } = buildDatasets();
  if (!metricsChart) {
    const ctx = document.getElementById('metricsChart').getContext('2d');
    metricsChart = new Chart(ctx, {
      type: 'bar',
      data: { labels, datasets },
      options: {
        responsive: true,
        scales: { x: { stacked: stacked }, y: { beginAtZero: true, max: 100, stacked: stacked } }
      }
    });
  } else {
    metricsChart.data.labels = labels;
    metricsChart.data.datasets = datasets;
    metricsChart.options.scales.x.stacked = stacked;
    metricsChart.options.scales.y.stacked = stacked;
    metricsChart.update();
  }
}

function clearHistory() {
  history = [];
  saveHistory();
  updateChartFromHistory();
}

// wire controls
chkOriginal.addEventListener('change', updateChartFromHistory);
chkRewritten.addEventListener('change', updateChartFromHistory);
chkSimilarity.addEventListener('change', updateChartFromHistory);
chkGrammar.addEventListener('change', updateChartFromHistory);
toggleStacked.addEventListener('click', () => { stacked = !stacked; updateChartFromHistory(); });
clearHistoryBtn.addEventListener('click', () => { clearHistory(); status.textContent = 'History cleared.'; });
historySizeSelect.addEventListener('change', () => { saveHistory(); updateChartFromHistory(); });

loadHistory();
updateChartFromHistory();

analyzeBtn.addEventListener('click', async () => {
  const text = inputText.value.trim();
  if (!text) {
    status.textContent = 'Please enter text first.';
    return;
  }

  status.textContent = 'Analyzing...';
    spinner.hidden = false;
  try {
    const response = await fetch('/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const data = await response.json();
    if (!response.ok) {
      status.textContent = data.error || 'Analysis failed.';
      spinner.hidden = true;
      return;
    }

    originalScore.textContent = `${data.original_score}%`;
    rewrittenScore.textContent = `${data.rewritten_score}%`;
    similarityScore.textContent = `${data.similarity_score}%`;
    readabilityGrade.textContent = data.readability_grade.toFixed(1);
    grammarScore.textContent = `${data.grammar_score}%`;
    aiSourceResult.textContent = data.ai_source || 'Unknown';
    sourceTypeResult.textContent = data.source_type || 'General';
    wordCount.textContent = data.word_count;
    charCount.textContent = data.character_count;
    processingTime.textContent = `${data.processing_time_ms} ms`;
    outputText.value = data.rewritten_text;
    downloadLink.href = data.download_url;
    downloadLink.textContent = 'Download';
    // update chart with latest metrics
    const entry = { ts: Date.now(), label: new Date().toLocaleTimeString(), original_score: data.original_score, rewritten_score: data.rewritten_score, similarity_score: data.similarity_score, grammar_score: data.grammar_score };
    pushToHistory(entry);
    updateChartFromHistory();
    spinner.hidden = true;
    resultsSection.hidden = false;
    status.textContent = 'Analysis complete.';
  } catch (error) {
    spinner.hidden = true;
    status.textContent = 'Unable to reach the server.';
  }
});

clearBtn.addEventListener('click', () => {
  inputText.value = '';
  outputText.value = '';
  resultsSection.hidden = true;
  status.textContent = '';
});

copyBtn.addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(outputText.value);
    status.textContent = 'Copied to clipboard.';
  } catch (error) {
    status.textContent = 'Copy failed.';
  }
});
