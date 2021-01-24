// Adapted from https://www.metaltoad.com/blog/angular-api-calls-django-authentication-jwt
import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {BehaviorSubject, interval, Observable} from 'rxjs';

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
  public userid: BehaviorSubject<number>;
  public username: BehaviorSubject<string>;
  public ngoid: BehaviorSubject<number>;

  // error messages received from the login attempt
  public errors: any = [];

  constructor(private httpClient: HttpClient) {
    this.userid = new BehaviorSubject<number>(-1);
    this.username = new BehaviorSubject<string>('');
    this.ngoid = new BehaviorSubject<number>(-1);

    this.token = localStorage.getItem('token');
    const expiration = localStorage.getItem('token-expiration');
    if (this.token && expiration) {
      if (Date.parse(expiration) - 120000 < Date.now()) {
        this.refreshToken();
      }
      interval(120000).subscribe(x => this.refreshToken());
      this.userid.next(Number(localStorage.getItem('userid')));
      this.username.next(localStorage.getItem('username') as string);
      const ngoid = Number(localStorage.getItem('ngoid'));
      if (ngoid) {
        this.ngoid.next(ngoid);
      }
    }
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
        localStorage.setItem('refresh-token', data.refresh_token);
        this.updateData(data.access_token);
        localStorage.setItem('token', data.access_token);
        this.username.next(data.username);
        localStorage.setItem('username', this.username.value);
        this.ngoid.next(data.ngo_id);
        if (this.ngoid.value !== -1) {
          localStorage.setItem('ngoid', String(this.ngoid.value));
        }
      },
      err => {
        this.errors = err.error;
      }
    );
  }

  // Refreshes the JWT token, to extend the time the user is logged in
  public refreshToken(): void {
    this.httpClient.post(this.url('refresh/'), {refresh_token: localStorage.getItem('refresh-token')}, this.httpOptions).subscribe(
        (data: any) => {
        this.updateData(data.access_token);
        localStorage.setItem('token', data.access_token);
      },
      err => {
        this.errors = err.error;
      }
    );
  }

  public signOut(): void {
    this.token = null;
    this.tokenExpires = null;
    this.userid.next(-1);
    this.username.next('');
    this.ngoid.next(-1);
    localStorage.removeItem('refresh-token');
    localStorage.removeItem('token');
    localStorage.removeItem('token-expiration');
    localStorage.removeItem('username');
    localStorage.removeItem('ngoid');
  }

  private updateData(token: string): void {
    this.token = token;
    this.errors = [];

    // decode the token to read the username and expiration timestamp
    const tokenParts = this.token.split(/\./);
    const tokenDecoded = JSON.parse(window.atob(tokenParts[1]));
    this.tokenExpires = new Date(tokenDecoded.exp * 1000);
    localStorage.setItem('token-expiration', String(this.tokenExpires));
    this.userid.next(tokenDecoded.user_id);
    localStorage.setItem('userid', tokenDecoded.user_id);
  }
}
