import React, { useState, useEffect } from 'react';
import { api, PredictionResponse } from '../lib/api';
import { TrendingUp, AlertCircle, Check, AlertTriangle } from 'lucide-react';

const Prediction: React.FC = () => {
  const [ticker, setTicker] = useState('AAPL');
  const [daysAhead, setDaysAhead] = useState(1);
  const [loading, setLoading] = useState(false);
  const [predicting, setPredicting] = useState(false);
  const [error, setError] = useState('');
  const [prediction, setPrediction] = useState<PredictionResponse | null>(null);
  const [predictions, setPredictions] = useState<PredictionResponse[]>([]);

  useEffect(() => {
    loadPredictions();
  }, []);

  const loadPredictions = async () => {
    setLoading(true);
    try {
      const result = await api.getPredictions();
      setPredictions(result);
    } catch (err: any) {
      setError('Failed to load prediction history');
    } finally {
      setLoading(false);
    }
  };

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setPredicting(true);

    try {
      const result = await api.predict(ticker.toUpperCase(), daysAhead);
      setPrediction(result);
      loadPredictions();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Prediction failed. Please try again.');
    } finally {
      setPredicting(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 fade-in">
      {/* Prediction Form */}
      <div className="glass rounded-xl p-8 mb-8">
        <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
          <TrendingUp className="w-6 h-6 text-blue-400" />
          Make a Prediction
        </h2>

        {error && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-500/50 rounded-lg flex items-start space-x-2">
            <AlertCircle className="w-5 h-5 text-red-400 mt-0.5 flex-shrink-0" />
            <p className="text-red-300">{error}</p>
          </div>
        )}

        <form onSubmit={handlePredict} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Stock Ticker
              </label>
              <input
                type="text"
                value={ticker}
                onChange={(e) => setTicker(e.target.value)}
                placeholder="e.g., AAPL"
                className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500/50 focus:bg-white/10 transition uppercase"
                disabled={predicting}
                required
                maxLength={5}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Predict Days Ahead: {daysAhead}
              </label>
              <input
                type="range"
                min="1"
                max="30"
                value={daysAhead}
                onChange={(e) => setDaysAhead(parseInt(e.target.value))}
                className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer"
                disabled={predicting}
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>1 day</span>
                <span>30 days</span>
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={predicting || ticker.length === 0}
            className="w-full py-3 bg-gradient-to-r from-blue-600 to-blue-400 text-white font-semibold rounded-lg hover:from-blue-500 hover:to-blue-300 disabled:opacity-50 disabled:cursor-not-allowed transition flex items-center justify-center gap-2"
          >
            {predicting ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Generating Prediction...
              </>
            ) : (
              <>
                <TrendingUp className="w-5 h-5" />
                Generate Prediction
              </>
            )}
          </button>
        </form>

        {/* Prediction Result */}
        {prediction && (
          <div className="mt-8 pt-8 border-t border-white/10">
            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <Check className="w-5 h-5 text-green-400" />
              Prediction Result
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div className="bg-white/5 rounded-lg p-4">
                <p className="text-gray-400 text-sm mb-1">Ticker</p>
                <p className="text-2xl font-bold text-white">{prediction.ticker}</p>
              </div>

              <div className="bg-white/5 rounded-lg p-4">
                <p className="text-gray-400 text-sm mb-1">Predicted Price</p>
                <p className="text-2xl font-bold text-blue-400">
                  ${prediction.predicted_price.toFixed(2)}
                </p>
              </div>

              <div className="bg-white/5 rounded-lg p-4">
                <p className="text-gray-400 text-sm mb-1">Prediction Window</p>
                <p className="text-lg font-semibold text-white">
                  {prediction.prediction_window} day{prediction.prediction_window !== 1 ? 's' : ''}
                </p>
              </div>

              <div className="bg-white/5 rounded-lg p-4">
                <p className="text-gray-400 text-sm mb-1">Generated</p>
                <p className="text-sm font-mono text-green-400">
                  {new Date(prediction.created_at).toLocaleString()}
                </p>
              </div>
            </div>

            {/* Metrics */}
            {prediction.metrics && Object.keys(prediction.metrics).length > 0 && (
              <div>
                <h4 className="text-lg font-semibold text-white mb-3">Model Accuracy Metrics</h4>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {Object.entries(prediction.metrics).map(([key, value]) => (
                    <div key={key} className="bg-white/5 rounded-lg p-3">
                      <p className="text-xs text-gray-400 uppercase mb-1">
                        {key.replace(/_/g, ' ')}
                      </p>
                      <p className="text-lg font-bold text-blue-400">
                        {typeof value === 'number' ? value.toFixed(6) : value}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Prediction History */}
      <div className="glass rounded-xl p-8">
        <h2 className="text-2xl font-bold text-white mb-6">Prediction History</h2>

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          </div>
        ) : predictions.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-white/10">
                  <th className="px-4 py-3 text-left text-gray-400">Ticker</th>
                  <th className="px-4 py-3 text-left text-gray-400">Predicted Price</th>
                  <th className="px-4 py-3 text-left text-gray-400">Days Ahead</th>
                  <th className="px-4 py-3 text-left text-gray-400">Accuracy (MAE)</th>
                  <th className="px-4 py-3 text-left text-gray-400">Generated</th>
                </tr>
              </thead>
              <tbody>
                {predictions.slice(0, 10).map((pred) => (
                  <tr key={pred.id} className="border-b border-white/5 hover:bg-white/5 transition">
                    <td className="px-4 py-3 font-semibold text-white">{pred.ticker}</td>
                    <td className="px-4 py-3 text-blue-400 font-semibold">
                      ${pred.predicted_price.toFixed(2)}
                    </td>
                    <td className="px-4 py-3 text-gray-300">{pred.prediction_window}</td>
                    <td className="px-4 py-3">
                      {pred.metrics?.mae ? (
                        <span className="text-green-400">{pred.metrics.mae.toFixed(6)}</span>
                      ) : (
                        <span className="text-gray-400">N/A</span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-gray-400 text-xs">
                      {new Date(pred.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-center text-gray-400 py-12">No predictions yet. Generate your first prediction above!</p>
        )}
      </div>

      {/* Warning Box */}
      <div className="mt-8 p-4 bg-red-500/10 border border-red-500/30 rounded-lg flex items-start gap-3">
        <AlertTriangle className="w-5 h-5 text-red-400 mt-0.5 flex-shrink-0" />
        <div>
          <p className="font-semibold text-red-300">Important Disclaimer</p>
          <p className="text-red-200 text-sm mt-1">
            These predictions are generated by a machine learning model trained on historical data.
            They are for educational purposes only and should NEVER be your sole basis for investment
            decisions. All stock investments carry risk, including potential loss of principal.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Prediction;
