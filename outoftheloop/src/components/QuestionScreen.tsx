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
    const questions = [...gameQuestions[chosenCategory]];
    for (let i = questions.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [questions[i], questions[j]] = [questions[j], questions[i]];
    }
    setQuestionDeck(questions);
  }, [chosenCategory]);

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
    return <div>Loading...</div>;
  }

  const currentPair = questionPairs[currentPairIndex];
  const numPlayers = questionPairs.length / numRounds;
  const currentRound = Math.floor(currentPairIndex / numPlayers) + 1;
  const question = questionDeck[currentPairIndex % questionDeck.length] || "No more unique questions!";

  return (
    <div className="flex flex-col h-full p-4 text-white text-center">
      {/* This container will now center all its content vertically */}
      <div className="flex-grow flex flex-col items-center justify-center">
        
        {/* Text content block */}
        <div className="flex-grow flex flex-col items-center justify-center">
            <p className="text-xl text-gray-400">Round {currentRound} of {numRounds}</p>
            <h2 className="text-4xl font-bold mt-4">{currentPair.asker}</h2>
            <p className="text-lg my-2 text-gray-500">asks...</p>
            <h2 className="text-4xl font-bold">{currentPair.answerer}</h2>
            <p className="text-3xl font-semibold text-cyan-400 mt-8">"{question}"</p>
        </div>
        
        {/* Button container with new sizing and spacing */}
        <div className="w-full max-w-xs mb-8">
          <div className="flex flex-col gap-4">
            <IonButton 
              onClick={handleNextQuestion} 
              expand="block" 
              // Using our new custom class from variables.css
              className="tall-button"
            >
              {currentPairIndex === questionPairs.length - 1 ? 'Go to Voting' : 'Next Question'}
            </IonButton>
            <IonButton 
              onClick={handlePreviousQuestion}
              expand="block" 
              color="medium"
              // Using our new custom class from variables.css
              className="tall-button"
              disabled={currentPairIndex === 0}
            >
              Previous
            </IonButton>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuestionScreen;
