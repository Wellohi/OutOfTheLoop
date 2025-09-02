import React, { useState, useEffect } from 'react';
import { IonButton } from '@ionic/react';

interface ResultsScreenProps {
  mostVotedName: string | null;
  impostorName: string | null;
  onContinue: (isCorrectGuess: boolean) => void;
  onRestart: () => void;
}

const ResultsScreen: React.FC<ResultsScreenProps> = ({ mostVotedName, impostorName, onContinue, onRestart }) => {
  const [isRevealed, setIsRevealed] = useState(false);

  useEffect(() => {
    setIsRevealed(false);
  }, [mostVotedName, impostorName]);

  const handleReveal = () => setIsRevealed(true);

  const isCorrectGuess = mostVotedName === impostorName;

  return (
    <div className="d-flex flex-column vh-100 p-4 text-white text-center">
      <div className="flex-grow-1 d-flex flex-column align-items-center justify-content-center">
        <h2 className="h4 text-muted">The group voted for:</h2>
        <p className="h1 fw-bold my-2">{mostVotedName}</p>
        
        {isRevealed && (
          <div className="mt-4">
            <h2 className="h4 text-muted">The Impostor was:</h2>
            <p className="h1 fw-bold my-2">{impostorName}</p>

            <h1 className={`display-4 fw-bolder mt-5 ${isCorrectGuess ? 'text-info' : 'text-danger'}`}>
              {isCorrectGuess ? "The Group Wins!" : "The Impostor Wins!"}
            </h1>
          </div>
        )}
      </div>
      
      <div className="d-grid">
        {isRevealed ? (
          <IonButton onClick={isCorrectGuess ? onRestart : () => onContinue(isCorrectGuess)} size="large" className="fw-bold">
            {isCorrectGuess ? 'Play Again' : 'Continue'}
          </IonButton>
        ) : (
          <IonButton onClick={handleReveal} size="large" className="fw-bold">
            Reveal True Impostor
          </IonButton>
        )}
      </div>
    </div>
  );
};

export default ResultsScreen;
