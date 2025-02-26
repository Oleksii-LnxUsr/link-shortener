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
  //public user: any;
  myuser: MyUser = {
    username: '',
    password: ''
  };
  error = "";

  constructor(private qrService: QrService, private router: Router, private _userService: UserService) { }

  ngOnInit(): void {
  }

  GoToQr(qr: Qr){
    this.router.navigate(['/qr', qr.shortUrl.replace('https://okqr.ru/','') ]);
  }

  add(longUrl: string): void {
    console.log(longUrl);

    if (!longUrl) {
      this.error = "Пожалуйста, введите URL";
      return;
    }

    longUrl = longUrl.trim();
    longUrl = longUrl.replace('http://','https://');

    if (longUrl.indexOf('https://')===-1){
      longUrl = 'https://' + longUrl;
    }

    try {
      const url = new URL(longUrl);
      console.log(url);
      if (!url.protocol || !url.hostname || !url.protocol.includes("https")) {
        this.error = "Неверная схема URL или доменное имя";
        return;
      }
    } catch (e) {
      this.error = "Неверный формат URL";
      return;
    }

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
