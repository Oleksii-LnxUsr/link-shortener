import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MainComponent } from './main/main.component';
import { QrComponent } from './qr/qr.component';
import { RedirectComponent } from './redirect/redirect.component';
import { NotfoundComponent } from './notfound/notfound.component';

const routes: Routes = [
  { path: '', redirectTo: '/main', pathMatch: 'full' },  
  { path: 'main', component: MainComponent }, 
  { path: 'qr/:shortUrl', component: QrComponent },  
  { path: ':shortUrl', component: RedirectComponent },   
  { path: '404', component: NotfoundComponent },     
  
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
