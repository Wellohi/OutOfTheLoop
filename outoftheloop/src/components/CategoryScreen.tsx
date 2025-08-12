import React, { useState } from 'react';
import { IonButton } from '@ionic/react';
// Note the path change to find the game-logic file
import { gameWords } from '../game-logic.js';

interface CategoryScreenProps {
  onStartGame: (category: string, rounds: number) => void;
  onBack: () => void;
}

const CategoryScreen: React.FC<CategoryScreenProps> = ({ onStartGame, onBack }) => {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedRound, setSelectedRound] = useState<number | null>(null);
  const categories = Object.keys(gameWords);
  const rounds = [1, 2, 3];

  return (
    <div className="flex flex-col h-full p-4 text-white">
        <h2 className="text-3xl font-bold text-center text-cyan-400 mb-4">Game Setup</h2>
        
        <div className="flex-grow">
            <h3 className="text-xl font-semibold mb-2 text-gray-300">Choose a Category</h3>
            <div className="grid grid-cols-2 gap-2">
                {categories.map(cat => (
                    <IonButton 
                        key={cat} 
                        onClick={() => setSelectedCategory(cat)}
                        color={selectedCategory === cat ? 'primary' : 'medium'}
                        expand="block"
                    >
                        {cat}
                    </IonButton>
                ))}
            </div>

            <h3 className="text-xl font-semibold mt-6 mb-2 text-gray-300">Select Rounds</h3>
            <div className="grid grid-cols-3 gap-2">
                {rounds.map(round => (
                    <IonButton 
                        key={round} 
                        onClick={() => setSelectedRound(round)}
                        color={selectedRound === round ? 'primary' : 'medium'}
                        expand="block"
                    >
                        {round}
                    </IonButton>
                ))}
            </div>
        </div>

        <div className="flex gap-2 mt-4">
            <IonButton onClick={onBack} expand="block" size="large" color="medium" className="font-bold w-1/3">
                Back
            </IonButton>
            <IonButton 
                onClick={() => onStartGame(selectedCategory!, selectedRound!)}
                expand="block" 
                size="large" 
                className="font-bold w-2/3"
                disabled={!selectedCategory || !selectedRound}
            >
                Start Game
            </IonButton>
        </div>
    </div>
  );
};

export default CategoryScreen;
