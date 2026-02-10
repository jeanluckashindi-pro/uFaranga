import React from 'react';
import ComponentExamples from './components/common/ComponentExamples';
import TailwindTest from './components/TailwindTest';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <h1 className="text-2xl font-bold text-blue-600">uFaranga - Front Office</h1>
            <p className="text-gray-600">Application Client</p>
          </div>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <TailwindTest />
        </div>
        <ComponentExamples />
      </main>
    </div>
  );
}

export default App;
