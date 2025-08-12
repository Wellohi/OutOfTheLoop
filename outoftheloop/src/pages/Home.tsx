import React, { useState } from 'react';
import { IonContent, IonPage } from '@ionic/react';

// --- Local Imports ---
import { setupGame } from '../game-logic.js';
import TitleScreen from '../components/TitleScreen';
import SetupScreen from '../components/SetupScreen';
import CategoryScreen from '../components/CategoryScreen';
import RevealScreen from '../components/RevealScreen'; // NEW: Import the RevealScreen

// --- Main Page Component ---

const Home: React.FC = () => {
  const [screen, setScreen] = useState('title');
  const [players, setPlayers] = useState<string[]>([]);
  const [gameState, setGameState] = useState<any[] | null>(null);

  const handleStartGame = () => setScreen('setup');
  const handleBackToTitle = () => setScreen('title');
  const handleBackToSetup = () => setScreen('setup');

  const handleSetupContinue = (names: string[]) => {
    const finalNames = names.map(name => name.trim());
    setPlayers(finalNames);
    setScreen('category');
  };
  
  const handleCategoryContinue = (category: string, rounds: number) => {
    const newGameState = setupGame(players, category);
    setGameState(newGameState);
    // MODIFIED: Switch to the reveal screen instead of showing an alert
    setScreen('reveal');
  };

  // NEW: Function to handle continuing from the reveal screen
  const handleRevealContinue = () => {
    // For now, just show an alert. Next, we'll go to the question screen.
    alert("All words revealed! Next, we'll go to the question rounds.");
    // setScreen('question'); // This will be our next step
  };

  const renderScreen = () => {
    switch (screen) {
      case 'title':
        return <TitleScreen onStartGame={handleStartGame} />;
      case 'setup':
        return <SetupScreen onContinue={handleSetupContinue} onBack={handleBackToTitle} />;
      case 'category':
        return <CategoryScreen onStartGame={handleCategoryContinue} onBack={handleBackToSetup} />;
      // NEW: Add the case to render the reveal screen
      case 'reveal':
        return <RevealScreen gameState={gameState!} onContinue={handleRevealContinue} />;
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
