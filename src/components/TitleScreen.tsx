import React from 'react';
import { IonButton } from '@ionic/react';

interface TitleScreenProps {
  onStartGame: () => void;
}

const TitleScreen: React.FC<TitleScreenProps> = ({ onStartGame }) => {
  return (
    <div className="d-flex flex-column vh-100 p-4 text-white text-center">
      {/* This div will grow to push the content apart */}
      <div className="flex-grow-1 d-flex flex-column align-items-center justify-content-center">
        <h1 className="h1 fw-bold text-info">Out of the Loop</h1>
        <p className="lead text-accent">A game of words and suspicion.</p>
      </div>
      <div className="d-grid">
        <IonButton onClick={onStartGame} size="large" className="fw-bold">
          Start Game
        </IonButton>
      </div>
    </div>
  );
};

export default TitleScreen;
