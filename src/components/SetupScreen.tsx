import React, { useState } from 'react';
import { 
  IonButton,
  IonInput,
  IonItem,
  IonList,
  IonIcon
} from '@ionic/react';
import { addCircleOutline, trash } from 'ionicons/icons';
import { Player } from '../types';

interface SetupScreenProps {
  initialPlayers: string[];
  onContinue: (names: string[]) => void;
  onBack: () => void;
}

const SetupScreen: React.FC<SetupScreenProps> = ({ initialPlayers, onContinue, onBack }) => {
  const [playerNames, setPlayerNames] = useState(
    initialPlayers.length > 0 ? initialPlayers : ['', '', '']
  );

  const handleNameChange = (index: number, newName: string) => {
    const updatedNames = [...playerNames];
    updatedNames[index] = newName;
    setPlayerNames(updatedNames);
  };

  const addPlayer = () => {
    if (playerNames.length < 10) {
      setPlayerNames([...playerNames, '']);
    }
  };

  const removePlayer = (index: number) => {
    if (playerNames.length > 3) {
      const updatedNames = playerNames.filter((_, i) => i !== index);
      setPlayerNames(updatedNames);
    }
  };

  return (
    // Use Bootstrap's flexbox utilities for the main layout
    <div className="d-flex flex-column vh-100 p-3 text-white">
      <h2 className="text-center text-info mb-4 h3">Enter Player Names</h2>
      
      {/* This div will grow to fill available space */}
      <div className="flex-grow-1 overflow-auto">
        <IonList lines="none" className="bg-transparent">
          {playerNames.map((name, index) => (
            <IonItem key={index} className="mb-2 rounded-lg custom-item">
              <IonInput
                label={`Player ${index + 1}`}
                labelPlacement="stacked"
                value={name}
                onIonInput={(e) => handleNameChange(index, e.detail.value!)}
                className="text-white"
              />
              {playerNames.length > 3 && (
                <IonButton 
                  slot="end" 
                  fill="clear"
                  onClick={() => removePlayer(index)}
                >
                  <IonIcon icon={trash} color="danger" style={{ fontSize: '24px' }}/>
                </IonButton>
              )}
            </IonItem>
          ))}
        </IonList>

        <IonButton 
          expand="block" 
          fill="outline" 
          onClick={addPlayer} 
          className="mt-3"
          disabled={playerNames.length >= 10}
        >
          <IonIcon slot="start" icon={addCircleOutline} />
          Add Player
        </IonButton>
      </div>
      
      {/* Bottom navigation buttons */}
      <div className="d-grid gap-2 mt-3">
        <IonButton 
          onClick={() => onContinue(playerNames)}
          expand="block" 
          size="large" 
          className="fw-bold"
          disabled={playerNames.some(name => name.trim() === '')}
        >
          Continue
        </IonButton>
        <IonButton onClick={onBack} expand="block" color="medium" className="fw-bold">
          Back
        </IonButton>
      </div>
    </div>
  );
};

export default SetupScreen;
