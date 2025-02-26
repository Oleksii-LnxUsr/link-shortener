import { APP_INITIALIZER, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { QrComponent } from './qr/qr.component';
import { MainComponent } from './main/main.component';

import { HttpClientModule } from '@angular/common/http';
import { HttpClientInMemoryWebApiModule } from 'angular-in-memory-web-api';
//import { InMemoryDataService } from './in-memory-data.service';
import { FormsModule } from '@angular/forms';
import { ClipboardModule } from 'ngx-clipboard';
import { HeaderComponent } from './header/header.component';
import { NotfoundComponent } from './notfound/notfound.component';
import { QrService } from './qr.service';

export function initConfig(qrService: QrService) {
  return () => qrService.loadKeywords();
}

@NgModule({
  declarations: [
    AppComponent,
    QrComponent,
    MainComponent,
    HeaderComponent,
    NotfoundComponent
  ],
  imports: [
    BrowserModule.withServerTransition({ appId: 'serverApp' }),
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    //HttpClientInMemoryWebApiModule.forRoot(
    //  InMemoryDataService, { dataEncapsulation: false }
    //),
    ClipboardModule,
  ],
  providers: [
    QrService,
    { provide: APP_INITIALIZER, useFactory: initConfig, deps: [QrService], multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
