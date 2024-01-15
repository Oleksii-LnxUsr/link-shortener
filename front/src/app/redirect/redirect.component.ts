import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Qr } from '../qr';
import { QrService } from '../qr.service';

@Component({
  selector: 'app-redirect',
  templateUrl: './redirect.component.html',
  styleUrls: ['./redirect.component.css']
})
export class RedirectComponent implements OnInit {
  private qr?: Qr;

  constructor(private route: ActivatedRoute, private qrService: QrService, private router: Router) { }

  ngOnInit(): void {
    this.getQr();
  }
  
  getQr(): void {
    //const id = Number(this.route.snapshot.paramMap.get('id'));
    const shortUrl = this.route.snapshot.paramMap.get('shortUrl');
    //console.log(shortUrl)
    this.qrService.getQr(shortUrl)
      .subscribe(qr => {
        if (qr!==undefined){
          this.qr = qr
          console.log(this.qr);        
          window.location.href = qr.longUrl;
        }
        else{
          console.log('not found');
          window.location.href = 'https://okqr.ru/404';
        }
        
      });
  }

}
