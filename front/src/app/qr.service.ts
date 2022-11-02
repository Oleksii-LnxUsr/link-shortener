import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { catchError, map, tap } from 'rxjs/operators';
import { Qr } from './qr';

@Injectable({
  providedIn: 'root'
})
export class QrService {
  
  //private qrUrl = 'api/qrs';  // URL to web api
  private qrUrl = 'https://okqr.ru/api/grs';  // URL to web api
  

  constructor(private http: HttpClient) { }

  private log(message: string) {
    console.log(`QrService: ${message}`);
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
  
      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead
  
      // TODO: better job of transforming error for user consumption
      //this.log(`${operation} failed: ${error.message}`);
  
      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

  /** GET hero by id. Will 404 if id not found */
  getQr(shortUrl: string | null = null): Observable<Qr> {
    const url = `${this.qrUrl}/${shortUrl}/`;
    return this.http.get<Qr>(url).pipe(
      tap(_ => this.log(`fetched qr id=${shortUrl}`)),
      catchError(this.handleError<Qr>(`getQr shortUrl=${shortUrl}`))
    );
  }

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json', 'accept': '*/*'})
  };

  /** POST: add a new qr to the server */
  addQr(qr: Qr): Observable<Qr> {
    console.log(qr);
    return this.http.post<Qr>(this.qrUrl, qr, this.httpOptions).pipe(
      tap((newQr: Qr) => this.log(`added qr w/ id=${newQr.id}`)),
      catchError(this.handleError<Qr>('addQr'))
    );
  }
  

}
