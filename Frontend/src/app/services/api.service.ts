// Adapted from https://www.metaltoad.com/blog/angular-api-calls-django-authentication-jwt
import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {BehaviorSubject, Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
    // http options used for making API calls
  private httpOptions: any;

  // the actual JWT token
  public token: string | undefined | null;

  // the token expiration date
  public tokenExpires: Date | undefined | null;

  // the username of the logged in user
  public userid: BehaviorSubject<string>;
  public username: BehaviorSubject<string>;

  // error messages received from the login attempt
  public errors: any = [];

  constructor(private httpClient: HttpClient) {
    this.userid = new BehaviorSubject<string>('');
    this.username = new BehaviorSubject<string>('');
  }
  public delete(endpoint: string, params?: any): Observable<any> {
    return this.httpClient.delete(this.url(endpoint), {headers: this.authHeader(), params});
  }
  public get(endpoint: string, params?: any): Observable<any> {
    return this.httpClient.get(this.url(endpoint), {headers: this.authHeader(), params});
  }
  public patch(endpoint: string, body: any, params?: any): Observable<any> {
    return this.httpClient.patch(this.url(endpoint), body, {headers: this.authHeader(), params});
  }
  public post(endpoint: string, body: any, params?: any): Observable<any> {
    return this.httpClient.post(this.url(endpoint), body, {headers: this.authHeader(), params});
  }
  public put(endpoint: string, body: any, params?: any): Observable<any> {
    return this.httpClient.put(this.url(endpoint), body, {headers: this.authHeader(), params});
  }

  private url(endpoint: string): string {
    return 'http://localhost:8000/' + endpoint;
  }

  private authHeader(): HttpHeaders {
    if (this.token) {
      return new HttpHeaders({Authorization: 'Bearer ' + this.token});
    }
    return new HttpHeaders({});
  }

  // Uses http.post() to get an auth token from djangorestframework-jwt endpoint
  public login(user: object): void {
    this.userPost(user, this.url('users/login/'));
  }

  public register(user: object, query?: any): void {
    this.userPost(user, this.url('users/register/'), query);
  }

  public socialLogin(token: object, endpoint: string, query?: any): void {
    this.userPost(token, this.url(endpoint), query);
  }

  private userPost(user: object, endpoint: string, query?: any): void {
    this.httpClient.post(endpoint, user, {params: query}).subscribe(
        (data: any) => {
        this.updateData(data.access_token);
        this.username.next(data.username);
      },
      err => {
        this.errors = err.error;
      }
    );
  }

  // Refreshes the JWT token, to extend the time the user is logged in
  public refreshToken(): void {
    this.httpClient.post('/api-token-refresh/', JSON.stringify({token: this.token}), this.httpOptions).subscribe(
        (data: any) => {
        this.updateData(data.token);
      },
      err => {
        this.errors = err.error;
      }
    );
  }

  public signOut(): void {
    this.token = null;
    this.tokenExpires = null;
    this.userid.next('');
    this.username.next('');
  }

  private updateData(token: string): void {
    this.token = token;
    this.errors = [];

    // decode the token to read the username and expiration timestamp
    const tokenParts = this.token.split(/\./);
    const tokenDecoded = JSON.parse(window.atob(tokenParts[1]));
    console.log(tokenDecoded);
    this.tokenExpires = new Date(tokenDecoded.exp * 1000);
    this.userid.next(tokenDecoded.user_id);
    console.log(this.userid.value);
  }
}
