import React, { useState } from 'react';
import { IonContent, IonPage } from '@ionic/react';

// --- Local Imports ---
import { setupGame } from '../game-logic.js';
import { Player } from '../types';
import TitleScreen from '../components/TitleScreen';
import SetupScreen from '../components/SetupScreen';
import CategoryScreen from '../components/CategoryScreen';
import RevealScreen from '../components/RevealScreen';
import QuestionScreen from '../components/QuestionScreen';
import VotingScreen from '../components/VotingScreen';
import ResultsScreen from '../components/ResultsScreen';
import ImpostorGuessScreen from '../components/ImpostorGuessScreen';

// --- Main Page Component ---

const Home: React.FC = () => {
  const [screen, setScreen] = useState('title');
  const [players, setPlayers] = useState<string[]>([]);
  const [gameState, setGameState] = useState<Player[] | null>(null);
  const [numRounds, setNumRounds] = useState(0);
  const [chosenCategory, setChosenCategory] = useState('');
  const [questionPairs, setQuestionPairs] = useState<{asker: string, answerer: string}[]>([]);
  const [mostVotedName, setMostVotedName] = useState<string | null>(null);
  const [impostorName, setImpostorName] = useState<string | null>(null);

  const handleStartGame = () => setScreen('setup');
  const handleBackToTitle = () => {
    setPlayers([]);
    setScreen('title');
  };
  const handleBackToSetup = () => setScreen('setup');

  const handleSetupContinue = (names: string[]) => {
    const finalNames = names.map(name => name.trim());
    setPlayers(finalNames);
    setScreen('category');
  };
  
  const handleCategoryContinue = (category: string, rounds: number) => {
    const newGameState = setupGame(players, category);
    setGameState(newGameState);
    setChosenCategory(category);
    setNumRounds(rounds);
    generateQuestionRounds(players, rounds);
    setScreen('reveal');
  };

  const handleRevealContinue = () => setScreen('question');
  const handleQuestionContinue = () => setScreen('voting');

  const handleVotingComplete = (votes: { [key: string]: number }) => {
    const votedName = Object.keys(votes).reduce((a, b) => votes[a] > votes[b] ? a : b);
    const impostor = gameState?.find(p => p.role === 'Out of the Loop');
    
    setMostVotedName(votedName);
    setImpostorName(impostor?.name || null);
    setScreen('results');
  };

  const handleResultsContinue = () => {
    // This function now ALWAYS goes to the impostor guess screen.
    setScreen('impostorGuess');
  };

  const handleRestart = () => {
    setGameState(null);
    setNumRounds(0);
    setChosenCategory('');
    setQuestionPairs([]);
    setMostVotedName(null);
    setImpostorName(null);
    setScreen('category');
  };
  
  const generateQuestionRounds = (currentPlayers: string[], rounds: number) => {
    let pairs: {asker: string, answerer: string}[] = [];
    for (let i = 0; i < rounds; i++) {
      const shuffled = [...currentPlayers].sort(() => 0.5 - Math.random());
      for (let j = 0; j < shuffled.length; j++) {
        const asker = shuffled[j];
        const answerer = shuffled[(j + 1) % shuffled.length];
        pairs.push({ asker, answerer });
      }
    }
    setQuestionPairs(pairs);
  };

  const renderScreen = () => {
    switch (screen) {
      case 'title':
        return <TitleScreen onStartGame={handleStartGame} />;
      case 'setup':
        return <SetupScreen initialPlayers={players} onContinue={handleSetupContinue} onBack={handleBackToTitle} />;
      case 'category':
        return <CategoryScreen onStartGame={handleCategoryContinue} onBack={handleBackToSetup} />;
      case 'reveal':
        return <RevealScreen gameState={gameState!} onContinue={handleRevealContinue} />;
      case 'question':
        return <QuestionScreen 
                  questionPairs={questionPairs} 
                  chosenCategory={chosenCategory} 
                  numRounds={numRounds} 
                  onContinue={handleQuestionContinue} 
               />;
      case 'voting':
        return <VotingScreen 
                  gameState={gameState!}
                  playerNames={players}
                  onVotingComplete={handleVotingComplete}
               />;
      case 'results':
        return <ResultsScreen 
                  mostVotedName={mostVotedName!}
                  impostorName={impostorName!}
                  onContinue={handleResultsContinue}
               />;
      case 'impostorGuess':
        return <ImpostorGuessScreen
                  gameState={gameState!}
                  chosenCategory={chosenCategory}
                  impostorName={impostorName!}
                  onRestart={handleRestart}
               />;
      default:
        return <TitleScreen onStartGame={handleStartGame} />;
    }
  };

  return (
    <IonPage>
      <IonContent fullscreen className="ion-color-dark">
        {renderScreen()}
      </IonContent>
    </IonPage>
  );
};

export default Home;
