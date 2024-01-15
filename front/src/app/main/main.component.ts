import { group } from '@angular/animations';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MyUser } from '../myuser';
import { Qr } from '../qr';
import { QrService } from '../qr.service';
import { UserService } from '../user.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  //qrs: Qr[] = [];
  referrer_url: string = '';
  //public user: any;
  myuser: MyUser = {
    username: '',
    password: ''
  };
  
  constructor(private qrService: QrService, private router: Router, private _userService: UserService) { }

  ngOnInit(): void {
    console.log('document.referrer-->');
    console.log(document.referrer.toString());
    this.referrer_url = document.referrer.toString();    
  }
  

  GoToQr(qr: Qr){
    this.router.navigate(['/qr', qr.shortUrl.replace('https://okqr.ru/','') ]);
  }

  add(longUrl: string): void {
    longUrl = longUrl.trim();
    longUrl = longUrl.replace('http://','https://');
    if (longUrl.indexOf('https://')===-1){
      longUrl = 'https://'+longUrl;
    }

    if (!longUrl) { return; }
    
    
    this.qrService.addQr({ longUrl } as Qr)
      .subscribe(qr => {
        //this.qrs.push(qr);
        this.GoToQr(qr);
      });
  }

  login(user: MyUser) {
    this._userService.login(user);
  }
 
  /*refreshToken() {
    this._userService.refreshToken();
  }
 
  logout() {
    this._userService.logout();
  }*/



}
