import { Component } from '@angular/core';

@Component({
  selector: 'my-app',
  template: `
    <h1>{{title}}</h1>
    <h2>{{player.name}}</h2>
    <div><label>ldap: </label>{{player.ldap}}</div>
    <div>
      <label>name: </label>
      <input [(ngModel)]="player.name" placeholder="name">
    </div>
    `,
})
export class AppComponent {
  title = "Pong";
  player: Player = {
    ldap: "danielsank",
    name: "Daniel Sank"
  };
}

export class Player {
  ldap: string;
  name: string;
}
