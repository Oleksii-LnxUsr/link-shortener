import { isPlatformServer } from "@angular/common";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Inject, Injectable, PLATFORM_ID } from "@angular/core";
import { Meta } from "@angular/platform-browser";
import { firstValueFrom, Observable, of } from "rxjs";

import { catchError, tap } from "rxjs/operators";
import { environment } from "src/environments/environment";
import { Qr } from "./qr";

@Injectable({
  providedIn: "root",
})
export class QrService {
  private qrUrl = `${environment.API_URL}/grs`;
  private defaultKeywords = [
    "сокращатель ссылок",
    "короткие ссылки",
    "URL shortener",
    "QR code",
    "QR",
    "QR код",
  ];

  constructor(
    private http: HttpClient,
    private meta: Meta,
    @Inject(PLATFORM_ID) private platformId: any,
  ) {}

  private log(message: string) {
    console.log(`QrService: ${message}`);
  }

  private handleError<T>(operation = "operation", result?: T) {
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
      tap((_) => this.log(`fetched qr id=${shortUrl}`)),
      catchError(this.handleError<Qr>(`getQr shortUrl=${shortUrl}`)),
    );
  }

  /** GET a keywords from API, returns default fallback set if not found */
  async loadKeywords(): Promise<void> {
    //if (!isPlatformServer(this.platformId)) {
    //  return;
    //}
    return firstValueFrom(
      this.http.get<{ keywords: string[] }>(`${environment.API_URL}/keywords/`),
    )
      .then((response) => {
        if (response && response.keywords && response.keywords.length) {
          this.meta.updateTag({
            name: "keywords",
            content: response.keywords.join(","),
          });
        } else {
          this.meta.updateTag({
            name: "keywords",
            content: this.defaultKeywords.join(","),
          });
        }
      })
      .catch((err) => {
        console.warn("Failed to set keywords:", err);
        this.meta.updateTag({
          name: "keywords",
          content: this.defaultKeywords.join(","),
        });
      });
  }

  httpOptions = {
    headers: new HttpHeaders({
      "Content-Type": "application/json",
      accept: "*/*",
    }),
  };

  /** POST: add a new qr to the server */
  addQr(qr: Qr): Observable<Qr> {
    console.log(qr);
    return this.http.post<Qr>(this.qrUrl, qr, this.httpOptions).pipe(
      tap((newQr: Qr) => this.log(`added qr w/ id=${newQr.id}`)),
      catchError(this.handleError<Qr>("addQr")),
    );
  }
}
