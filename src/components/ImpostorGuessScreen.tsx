import React, { useState, useEffect } from 'react';
import { IonButton } from '@ionic/react';
import { gameWords } from '../game-logic.js';
import { Player, WordObject } from '../types';

interface ImpostorGuessScreenProps {
  gameState: Player[];
  chosenCategory: string;
  impostorName: string;
  onRestart: () => void;
}

const ImpostorGuessScreen: React.FC<ImpostorGuessScreenProps> = ({ gameState, chosenCategory, impostorName, onRestart }) => {
  const [guessResult, setGuessResult] = useState<'correct' | 'incorrect' | null>(null);
  // NEW: State to hold the 6 word choices and the player's selection
  const [wordChoices, setWordChoices] = useState<WordObject[]>([]);
  const [selectedWord, setSelectedWord] = useState<string | null>(null);

  const secretWordObject = gameState.find(p => p.role === 'In the Group')?.word as WordObject;
  const secretWord = secretWordObject.word;

  // This effect runs once when the screen loads to prepare the 6 word choices.
  useEffect(() => {
    const allWordsInCategory = gameWords[chosenCategory];
    // Filter out the secret word to get a list of incorrect options
    const incorrectWords = allWordsInCategory.filter(w => w.word !== secretWord);
    
    // Shuffle the incorrect words and take the first 5
    const shuffledIncorrect = [...incorrectWords].sort(() => 0.5 - Math.random());
    const randomIncorrect = shuffledIncorrect.slice(0, 5);
    
    // Create the final list of 6 choices and shuffle it again
    const finalChoices = [...randomIncorrect, secretWordObject].sort(() => 0.5 - Math.random());
    setWordChoices(finalChoices);
  }, [gameState, chosenCategory, secretWord]);


  const handleConfirmGuess = () => {
    if (selectedWord === secretWord) {
      setGuessResult('correct');
    } else {
      setGuessResult('incorrect');
    }
  };

  if (guessResult) {
    return (
      <div className="flex flex-col h-full p-4 text-white text-center">
        <div className="flex-grow flex flex-col items-center justify-center">
          <h2 className="text-2xl text-gray-400">The secret word was:</h2>
          <p className="text-5xl font-bold my-2 text-cyan-400">{secretWord}</p>
          <h1 className={`text-6xl font-extrabold mt-12 ${guessResult === 'correct' ? 'text-cyan-400' : 'text-rose-400'}`}>
            {guessResult === 'correct' ? "Impostor Wins!" : "The Group Wins!"}
          </h1>
        </div>
        <IonButton onClick={onRestart} expand="block" size="large" className="font-bold tall-button solo-button">
          Play Again
        </IonButton>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full p-4 text-white">
      <div className="text-center">
        <h2 className="text-3xl font-bold">{impostorName}</h2>
        <p className="text-xl mt-1 text-gray-400">Guess the secret word!</p>
      </div>
      <div className="flex-grow grid gap-3 content-center mt-4">
        {wordChoices.map(({ word }) => (
          <IonButton
            key={word}
            onClick={() => setSelectedWord(word)}
            color={selectedWord === word ? 'primary' : 'medium'}
            className="font-bold guess-button"
          >
            {word}
          </IonButton>
        ))}
      </div>
      {/* NEW: Confirm button that is disabled until a word is selected */}
      <IonButton 
        onClick={handleConfirmGuess} 
        expand="block" 
        size="large" 
        className="font-bold tall-button solo-button"
        disabled={!selectedWord}
      >
        Confirm Guess
      </IonButton>
    </div>
  );
};

export default ImpostorGuessScreen;
