import React from 'react';

const TailwindTest = () => {
  return (
    <div className="p-8 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-4">Test Tailwind CSS</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white bg-opacity-20 p-4 rounded-lg">
          <h3 className="font-semibold">Couleurs</h3>
          <div className="flex space-x-2 mt-2">
            <div className="w-6 h-6 bg-red-500 rounded"></div>
            <div className="w-6 h-6 bg-green-500 rounded"></div>
            <div className="w-6 h-6 bg-blue-500 rounded"></div>
          </div>
        </div>
        
        <div className="bg-white bg-opacity-20 p-4 rounded-lg">
          <h3 className="font-semibold">Spacing</h3>
          <div className="space-y-2 mt-2">
            <div className="h-2 bg-white bg-opacity-50 rounded"></div>
            <div className="h-2 bg-white bg-opacity-50 rounded w-3/4"></div>
            <div className="h-2 bg-white bg-opacity-50 rounded w-1/2"></div>
          </div>
        </div>
        
        <div className="bg-white bg-opacity-20 p-4 rounded-lg">
          <h3 className="font-semibold">Typography</h3>
          <p className="text-sm mt-2">Small text</p>
          <p className="text-base">Base text</p>
          <p className="text-lg font-bold">Large bold</p>
        </div>
      </div>
      
      <button className="mt-6 bg-white text-blue-600 px-6 py-2 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
        Bouton Test
      </button>
    </div>
  );
};

export default TailwindTest;