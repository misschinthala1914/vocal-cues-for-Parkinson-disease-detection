import React, { useState } from 'react';
import { AlertCircle } from 'lucide-react';
import { VoiceAnalysis } from './components/VoiceAnalysis';
import { Results } from './components/Results';
import { ModelAccuracy } from './components/ModelAccuracy';
import { Recommendations } from './components/Recommendations';
import CBITLogo from './assets/cbit-image.jpeg';

export type AnalysisResult = {
  isParkinsons: boolean;
  confidence: number;
  features: Record<string, number>;
};

function App() {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [locked, setLocked] = useState(false);

  const handleAnalysisComplete = (analysisResult: AnalysisResult) => {
    if (!locked) {
      setResult(analysisResult);
      setLocked(true);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex items-center space-x-4">
          <img
            src={CBITLogo}
            alt="CBIT Logo"
            className="h-12 w-12 rounded-full border border-gray-300"
          />
          <h1 className="text-2xl font-bold text-gray-900">
            Parkinson's Disease Detection using Vocal Cues
          </h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <VoiceAnalysis onAnalysisComplete={handleAnalysisComplete} />
        </div>

        {result && <Results result={result} />}

        {result && <Recommendations isParkinsons={result.isParkinsons} />}

        <div className="mt-8">
          <ModelAccuracy />
        </div>

        <div className="mt-8 bg-yellow-50 border-l-4 border-yellow-400 p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <AlertCircle className="h-5 w-5 text-yellow-400" />
            </div>
            <div className="ml-3">
              <p className="text-sm text-yellow-700">
                This tool is for educational purposes only. Please consult with
                healthcare professionals for proper medical diagnosis.
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
