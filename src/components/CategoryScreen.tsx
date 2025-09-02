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

  // This effect is not strictly necessary for this component version,
  // but it's good practice to reset state when it becomes visible.
  useEffect(() => {
    setSelectedCategory(null);
    setSelectedRound(null);
  }, []);


  return (
    <div className="d-flex flex-column vh-100 p-3 text-white">
      <h1 className="text-center text-info mb-3 h1">Configurar Jogo</h1>

      <div className="flex-grow-1 overflow-auto">
        <h2 className="h2 text-center mb-3">Selecione a Categoria</h2>
        <div className="row row-cols-2 g-3"> {/* Increased gap for more spacing */}
          {Object.keys(gameWords).map((categoryName) => (
            <div className="col d-grid" key={categoryName}>
              <button
                // MODIFIED: Added py-3 to make buttons taller
                className={`btn py-3 ${selectedCategory === categoryName ? 'btn-primary' : 'btn-outline-primary'}`}
                onClick={() => setSelectedCategory(categoryName)}
              >
                {categoryName}
              </button>
            </div>
          ))}
        </div>

        <h2 className="h2 text-center mt-4 mb-3">Rodadas de Perguntas</h2>
        <div className="row row-cols-3 g-2">
          {[1, 2, 3].map((roundNum) => (
            <div className="col d-grid" key={roundNum}>
              <button
                // MODIFIED: Added py-3 to make buttons taller
                className={`btn py-3 ${selectedRound === roundNum ? 'btn-info' : 'btn-outline-info'}`}
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
          Próximo
        </IonButton>
        <IonButton onClick={onBack} expand="block" size="large" color="medium" className="fw-bold">
          Voltar
        </IonButton>
      </div>
    </div>
  );
};

export default CategoryScreen;

