import React, { useState } from 'react';
import { IonButton } from '@ionic/react';

// Define the structure of our game state for better type safety
interface Player {
  name: string;
  role: 'In the Group' | 'Out of the Loop';
  word: { word: string; desc: string } | string;
}

interface RevealScreenProps {
  gameState: Player[];
  onContinue: () => void;
}

const RevealScreen: React.FC<RevealScreenProps> = ({ gameState, onContinue }) => {
  // State to track the current player and if their word is hidden
  const [currentPlayerIndex, setCurrentPlayerIndex] = useState(0);
  const [isWordHidden, setIsWordHidden] = useState(true);

  const currentPlayer = gameState[currentPlayerIndex];
  const isLastPlayer = currentPlayerIndex === gameState.length - 1;

  const handleNextAction = () => {
    if (isWordHidden) {
      // If the word is hidden, show it.
      setIsWordHidden(false);
    } else {
      // If the word is showing...
      if (isLastPlayer) {
        // And it's the last player, continue to the next game screen.
        onContinue();
      } else {
        // Otherwise, move to the next player and hide the word again.
        setCurrentPlayerIndex(currentPlayerIndex + 1);
        setIsWordHidden(true);
      }
    }
  };

  const renderWordInfo = () => {
    if (typeof currentPlayer.word === 'object') {
      // It's a regular player
      return (
        <>
          <h2 className="text-2xl text-gray-400">Sua Palavra é:</h2>
          <p className="text-5xl font-bold text-cyan-400 my-4">{currentPlayer.word.word}</p>
          <p className="text-lg text-gray-500 italic">({currentPlayer.word.desc})</p>
        </>
      );
    }
    // It's the impostor
    return <p className="text-3xl font-bold text-rose-400 my-4">{currentPlayer.word}</p>;
  };

  return (
    <div className="flex flex-col h-full p-4 text-white text-center">
      <div className="flex-grow flex flex-col items-center justify-center">
        {isWordHidden ? (
          <>
            <h2 className="text-4xl font-bold">{currentPlayer.name}</h2>
            <p className="text-xl mt-2 text-gray-400">Sua vez, passe o telefone para ele.</p>
          </>
        ) : (
          renderWordInfo()
        )}
      </div>
      <IonButton onClick={handleNextAction} expand="block" size="large" className="font-bold">
        {isWordHidden ? 'Toque para revelar' : (isLastPlayer ? 'Iniciar Jogo' : 'Toque para Esconder')}
      </IonButton>
    </div>
  );
};

export default RevealScreen;
