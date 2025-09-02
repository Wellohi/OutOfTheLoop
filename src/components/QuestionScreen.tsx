import React, { useState, useEffect } from 'react';
import { IonButton } from '@ionic/react';
import { gameQuestions } from '../game-logic.js';

// Define the structure of a question pair
interface QuestionPair {
  asker: string;
  answerer: string;
}

interface QuestionScreenProps {
  questionPairs: QuestionPair[];
  chosenCategory: string;
  numRounds: number;
  onContinue: () => void;
}

const QuestionScreen: React.FC<QuestionScreenProps> = ({ questionPairs, chosenCategory, numRounds, onContinue }) => {
  const [currentPairIndex, setCurrentPairIndex] = useState(0);
  const [questionDeck, setQuestionDeck] = useState<string[]>([]);

  useEffect(() => {
    // A more robust way to handle potentially missing categories
    const questionsForCategory = gameQuestions[chosenCategory] || [];
    const questions = [...questionsForCategory];
    
    // Shuffle the array (Fisher-Yates shuffle)
    for (let i = questions.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [questions[i], questions[j]] = [questions[j], questions[i]];
    }
    setQuestionDeck(questions);
    setCurrentPairIndex(0); // Reset index when category changes
  }, [chosenCategory, questionPairs]); // Rerun effect if the pairs or category change

  const handleNextQuestion = () => {
    if (currentPairIndex < questionPairs.length - 1) {
      setCurrentPairIndex(currentPairIndex + 1);
    } else {
      onContinue();
    }
  };

  const handlePreviousQuestion = () => {
    if (currentPairIndex > 0) {
      setCurrentPairIndex(currentPairIndex - 1);
    }
  };

  if (questionPairs.length === 0) {
    return <div className="p-4 text-white">Loading...</div>;
  }

  const currentPair = questionPairs[currentPairIndex];
  const numPlayers = questionPairs.length / numRounds;
  const currentRound = Math.floor(currentPairIndex / numPlayers) + 1;
  const question = questionDeck[currentPairIndex % questionDeck.length] || "No more unique questions!";

  return (
    <div className="d-flex flex-column vh-100 p-4 text-white text-center">
      
      {/* This container will grow to fill space, centering its content */}
      <div className="flex-grow-1 d-flex flex-column align-items-center justify-content-center">
        <p className="lead text-accent">Round {currentRound} of {numRounds}</p>
        <h2 className="display-5 fw-bold mt-3">{currentPair.asker}</h2>
        <p className="lead my-2 text-accent">asks...</p>
        <h2 className="display-5 fw-bold">{currentPair.answerer}</h2>
        <p className="h4 text-info mt-4">"{question}"</p>
      </div>
      
      {/* Button container */}
      <div className="d-grid gap-3">
        <IonButton 
          onClick={handleNextQuestion} 
          size="large"
          className="fw-bold"
        >
          {currentPairIndex === questionPairs.length - 1 ? 'Go to Voting' : 'Next Question'}
        </IonButton>
        <IonButton 
          onClick={handlePreviousQuestion}
          size="large"
          color="medium"
          className="fw-bold"
          disabled={currentPairIndex === 0}
        >
          Previous
        </IonButton>
      </div>
    </div>
  );
};

export default QuestionScreen;

