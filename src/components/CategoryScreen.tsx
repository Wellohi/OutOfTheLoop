import React, { useState, useEffect } from 'react';
import { IonButton } from '@ionic/react';
import { gameWords } from '../game-logic.js';

interface CategoryScreenProps {
  onStartGame: (category: string, rounds: number) => void;
  onBack: () => void;
}

const CategoryScreen: React.FC<CategoryScreenProps> = ({ onStartGame, onBack }) => {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedRound, setSelectedRound] = useState<number | null>(null);

  return (
    <div className="d-flex flex-column vh-100 p-3 text-white">
      <h2 className="text-center text-info mb-3 h3">Game Setup</h2>

      <div className="flex-grow-1 overflow-auto">
        <h3 className="h5 text-center mb-3">Choose a Category</h3>
        <div className="row row-cols-2 g-2">
          {Object.keys(gameWords).map((categoryName) => (
            <div className="col d-grid" key={categoryName}>
              <button
                className={`btn ${selectedCategory === categoryName ? 'btn-primary' : 'btn-outline-primary'}`}
                onClick={() => setSelectedCategory(categoryName)}
              >
                {categoryName}
              </button>
            </div>
          ))}
        </div>

        <h3 className="h5 text-center mt-4 mb-3">Select Number of Question Rounds</h3>
        <div className="row row-cols-3 g-2">
          {[1, 2, 3].map((roundNum) => (
            <div className="col d-grid" key={roundNum}>
              <button
                className={`btn ${selectedRound === roundNum ? 'btn-info' : 'btn-outline-info'}`}
                onClick={() => setSelectedRound(roundNum)}
              >
                {roundNum}
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className="d-grid gap-2 mt-3">
        <IonButton
          onClick={() => onStartGame(selectedCategory!, selectedRound!)}
          expand="block"
          size="large"
          className="fw-bold"
          disabled={!selectedCategory || !selectedRound}
        >
          Continue
        </IonButton>
        <IonButton onClick={onBack} expand="block" size="large" color="medium" className="fw-bold">
          Back
        </IonButton>
      </div>
    </div>
  );
};

export default CategoryScreen;
