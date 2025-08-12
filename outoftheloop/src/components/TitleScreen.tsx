import React from 'react';
import { IonButton } from '@ionic/react';

// Define the props that this component accepts
interface TitleScreenProps {
  onStartGame: () => void;
}

const TitleScreen: React.FC<TitleScreenProps> = ({ onStartGame }) => {
  return (
    <div className="flex flex-col h-full p-4 text-white">
      <div className="flex-grow flex flex-col items-center justify-center text-center">
        <h1 className="text-5xl font-bold text-cyan-400">Out of the Loop</h1>
        <p className="text-lg mt-2 text-gray-400">Um jogo de palavras e suspeitos.</p>
      </div>
      <IonButton onClick={onStartGame} expand="block" size="large" className="font-bold">
        Start Game
      </IonButton>
    </div>
  );
};

export default TitleScreen;
