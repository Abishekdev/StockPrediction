import React, { useState, useEffect } from 'react';
import { api } from '../lib/api';
import { Settings, RefreshCw, Check, AlertCircle, Zap } from 'lucide-react';

const SettingsPage: React.FC = () => {
  const [availableModels, setAvailableModels] = useState<any[]>([]);
  const [retrainingTicker, setRetrainingTicker] = useState('');
  const [retraining, setRetraining] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [modelLoading, setModelLoading] = useState(true);

  // Retraining parameters
  const [epochs, setEpochs] = useState(50);
  const [batchSize, setBatchSize] = useState(32);
  const [lstmUnits, setLstmUnits] = useState(128);

  useEffect(() => {
    loadModels();
  }, []);

  const loadModels = async () => {
    setModelLoading(true);
    try {
      const result = await api.getAvailableModels();
      setAvailableModels(result.models || []);
    } catch (err) {
      setError('Failed to load models');
    } finally {
      setModelLoading(false);
    }
  };

  const handleRetrain = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!retrainingTicker.trim()) {
      setError('Please enter a ticker symbol');
      return;
    }

    setError('');
    setSuccess('');
    setRetraining(true);

    try {
      const response = await api.retrain(retrainingTicker.toUpperCase(), epochs, batchSize, lstmUnits);
      setSuccess(`Retraining started for ${retrainingTicker.toUpperCase()}. This may take a few minutes.`);
      setRetrainingTicker('');

      // Reload models after a delay
      setTimeout(loadModels, 30000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Retraining failed');
    } finally {
      setRetraining(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 fade-in">
      {/* Retrain Model Section */}
      <div className="glass rounded-xl p-8 mb-8">
        <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
          <Zap className="w-6 h-6 text-blue-400" />
          Retrain Model
        </h2>

        <p className="text-gray-400 mb-6">
          Retrain the LSTM model for a specific stock ticker to improve prediction accuracy with new data.
        </p>

        {error && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-500/50 rounded-lg flex items-start space-x-2">
            <AlertCircle className="w-5 h-5 text-red-400 mt-0.5 flex-shrink-0" />
            <p className="text-red-300">{error}</p>
          </div>
        )}

        {success && (
          <div className="mb-6 p-4 bg-green-500/10 border border-green-500/50 rounded-lg flex items-start space-x-2">
            <Check className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" />
            <p className="text-green-300">{success}</p>
          </div>
        )}

        <form onSubmit={handleRetrain} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Stock Ticker
              </label>
              <input
                type="text"
                value={retrainingTicker}
                onChange={(e) => setRetrainingTicker(e.target.value)}
                placeholder="e.g., AAPL"
                className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500/50 focus:bg-white/10 transition uppercase"
                disabled={retraining}
                maxLength={5}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Epochs: {epochs}
              </label>
              <input
                type="range"
                min="10"
                max="200"
                value={epochs}
                onChange={(e) => setEpochs(parseInt(e.target.value))}
                className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer"
                disabled={retraining}
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>10</span>
                <span>200</span>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Batch Size: {batchSize}
              </label>
              <input
                type="range"
                min="8"
                max="128"
                value={batchSize}
                onChange={(e) => setBatchSize(parseInt(e.target.value))}
                className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer"
                disabled={retraining}
                step="8"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>8</span>
                <span>128</span>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                LSTM Units: {lstmUnits}
              </label>
              <input
                type="range"
                min="64"
                max="512"
                value={lstmUnits}
                onChange={(e) => setLstmUnits(parseInt(e.target.value))}
                className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer"
                disabled={retraining}
                step="64"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>64</span>
                <span>512</span>
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={retraining || !retrainingTicker.trim()}
            className="w-full py-3 bg-gradient-to-r from-blue-600 to-blue-400 text-white font-semibold rounded-lg hover:from-blue-500 hover:to-blue-300 disabled:opacity-50 disabled:cursor-not-allowed transition flex items-center justify-center gap-2"
          >
            {retraining ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Training...
              </>
            ) : (
              <>
                <RefreshCw className="w-5 h-5" />
                Start Retraining
              </>
            )}
          </button>
        </form>

        <div className="mt-4 p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg text-blue-300 text-sm">
          <p className="font-semibold mb-1">ℹ️ Info</p>
          <ul className="list-disc list-inside space-y-1">
            <li>Retraining uses the latest stock data and can take several minutes</li>
            <li>More epochs generally lead to better accuracy but longer training time</li>
            <li>Larger batch sizes train faster but may converge slower</li>
          </ul>
        </div>
      </div>

      {/* Available Models Section */}
      <div className="glass rounded-xl p-8">
        <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
          <Settings className="w-6 h-6 text-blue-400" />
          Available Models
        </h2>

        {modelLoading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          </div>
        ) : availableModels.length > 0 ? (
          <div className="space-y-4">
            {availableModels.map((model, index) => (
              <div key={index} className="bg-white/5 rounded-lg p-6 border border-white/10">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-bold text-white mb-1">{model.ticker}</h3>
                    <p className="text-sm text-gray-400">
                      Trained: {formatDate(model.trained_at)}
                    </p>
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
                  <div>
                    <p className="text-xs text-gray-400 mb-1">RMSE</p>
                    <p className="font-bold text-white">
                      {model.test_metrics?.rmse?.toFixed(6) || 'N/A'}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-400 mb-1">MAE</p>
                    <p className="font-bold text-white">
                      {model.test_metrics?.mae?.toFixed(6) || 'N/A'}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-400 mb-1">MAPE</p>
                    <p className="font-bold text-white">
                      {model.test_metrics?.mape?.toFixed(4) || 'N/A'}%
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-400 mb-1">Train Samples</p>
                    <p className="font-bold text-white">{model.training_samples || 'N/A'}</p>
                  </div>
                </div>

                <div className="text-xs text-gray-500 space-y-1">
                  <p>
                    <span className="text-gray-400">Lookback Window:</span> {model.lookback_window} days
                  </p>
                  <p>
                    <span className="text-gray-400">LSTM Units:</span> {model.lstm_units}
                  </p>
                  <p>
                    <span className="text-gray-400">Batch Size:</span> {model.batch_size}
                  </p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-center text-gray-400 py-12">
            No trained models yet. Train your first model using the training script.
          </p>
        )}
      </div>

      {/* System Information */}
      <div className="mt-8 p-4 bg-gray-500/10 border border-gray-500/30 rounded-lg text-gray-300 text-sm">
        <p className="font-semibold mb-2">System Information</p>
        <ul className="space-y-1 text-xs">
          <li>Backend: FastAPI (Python)</li>
          <li>Frontend: React.js with TypeScript</li>
          <li>ML Framework: TensorFlow/Keras</li>
          <li>Database: SQLite/PostgreSQL</li>
          <li>Real-time Updates: WebSockets</li>
        </ul>
      </div>
    </div>
  );
};

export default SettingsPage;
