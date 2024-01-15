import { Injectable } from '@angular/core';
import { InMemoryDbService } from 'angular-in-memory-web-api';
import { Qr } from './qr';


@Injectable({
  providedIn: 'root'
})
export class InMemoryDataService implements InMemoryDbService {
  createDb() {
    const qrs = [
      { id: 12, longUrl: 'https://ya.ru', shortUrl: 'BSDF' },
      { id: 13, longUrl: 'https://google.com', shortUrl: 'FDGF' },      
    ];
    return {qrs};
  }

  // Overrides the genId method to ensure that a hero always has an id.
  // If the heroes array is empty,
  // the method below returns the initial number (11).
  // if the heroes array is not empty, the method below returns the highest
  // qr id + 1.
  genId(qrs: Qr[]): number {
    return qrs.length > 0 ? Math.max(...qrs.map(qr => qr.id)) + 1 : 11;
  }
}
