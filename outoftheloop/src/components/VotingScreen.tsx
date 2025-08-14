import React, { useState } from 'react';
import { IonButton } from '@ionic/react';
import { Player } from '../types';

interface VotingScreenProps {
  gameState: Player[];
  playerNames: string[];
  onVotingComplete: (votes: { [key: string]: number }) => void;
}

const VotingScreen: React.FC<VotingScreenProps> = ({ gameState, playerNames, onVotingComplete }) => {
  const [currentVoterIndex, setCurrentVoterIndex] = useState(0);
  const [votes, setVotes] = useState<{ [key: string]: number }>(() => {
    const initialVotes: { [key: string]: number } = {};
    playerNames.forEach(name => initialVotes[name] = 0);
    return initialVotes;
  });
  const [showFeedback, setShowFeedback] = useState(false);

  const handleVote = (votedForName: string) => {
    const newVotes = { ...votes };
    newVotes[votedForName]++;
    setVotes(newVotes);
    setShowFeedback(true);

    setTimeout(() => {
      if (currentVoterIndex < playerNames.length - 1) {
        setCurrentVoterIndex(currentVoterIndex + 1);
        setShowFeedback(false);
      } else {
        onVotingComplete(newVotes);
      }
    }, 1200); // 1.2 second delay for feedback
  };

  if (showFeedback) {
    return (
      <div className="flex flex-col h-full p-4 text-white items-center justify-center">
        <h2 className="text-4xl font-bold text-cyan-400">Vote Registered!</h2>
      </div>
    );
  }

  const currentVoter = playerNames[currentVoterIndex];

  return (
    <div className="flex flex-col h-full p-4 text-white">
      <div className="text-center">
        <h2 className="text-3xl font-bold">{currentVoter}</h2>
        <p className="text-xl mt-1 text-gray-400">Who is the Impostor?</p>
      </div>
      <div className="flex-grow flex flex-col justify-center gap-4 mt-4">
        {gameState.map(player => {
          if (player.name === currentVoter) return null; // Can't vote for yourself
          return (
            <IonButton
              key={player.name}
              onClick={() => handleVote(player.name)}
              expand="block"
              size="large"
              color="medium"
              className="font-bold tall-button"
            >
              {player.name}
            </IonButton>
          );
        })}
      </div>
    </div>
  );
};

export default VotingScreen;
