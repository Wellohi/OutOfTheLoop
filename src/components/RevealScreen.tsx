import React, { useState } from 'react';
import { IonButton } from '@ionic/react';
import { Player, WordObject } from '../types';

interface RevealScreenProps {
  gameState: Player[];
  onContinue: () => void;
}

const RevealScreen: React.FC<RevealScreenProps> = ({ gameState, onContinue }) => {
  const [currentPlayerIndex, setCurrentPlayerIndex] = useState(0);
  const [isWordHidden, setIsWordHidden] = useState(true);
  const [playerConfirmed, setPlayerConfirmed] = useState(false);

  const currentPlayer = gameState[currentPlayerIndex];
  const isLastPlayer = currentPlayerIndex === gameState.length - 1;

  const handlePlayerConfirm = () => {
    setPlayerConfirmed(true);
  };

  const handleNextAction = () => {
    if (isWordHidden) {
      setIsWordHidden(false);
    } else {
      if (isLastPlayer) {
        onContinue();
      } else {
        // Reset all states for the next player
        setCurrentPlayerIndex(currentPlayerIndex + 1);
        setIsWordHidden(true);
        setPlayerConfirmed(false);
      }
    }
  };

  const renderWordInfo = () => {
    const isWordObject = (word: WordObject | string): word is WordObject => {
      return (word as WordObject).word !== undefined;
    }

    if (isWordObject(currentPlayer.word)) {
      return (
        <>
          <h2 className="text-2xl text-gray-400">Your word is:</h2>
          <p className="text-5xl font-bold text-cyan-400 my-4">{currentPlayer.word.word}</p>
          <p className="text-lg text-gray-500 italic">({currentPlayer.word.desc})</p>
        </>
      );
    }
    return <p className="text-3xl font-bold text-rose-400 my-4">{currentPlayer.word}</p>;
  };

  const renderContent = () => {
    if (!playerConfirmed) {
      return (
        <>
          <div className="flex-grow flex flex-col items-center justify-center">
            <h2 className="text-4xl font-bold">Pass the phone to</h2>
            <p className="text-5xl mt-2 text-cyan-400">{currentPlayer.name}</p>
          </div>
          {/* MODIFIED: Applied your custom button classes */}
          <IonButton onClick={handlePlayerConfirm} expand="block" size="large" className="font-bold tall-button solo-button">
            I am {currentPlayer.name}
          </IonButton>
        </>
      );
    }

    if (isWordHidden) {
      return (
        <>
          <div className="flex-grow flex flex-col items-center justify-center">
            <h2 className="text-4xl font-bold">{currentPlayer.name}</h2>
            <p className="text-xl mt-2 text-gray-400">It's your turn.</p>
          </div>
          {/* MODIFIED: Applied your custom button classes */}
          <IonButton onClick={handleNextAction} expand="block" size="large" className="font-bold tall-button solo-button">
            Tap to Reveal
          </IonButton>
        </>
      );
    }

    // Player is confirmed and word is revealed
    return (
      <>
        <div className="flex-grow flex flex-col items-center justify-center">
          {renderWordInfo()}
        </div>
        {/* MODIFIED: Applied your custom button classes */}
        <IonButton onClick={handleNextAction} expand="block" size="large" className="font-bold tall-button solo-button">
          {isLastPlayer ? 'Start Questions' : 'Tap to Hide'}
        </IonButton>
      </>
    );
  };

  return (
    <div className="flex flex-col h-full p-4 text-white text-center">
      {renderContent()}
    </div>
  );
};

export default RevealScreen;
