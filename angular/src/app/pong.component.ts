import { Component, OnInit } from '@angular/core';

import { PongService} from './pong.service';
import { Player } from './player';


@Component({
  selector: 'pong',
  styles: [`
    .selected {
      background-color: #CFD8DC !important;
      color: white;
    }
    .players{
      margin: 0 0 2em 0;
      list-style-type: none;
      padding: 0;
      width: 15em;
    }
    .players li {
      cursor: pointer;
      position: relative;
      left: 0;
      background-color: #EEE;
      margin: .5em;
      padding: .3em 0;
      height: 1.6em;
      border-radius: 4px;
    }
    .players li.selected:hover {
      background-color: #BBD8DC !important;
      color: white;
    }
    .players li:hover {
      color: #607D8B;
      background-color: #DDD;
      left: .1em;
    }
    .players .text {
     position: relative;
     top: -3px;
    }
    .players .badge {
      display: inline-block;
      font-size: small;
      color: white;
      padding: 0.8em 0.7em 0 0.7em;
      background-color: #607D8B;
      line-height: 1em;
      position: relative;
      left: -1px;
      top: -4px;
      height: 1.8em;
      margin-right: .8em;
      border-radius: 4px 0 0 4px;
    }
    `],
  template: `
    <ul class="players">
      <li *ngFor="let player of players"
          [class.selected]="player === selectedPlayer"
          (click)="onSelect(player)">
        <span class="badge">{{player.ldap}}</span> {{player.name}}
      </li>
    </ul>
    <div *ngIf="selectedPlayer">
      <player-detail [player]="selectedPlayer"></player-detail>
    </div>
    `,
  providers: [PongService]
})
export class PongComponent implements OnInit {
  players: Player[];
  selectedPlayer: Player;

  constructor(private pongService: PongService) {}

  getPlayers(): void {
    this.pongService.getPlayers().then(players => this.players = players);
  }

  ngOnInit(): void {
    this.getPlayers();
  }

  onSelect(player: Player): void {
    this.selectedPlayer = player;
  }
}
