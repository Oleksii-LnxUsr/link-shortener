import { Component, Input, OnInit } from '@angular/core';
import { ClipboardService } from 'ngx-clipboard';
import { ActivatedRoute } from '@angular/router';
import { Qr } from '../qr';
import { QrService } from '../qr.service';

@Component({
  selector: 'app-qr',
  templateUrl: './qr.component.html',
  styleUrls: ['./qr.component.css']
})
export class QrComponent implements OnInit {

  @Input() qr?: Qr;
  

  constructor(private route: ActivatedRoute, private qrService: QrService, private _clipboardService: ClipboardService) { }

  ngOnInit(): void {
    this.getQr();
    
    this._clipboardService.copyResponse$.subscribe(re => {
        if (re.isSuccess) {
            alert('ссылка скопирована в буфер!');
        }
    });

  }

  getQr(): void {
    //const id = Number(this.route.snapshot.paramMap.get('id'));
    const shortUrl = this.route.snapshot.paramMap.get('shortUrl');
    //console.log(shortUrl)
    this.qrService.getQr(shortUrl)
      .subscribe(qr => {
        this.qr = qr
        console.log(this.qr);
      });
  }

}
