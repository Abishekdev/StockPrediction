import React, { useState, useEffect } from 'react';
import { api, PortfolioItem } from '../lib/api';
import { Briefcase, Plus, Trash2, AlertCircle, TrendingUp, TrendingDown } from 'lucide-react';

const Portfolio: React.FC = () => {
  const [portfolio, setPortfolio] = useState<PortfolioItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);

  // Form state
  const [ticker, setTicker] = useState('');
  const [quantity, setQuantity] = useState('');
  const [purchasePrice, setPurchasePrice] = useState('');
  const [purchaseDate, setPurchaseDate] = useState(new Date().toISOString().split('T')[0]);
  const [addingItem, setAddingItem] = useState(false);

  useEffect(() => {
    loadPortfolio();
  }, []);

  const loadPortfolio = async () => {
    setLoading(true);
    setError('');
    try {
      const result = await api.getPortfolio();
      setPortfolio(result);
    } catch (err: any) {
      setError('Failed to load portfolio');
    } finally {
      setLoading(false);
    }
  };

  const handleAddItem = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setAddingItem(true);

    try {
      await api.addPortfolioItem(
        ticker.toUpperCase(),
        parseFloat(quantity),
        parseFloat(purchasePrice),
        purchaseDate
      );

      // Reset form
      setTicker('');
      setQuantity('');
      setPurchasePrice('');
      setPurchaseDate(new Date().toISOString().split('T')[0]);
      setShowForm(false);

      // Reload portfolio
      loadPortfolio();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to add item');
    } finally {
      setAddingItem(false);
    }
  };

  const handleDelete = async (portfolioId: number) => {
    if (!window.confirm('Are you sure you want to delete this item?')) return;

    setError('');
    try {
      await api.deletePortfolioItem(portfolioId);
      loadPortfolio();
    } catch (err: any) {
      setError('Failed to delete item');
    }
  };

  const totalValue = portfolio.reduce((sum, item) => {
    if (item.total_value) return sum + item.total_value;
    return sum;
  }, 0);

  const totalInvested = portfolio.reduce((sum, item) => {
    return sum + item.purchase_price * item.quantity;
  }, 0);

  const portfolioGain = totalValue - totalInvested;
  const portfolioGainPercent = totalInvested > 0 ? (portfolioGain / totalInvested) * 100 : 0;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 fade-in">
      {/* Portfolio Summary */}
      <div className="glass rounded-xl p-8 mb-8">
        <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
          <Briefcase className="w-6 h-6 text-blue-400" />
          Portfolio Dashboard
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          {/* Total Invested */}
          <div className="bg-white/5 rounded-lg p-4">
            <p className="text-gray-400 text-sm mb-1">Total Invested</p>
            <p className="text-2xl font-bold text-white">
              ${totalInvested.toFixed(2)}
            </p>
          </div>

          {/* Current Value */}
          <div className="bg-white/5 rounded-lg p-4">
            <p className="text-gray-400 text-sm mb-1">Current Value</p>
            <p className="text-2xl font-bold text-white">
              ${totalValue.toFixed(2)}
            </p>
          </div>

          {/* Gain/Loss */}
          <div className="bg-white/5 rounded-lg p-4">
            <p className="text-gray-400 text-sm mb-1">Gain/Loss</p>
            <p
              className={`text-2xl font-bold flex items-center gap-2 ${
                portfolioGain >= 0 ? 'text-green-400' : 'text-red-400'
              }`}
            >
              {portfolioGain >= 0 ? (
                <TrendingUp className="w-5 h-5" />
              ) : (
                <TrendingDown className="w-5 h-5" />
              )}
              ${Math.abs(portfolioGain).toFixed(2)} ({portfolioGainPercent.toFixed(2)}%)
            </p>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 bg-red-500/10 border border-red-500/50 rounded-lg flex items-start space-x-2">
          <AlertCircle className="w-5 h-5 text-red-400 mt-0.5 flex-shrink-0" />
          <p className="text-red-300">{error}</p>
        </div>
      )}

      {/* Add Item Form */}
      {showForm && (
        <div className="glass rounded-xl p-6 mb-8">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <Plus className="w-5 h-5" />
            Add Stock
          </h3>

          <form onSubmit={handleAddItem} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Ticker
                </label>
                <input
                  type="text"
                  value={ticker}
                  onChange={(e) => setTicker(e.target.value)}
                  placeholder="e.g., AAPL"
                  className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500/50 focus:bg-white/10 transition uppercase"
                  disabled={addingItem}
                  maxLength={5}
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Quantity
                </label>
                <input
                  type="number"
                  value={quantity}
                  onChange={(e) => setQuantity(e.target.value)}
                  placeholder="e.g., 10"
                  className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500/50 focus:bg-white/10 transition"
                  disabled={addingItem}
                  step="0.01"
                  min="0.01"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Purchase Price ($)
                </label>
                <input
                  type="number"
                  value={purchasePrice}
                  onChange={(e) => setPurchasePrice(e.target.value)}
                  placeholder="e.g., 150.00"
                  className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500/50 focus:bg-white/10 transition"
                  disabled={addingItem}
                  step="0.01"
                  min="0.01"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Purchase Date
                </label>
                <input
                  type="date"
                  value={purchaseDate}
                  onChange={(e) => setPurchaseDate(e.target.value)}
                  className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-blue-500/50 focus:bg-white/10 transition"
                  disabled={addingItem}
                  required
                />
              </div>
            </div>

            <div className="flex gap-2">
              <button
                type="submit"
                disabled={addingItem || !ticker || !quantity || !purchasePrice}
                className="flex-1 py-2 bg-gradient-to-r from-green-600 to-green-400 text-white font-semibold rounded-lg hover:from-green-500 hover:to-green-300 disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                {addingItem ? 'Adding...' : 'Add to Portfolio'}
              </button>

              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="flex-1 py-2 bg-gray-600 text-white font-semibold rounded-lg hover:bg-gray-500 transition"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Portfolio Items */}
      <div className="glass rounded-xl p-8">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold text-white">Holdings</h3>
          {!showForm && (
            <button
              onClick={() => setShowForm(true)}
              className="px-4 py-2 bg-gradient-to-r from-blue-600 to-blue-400 text-white font-semibold rounded-lg hover:from-blue-500 hover:to-blue-300 transition flex items-center gap-2"
            >
              <Plus className="w-4 h-4" />
              Add Stock
            </button>
          )}
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          </div>
        ) : portfolio.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-white/10">
                  <th className="px-4 py-3 text-left text-gray-400">Ticker</th>
                  <th className="px-4 py-3 text-left text-gray-400">Quantity</th>
                  <th className="px-4 py-3 text-left text-gray-400">Purchase Price</th>
                  <th className="px-4 py-3 text-left text-gray-400">Current Price</th>
                  <th className="px-4 py-3 text-left text-gray-400">Total Value</th>
                  <th className="px-4 py-3 text-left text-gray-400">Gain/Loss</th>
                  <th className="px-4 py-3 text-left text-gray-400">Action</th>
                </tr>
              </thead>
              <tbody>
                {portfolio.map((item) => {
                  const totalCost = item.purchase_price * item.quantity;
                  const currentValue = item.current_price ? item.quantity * item.current_price : null;
                  const gainLoss = currentValue ? currentValue - totalCost : null;
                  const gainLossPercent =
                    currentValue && totalCost ? ((currentValue - totalCost) / totalCost) * 100 : null;

                  return (
                    <tr key={item.id} className="border-b border-white/5 hover:bg-white/5 transition">
                      <td className="px-4 py-3 font-semibold text-white">{item.ticker}</td>
                      <td className="px-4 py-3 text-gray-300">{item.quantity.toFixed(2)}</td>
                      <td className="px-4 py-3 text-gray-300">${item.purchase_price.toFixed(2)}</td>
                      <td className="px-4 py-3 text-gray-300">
                        {item.current_price ? `$${item.current_price.toFixed(2)}` : 'N/A'}
                      </td>
                      <td className="px-4 py-3 font-semibold text-blue-400">
                        {item.total_value ? `$${item.total_value.toFixed(2)}` : 'N/A'}
                      </td>
                      <td className="px-4 py-3">
                        {gainLoss !== null ? (
                          <span
                            className={`font-semibold flex items-center gap-1 ${
                              gainLoss >= 0 ? 'text-green-400' : 'text-red-400'
                            }`}
                          >
                            {gainLoss >= 0 ? (
                              <TrendingUp className="w-4 h-4" />
                            ) : (
                              <TrendingDown className="w-4 h-4" />
                            )}
                            ${Math.abs(gainLoss).toFixed(2)} ({gainLossPercent?.toFixed(2)}%)
                          </span>
                        ) : (
                          <span className="text-gray-400">N/A</span>
                        )}
                      </td>
                      <td className="px-4 py-3">
                        <button
                          onClick={() => handleDelete(item.id)}
                          className="text-red-400 hover:text-red-300 transition"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-center text-gray-400 py-12">
            No stocks in portfolio. Add one to get started!
          </p>
        )}
      </div>
    </div>
  );
};

export default Portfolio;
