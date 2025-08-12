import React, { useState } from 'react';
import { 
  IonContent, 
  IonButton,
  IonInput,
  IonItem,
  IonList,
  IonIcon
} from '@ionic/react';
import { addCircleOutline, removeCircleOutline } from 'ionicons/icons';

interface SetupScreenProps {
  onContinue: (names: string[]) => void;
  onBack: () => void;
}

const SetupScreen: React.FC<SetupScreenProps> = ({ onContinue, onBack }) => {
  const [playerNames, setPlayerNames] = useState(['', '', '']);

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
    <div className="flex flex-col h-full p-4 text-white">
      <h2 className="text-3xl font-bold text-center text-cyan-400 mb-4">Enter Player Names</h2>
      <IonContent>
        <IonList lines="none" className="bg-transparent">
          {playerNames.map((name, index) => (
            <IonItem key={index} className="mb-2 rounded-lg bg-gray-800 border border-gray-700">
              <IonInput
                label={`Player ${index + 1}`}
                labelPlacement="stacked"
                value={name}
                onIonInput={(e) => handleNameChange(index, e.detail.value!)}
                className="text-white"
              />
              {playerNames.length > 3 && (
                <IonButton slot="end" fill="clear" onClick={() => removePlayer(index)}>
                  <IonIcon icon={removeCircleOutline} color="danger" />
                </IonButton>
              )}
            </IonItem>
          ))}
        </IonList>
        <IonButton expand="block" fill="outline" onClick={addPlayer} className="mt-4">
          <IonIcon slot="start" icon={addCircleOutline} />
          Add Player
        </IonButton>
      </IonContent>
      <div className="flex gap-2 mt-4">
        <IonButton onClick={onBack} expand="block" size="large" color="medium" className="font-bold w-1/3">
          Back
        </IonButton>
        <IonButton 
          onClick={() => onContinue(playerNames)}
          expand="block" 
          size="large" 
          className="font-bold w-2/3"
          disabled={playerNames.some(name => name.trim() === '')}
        >
          Continue
        </IonButton>
      </div>
    </div>
  );
};

export default SetupScreen;
