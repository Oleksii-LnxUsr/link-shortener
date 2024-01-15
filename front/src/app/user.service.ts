import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of} from 'rxjs';
import { MyToken } from './mytoken';
import { MyUser } from './myuser';

import { catchError, map, tap } from 'rxjs/operators';
import { Token } from '@angular/compiler';


@Injectable({
  providedIn: 'root'
})
export class UserService {
  
  private tokenUrl: string = 'http://okqr.ru:30903/api-token-auth/';  // URL to web api

  private httpOptions = {
            headers: new HttpHeaders({'Content-Type': 'application/json'})
          };  
 
  // текущий JWT токен
  public token: string = '';
 
  // время окончания жизни токена
  public token_expires: Date | undefined;
 
  // логин пользователя
  public username: string | undefined;
 
  // сообщения об ошибках авторизации
  public errors: any = [];

  constructor(private http: HttpClient) {   
  }

  // используем http.post() для получения токена
  /*public xlogin(user: User) {
    this.http.post('/api-token-auth/', JSON.stringify(user), this.httpOptions).subscribe(
      data => {
        this.updateData(data['token']);
      },
      err => {
        this.errors = err['error'];
      }
    );
  }*/

  private log(message: string) {
    console.log(`QrService: ${message}`);
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error); // log to console instead
      return of(result as T);
    };
  }

  login(myuser: MyUser):Observable<MyToken> {
    return this.http.post<MyToken>('http://okqr.ru:30903/api-token-auth/', myuser, this.httpOptions).pipe(
      tap((newToken: MyToken) => this.log(`added qr w/ id=${newToken.newtoken}`)),
      catchError(this.handleError<MyToken>('errorLogin'))
    )
  }
      
  /*private setSession(authResult) {
      const expiresAt = moment().add(authResult.expiresIn,'second');

      localStorage.setItem('id_token', authResult.idToken);
      localStorage.setItem("expires_at", JSON.stringify(expiresAt.valueOf()) );
  } */   
 
  // обновление JWT токена
  /*public refreshToken() {
    this.http.post('/api-token-refresh/', JSON.stringify({token: this.token}), this.httpOptions).subscribe(
      data => {
        this.updateData(data['token']);
      },
      err => {
        this.errors = err['error'];
      }
    );
  }*/
 
  /*public logout() {
    this.token = null;
    this.token_expires = null;
    this.username = null;
  }*/
 
  /*private updateData(token) {
    this.token = token;
    this.errors = [];
 
    // декодирование токена для получения логина и времени жизни токена
    const token_parts = this.token.split(/\./);
    const token_decoded = JSON.parse(window.atob(token_parts[1]));
    this.token_expires = new Date(token_decoded.exp * 1000);
    this.username = token_decoded.username;
  }*/

}
