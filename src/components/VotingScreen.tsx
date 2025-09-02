import React, { useState, useEffect } from 'react';
import { IonButton } from '@ionic/react';
import { Player } from '../types';

interface VotingScreenProps {
  gameState: Player[];
  playerNames: string[];
  onVotingComplete: (votes: { [key: string]: number }) => void;
}

const VotingScreen: React.FC<VotingScreenProps> = ({ gameState, playerNames, onVotingComplete }) => {
  const [currentVoterIndex, setCurrentVoterIndex] = useState(0);
  const [votes, setVotes] = useState<{ [key: string]: number }>({});
  const [showFeedback, setShowFeedback] = useState(false);

  // Effect to reset the state when a new game starts
  useEffect(() => {
    const initialVotes: { [key: string]: number } = {};
    playerNames.forEach(name => initialVotes[name] = 0);
    setVotes(initialVotes);
    setCurrentVoterIndex(0);
    setShowFeedback(false);
  }, [playerNames]);


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
      <div className="d-flex flex-column vh-100 p-4 text-white align-items-center justify-content-center">
        <h2 className="h2 fw-bold text-info">Vote Registered!</h2>
      </div>
    );
  }

  // Guard clause to prevent crash before playerNames is ready
  if (!playerNames || playerNames.length === 0) {
    return <div className="p-4 text-white">Loading voters...</div>;
  }

  const currentVoter = playerNames[currentVoterIndex];

  return (
    <div className="d-flex flex-column vh-100 p-4 text-white">
      <div className="text-center">
        <h2 className="h3 fw-bold">{currentVoter}</h2>
        <p className="lead mt-1 text-muted">Who is the Impostor?</p>
      </div>
      <div className="flex-grow-1 d-grid gap-3 align-content-center mt-4">
        {gameState.map(player => {
          if (player.name === currentVoter) return null; // Can't vote for yourself
          return (
            <IonButton
              key={player.name}
              onClick={() => handleVote(player.name)}
              expand="block"
              size="large"
              color="medium"
              className="fw-bold"
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

