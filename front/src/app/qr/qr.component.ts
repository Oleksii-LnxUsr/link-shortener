import { Component, Input, OnInit } from '@angular/core';
import { ClipboardService } from 'ngx-clipboard';
import { ActivatedRoute, Router } from '@angular/router';
import { Qr } from '../qr';
import { QrService } from '../qr.service';

@Component({
  selector: 'app-qr',
  templateUrl: './qr.component.html',
  styleUrls: ['./qr.component.css']
})
export class QrComponent implements OnInit {

  //@Input() qr?: Qr;
  qr?: Qr;
  
  oldShortUrl: string = '';
  its_edit: boolean = false;

  constructor(private route: ActivatedRoute, private qrService: QrService, 
    //private _clipboardService: ClipboardService,
    private router: Router
    ) { }

  ngOnInit(): void {
    this.getQr();
    this.its_edit = false;    
    console.log('OnInit');
    /*this._clipboardService.copyResponse$.subscribe(re => {
        if (re.isSuccess) {
            alert('ссылка скопирована в буфер!');
        }
    });*/

  }

  getQr(): void {
    //const id = Number(this.route.snapshot.paramMap.get('id'));
    const shortUrl = this.route.snapshot.paramMap.get('shortUrl');
    //console.log(shortUrl)
    this.qrService.getQr(shortUrl)
      .subscribe(qr => {
        this.qr = qr
        //console.log(this.qr);
        this.oldShortUrl = qr.longUrl;
      });
  }
  
  editurl(term: string): void {
    //console.log('editurl-->>');
    //console.log(this.oldShortUrl);
    /*if (this.oldShortUrl!==term){
      this.its_edit = true;
      this.oldShortUrl = '';      
    }
    else{
      this.its_edit = false;
    }*/
    this.its_edit = true;
    this.oldShortUrl = '';
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
        this.qr = qr;
        this.GoToQr(qr);
      });
  }

  GoToQr(qr: Qr){
    this.its_edit = false;
    this.router.navigate(['/qr', qr.shortUrl.replace('https://okqr.ru/','') ]);
  }



}
