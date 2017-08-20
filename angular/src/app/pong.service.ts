import { Injectable } from '@angular/core';

import { Player } from './player';
import { PLAYERS } from './mock-players';

@Injectable()
export class PongService {
  getPlayers(): Promise<Player[]> {
    return Promise.resolve(PLAYERS);
  }

  getPlayersSlowly(): Promise<Player[]> {
    return new Promise(resolve => {
      setTimeout(() => resolve(this.getPlayers()), 2000);
    });
  }
}
