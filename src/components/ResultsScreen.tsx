import React, { useState, useEffect } from 'react';
import { IonButton } from '@ionic/react';

interface ResultsScreenProps {
  mostVotedName: string | null;
  impostorName: string | null;
  onContinue: () => void;
  onRestart: () => void; // Keep onRestart for the final screen
}

const ResultsScreen: React.FC<ResultsScreenProps> = ({ mostVotedName, impostorName, onContinue, onRestart }) => {
  const [isRevealed, setIsRevealed] = useState(false);

  // This effect resets the screen to its initial state for a new game
  useEffect(() => {
    setIsRevealed(false);
  }, [mostVotedName, impostorName]);

  const handleReveal = () => {
    setIsRevealed(true);
  };

  const isCorrectGuess = mostVotedName === impostorName;

  return (
    <div className="d-flex flex-column vh-100 p-4 text-white text-center">
      <div className="flex-grow-1 d-flex flex-column align-items-center justify-content-center">
        <h2 className="h4 text-accent">O mais votado foi:</h2>
        <p className="display-4 fw-bold my-2">{mostVotedName}</p>
        
        {/* Conditionally render the final result after reveal */}
        {isRevealed && (
          <>
            <h2 className="h4 text-accent mt-5">Mas na verdade o impostor era:</h2>
            <p className="display-4 fw-bold my-2">{impostorName}</p>

            {/* The win/loss message based on the vote */}
            <h1 className={`display-3 fw-bolder mt-5 ${isCorrectGuess ? 'text-info' : 'text-danger'}`}>
              {isCorrectGuess ? "O impostor foi encontrado!" : "O impostor escapou!"}
            </h1>
          </>
        )}
      </div>
      
      {/* Conditionally render the correct button */}
      {isRevealed ? (
         // This button will always continue to the impostor's guess
        <IonButton onClick={onContinue} expand="block" size="large" className="fw-bold">
          Próximo
        </IonButton>
      ) : (
        <IonButton onClick={handleReveal} expand="block" size="large" className="fw-bold">
          Revelar Verdadeiro Impostor
        </IonButton>
      )}
    </div>
  );
};

export default ResultsScreen;

