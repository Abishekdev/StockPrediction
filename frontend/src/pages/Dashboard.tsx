import React, { useState, useEffect } from 'react';
import { api, StockData } from '../lib/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Search, TrendingUp, TrendingDown, AlertCircle } from 'lucide-react';

const Dashboard: React.FC = () => {
  const [ticker, setTicker] = useState('AAPL');
  const [searchInput, setSearchInput] = useState('');
  const [stockData, setStockData] = useState<StockData[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [currentPrice, setCurrentPrice] = useState<number | null>(null);
  const [priceChange, setPriceChange] = useState<number | null>(null);
  const [sentiment, setSentiment] = useState<any>(null);

  useEffect(() => {
    loadStockData(ticker);
    loadSentiment(ticker);
  }, [ticker]);

  const loadStockData = async (tickerSymbol: string) => {
    setLoading(true);
    setError('');
    try {
      const response = await api.getStockData(tickerSymbol, 100);
      setStockData(response.data);

      if (response.data.length > 0) {
        const lastPrice = response.data[response.data.length - 1].close;
        const firstPrice = response.data[0].close;
        setCurrentPrice(lastPrice);
        setPriceChange(lastPrice - firstPrice);
      }
    } catch (err: any) {
      setError(`Failed to load data for ${tickerSymbol}`);
    } finally {
      setLoading(false);
    }
  };

  const loadSentiment = async (tickerSymbol: string) => {
    try {
      const result = await api.getSentiment(tickerSymbol);
      setSentiment(result);
    } catch (err) {
      setSentiment(null);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchInput.trim()) {
      setTicker(searchInput.toUpperCase());
      setSearchInput('');
    }
  };

  const getSentimentColor = (score: number) => {
    if (score > 0.3) return 'bg-green-500/20 text-green-300 border-green-500/50';
    if (score > 0.1) return 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50';
    if (score < -0.3) return 'bg-red-500/20 text-red-300 border-red-500/50';
    if (score < -0.1) return 'bg-orange-500/20 text-orange-300 border-orange-500/50';
    return 'bg-gray-500/20 text-gray-300 border-gray-500/50';
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 fade-in">
      {/* Search Section */}
      <div className="mb-8">
        <form onSubmit={handleSearch} className="flex gap-2">
          <input
            type="text"
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            placeholder="Search ticker (e.g., AAPL, GOOGL, MSFT)..."
            className="flex-1 px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500/50 focus:bg-white/10 transition"
          />
          <button
            type="submit"
            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-400 text-white font-semibold rounded-lg hover:from-blue-500 hover:to-blue-300 transition flex items-center gap-2"
          >
            <Search className="w-5 h-5" />
            Search
          </button>
        </form>
      </div>

      {/* Price Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        {/* Current Price */}
        <div className="glass rounded-xl p-6">
          <p className="text-gray-400 text-sm mb-2">Current Price ({ticker})</p>
          <h3 className="text-3xl font-bold text-white mb-2">
            ${currentPrice?.toFixed(2) || 'N/A'}
          </h3>
          {priceChange !== null && (
            <p
              className={`text-sm font-semibold flex items-center gap-1 ${
                priceChange >= 0 ? 'text-green-400' : 'text-red-400'
              }`}
            >
              {priceChange >= 0 ? (
                <TrendingUp className="w-4 h-4" />
              ) : (
                <TrendingDown className="w-4 h-4" />
              )}
              {priceChange >= 0 ? '+' : ''}{priceChange.toFixed(2)} (100 days)
            </p>
          )}
        </div>

        {/* Sentiment Analysis */}
        {sentiment && (
          <div className="glass rounded-xl p-6">
            <p className="text-gray-400 text-sm mb-2">News Sentiment</p>
            <div className={`px-3 py-2 rounded-lg border inline-block ${getSentimentColor(sentiment.sentiment_score)}`}>
              <p className="font-semibold text-lg">{sentiment.interpretation}</p>
              <p className="text-xs mt-1">{sentiment.articles_analyzed} articles analyzed</p>
            </div>
          </div>
        )}

        {/* Statistics */}
        <div className="glass rounded-xl p-6">
          <p className="text-gray-400 text-sm mb-2">30-Day Range</p>
          {stockData.length > 0 && (
            <>
              <p className="text-white mb-1">
                High: <span className="font-bold">${Math.max(...stockData.slice(-30).map(d => d.high)).toFixed(2)}</span>
              </p>
              <p className="text-white">
                Low: <span className="font-bold">${Math.min(...stockData.slice(-30).map(d => d.low)).toFixed(2)}</span>
              </p>
            </>
          )}
        </div>
      </div>

      {/* Chart Section */}
      <div className="glass rounded-xl p-6 mb-8">
        <h2 className="text-xl font-bold text-white mb-4">Price History & Technical Indicators</h2>

        {error && (
          <div className="p-3 bg-red-500/10 border border-red-500/50 rounded-lg flex items-start space-x-2 mb-4">
            <AlertCircle className="w-5 h-5 text-red-400 mt-0.5 flex-shrink-0" />
            <p className="text-red-300">{error}</p>
          </div>
        )}

        {loading ? (
          <div className="h-96 flex items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          </div>
        ) : stockData.length > 0 ? (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={stockData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis
                dataKey="date"
                stroke="#999"
                tick={{ fontSize: 12 }}
                style={{ textAnchor: 'end', height: 50 }}
              />
              <YAxis stroke="#999" tick={{ fontSize: 12 }} width={50} />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(0, 0, 0, 0.8)',
                  border: '1px solid #444',
                  borderRadius: '8px',
                }}
                labelStyle={{ color: '#fff' }}
              />
              <Legend />
              <Line type="monotone" dataKey="close" stroke="#3b82f6" dot={false} name="Close Price" />
              <Line type="monotone" dataKey="ma20" stroke="#8b5cf6" dot={false} name="MA(20)" />
              <Line type="monotone" dataKey="ma50" stroke="#ec4899" dot={false} name="MA(50)" />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <p className="text-gray-400 text-center py-8">No data available</p>
        )}
      </div>

      {/* Disclaimer */}
      <div className="p-4 bg-yellow-500/10 border border-yellow-500/30 rounded-lg text-yellow-300 text-sm">
        <p className="font-semibold">⚠️ Disclaimer</p>
        <p className="mt-1">
          This dashboard is for educational purposes only. Stock prices are real, but sentiment
          analysis and predictions are simplified models. Always conduct thorough research before
          making investment decisions.
        </p>
      </div>
    </div>
  );
};

export default Dashboard;
