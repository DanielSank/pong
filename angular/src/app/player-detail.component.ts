import { Component, Input } from '@angular/core';
import { Player } from './player';

@Component({
  selector: 'player-detail',
  template: `
    <div>
      <h2>{{player.name}} details:</h2>
      <div><label>ldap: </label>{{player.ldap}}</div>
      <div>
        <label>name: </label>
        <input [(ngModel)]="player.name" placeholder="name"/>
      </div>
    </div>
  `
})
export class PlayerDetailComponent {
  @Input() player: Player;
}
