// src/types.ts

// Defines the structure of the word object for players in the group.
export interface WordObject {
  word: string;
  desc: string;
}

// Defines the structure of a player object in our game state.
export interface Player {
  name: string;
  role: 'In the Group' | 'Out of the Loop';
  word: WordObject | string; // It can be an object or a simple string for the impostor
}
