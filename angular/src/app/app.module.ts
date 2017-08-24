import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms';

import { AppComponent }  from './app.component';
import { PlayerDetailComponent } from './player-detail.component';
import { PongComponent } from './pong.component';
import { PongService } from '.pong.service';

@NgModule({
  imports: [
    BrowserModule,
    FormsModule],
  declarations: [
    AppComponent,
    PlayerDetailComponent,
    PongComponent],
  providers: [
    PongService
  ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
