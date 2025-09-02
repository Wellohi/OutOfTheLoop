import React, { useState, useEffect } from 'react';
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

  useEffect(() => {
    // Reset state when the component appears (for new games)
    setCurrentPlayerIndex(0);
    setIsWordHidden(true);
    setPlayerConfirmed(false);
  }, [gameState]);


  const handleConfirmation = () => {
    setPlayerConfirmed(true);
  };

  const handleNextAction = () => {
    if (isWordHidden) {
      setIsWordHidden(false);
    } else {
      if (isLastPlayer) {
        onContinue();
      } else {
        setCurrentPlayerIndex(currentPlayerIndex + 1);
        setIsWordHidden(true);
        setPlayerConfirmed(false); // Reset confirmation for next player
      }
    }
  };

  const isWordObject = (word: WordObject | string): word is WordObject => {
      return (word as WordObject).word !== undefined;
  }

  const renderWordInfo = () => {
    if (isWordObject(currentPlayer.word)) {
      return (
        <>
          <h2 className="h4 text-accent">A palavra é:</h2>
          <p className="h1 fw-bold text-info my-3">{currentPlayer.word.word}</p>
          <p className="text-accent fst-italic">({currentPlayer.word.desc})</p>
        </>
      );
    }
    return <p className="h3 fw-bold text-danger my-3">{currentPlayer.word}</p>;
  };

  return (
    <div className="d-flex flex-column vh-100 p-4 text-white text-center">
      <div className="flex-grow-1 d-flex flex-column align-items-center justify-content-center">
        {!playerConfirmed ? (
          <>
            <h2 className="h2 fw-bold">Passe o Dispositivo Para</h2>
            <p className="h1 text-info my-3">{currentPlayer.name}</p>
          </>
        ) : isWordHidden ? (
          <>
            <h2 className="h2 fw-bold">{currentPlayer.name}</h2>
            <p className="lead text-accent mt-2">Pronto para ver a palavra?</p>
          </>
        ) : (
          renderWordInfo()
        )}
      </div>

      <div className="d-grid">
        {!playerConfirmed ? (
            <IonButton onClick={handleConfirmation} size="large" className="fw-bold">
                Eu sou {currentPlayer.name}
            </IonButton>
        ) : (
            <IonButton onClick={handleNextAction} size="large" className="fw-bold">
                {isWordHidden ? 'Toque Para Revelar' : (isLastPlayer ? 'Iniciar Interrogatório' : 'Toque Para Esconder')}
            </IonButton>
        )}
      </div>
    </div>
  );
};

export default RevealScreen;
