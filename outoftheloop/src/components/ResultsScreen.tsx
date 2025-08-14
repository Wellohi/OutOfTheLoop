import React, { useState } from 'react';
import { IonButton } from '@ionic/react';

interface ResultsScreenProps {
  mostVotedName: string;
  impostorName: string;
  onRestart: () => void;
}

const ResultsScreen: React.FC<ResultsScreenProps> = ({ mostVotedName, impostorName, onRestart }) => {
  // NEW: State to track if the final result is visible
  const [isRevealed, setIsRevealed] = useState(false);

  const handleReveal = () => {
    setIsRevealed(true);
  };

  const isCorrectGuess = mostVotedName === impostorName;

  return (
    <div className="flex flex-col h-full p-4 text-white text-center">
      <div className="flex-grow flex flex-col items-center justify-center">
        <h2 className="text-2xl text-gray-400">The group voted for:</h2>
        <p className="text-5xl font-bold my-2">{mostVotedName}</p>
        
        {/* MODIFIED: Conditionally render the final result */}
        {isRevealed && (
          <>
            <h2 className="text-2xl text-gray-400 mt-8">The Impostor was:</h2>
            <p className="text-5xl font-bold my-2">{impostorName}</p>

            <h1 className={`text-6xl font-extrabold mt-12 ${isCorrectGuess ? 'text-cyan-400' : 'text-rose-400'}`}>
              {isCorrectGuess ? "The Group Wins!" : "The Impostor Wins!"}
            </h1>
          </>
        )}
      </div>
      
      {/* MODIFIED: Conditionally render the correct button */}
      {isRevealed ? (
        <IonButton onClick={onRestart} expand="block" size="large" className="font-bold tall-button">
          Play Again
        </IonButton>
      ) : (
        <IonButton onClick={handleReveal} expand="block" size="large" className="font-bold tall-button">
          Reveal True Impostor
        </IonButton>
      )}
    </div>
  );
};

export default ResultsScreen;
