import React, { useState, useEffect } from 'react';
import { IonButton } from '@ionic/react';

interface ResultsScreenProps {
  mostVotedName: string;
  impostorName: string;
  onContinue: () => void;
}

const ResultsScreen: React.FC<ResultsScreenProps> = ({ mostVotedName, impostorName, onContinue }) => {
  const [isRevealed, setIsRevealed] = useState(false);

  useEffect(() => {
    setIsRevealed(false);
  }, [mostVotedName]);

  const handleReveal = () => {
    setIsRevealed(true);
  };

  const isCorrectGuess = mostVotedName === impostorName;

  return (
    <div className="flex flex-col h-full p-4 text-white text-center">
      <div className="flex-grow flex flex-col items-center justify-center">
        <h2 className="text-2xl text-gray-400">The group voted for:</h2>
        <p className="text-5xl font-bold my-2">{mostVotedName}</p>
        
        {isRevealed && (
          <>
            <h2 className="text-2xl text-gray-400 mt-8">The Impostor was:</h2>
            <p className="text-5xl font-bold my-2">{impostorName}</p>

            {/* MODIFIED: The text is now just a status update, not the final result */}
            <h1 className={`text-5xl font-extrabold mt-12 ${isCorrectGuess ? 'text-cyan-400' : 'text-rose-400'}`}>
              {isCorrectGuess ? "The Impostor was caught!" : "The Impostor Escaped!"}
            </h1>
          </>
        )}
      </div>
      
      {isRevealed ? (
        // MODIFIED: The button now always says "Continue"
        <IonButton onClick={onContinue} expand="block" size="large" className="font-bold tall-button solo-button">
          Continue
        </IonButton>
      ) : (
        <IonButton onClick={handleReveal} expand="block" size="large" className="font-bold tall-button solo-button">
          Reveal True Impostor
        </IonButton>
      )}
    </div>
  );
};

export default ResultsScreen;
