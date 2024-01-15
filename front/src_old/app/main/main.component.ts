import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Qr } from '../qr';
import { QrService } from '../qr.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  qrs: Qr[] = [];
  
  constructor(private qrService: QrService, private router: Router) { }

  ngOnInit(): void {
  }

  GoToQr(qr: Qr){
    this.router.navigate(['/qr', qr.shortUrl.replace('https://okqr.ru/','') ]);
  }

  add(longUrl: string): void {
    longUrl = longUrl.trim();
    if (!longUrl) { return; }
    this.qrService.addQr({ longUrl } as Qr)
      .subscribe(qr => {
        this.qrs.push(qr);
        this.GoToQr(qr);
      });
  }


}
