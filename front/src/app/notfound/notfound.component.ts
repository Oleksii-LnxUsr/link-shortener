import { REQUEST } from '@nguniversal/express-engine/tokens'
import { Component, OnInit, Inject, PLATFORM_ID, Optional } from '@angular/core'
import { isPlatformServer } from "@angular/common"
import { Request } from 'express'
import { HeaderComponent } from '../header/header.component';

@Component({
  selector: 'app-notfound',
  templateUrl: './notfound.component.html',
  styleUrls: ['./notfound.component.css']
})
export class NotfoundComponent implements OnInit {
  constructor(
    @Inject(PLATFORM_ID) private platformId: any,
    @Optional() @Inject(REQUEST) private request: Request
  ) {}

  ngOnInit(): void {
    if (isPlatformServer(this.platformId)) {
      if (this.request.res) {
        this.request.res.status(404);
      }
    }
  }

}
