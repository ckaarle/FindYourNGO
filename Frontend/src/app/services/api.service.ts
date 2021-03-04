// Adapted from https://www.metaltoad.com/blog/angular-api-calls-django-authentication-jwt
import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {UserService} from './user.service';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  constructor(private httpClient: HttpClient, private userService: UserService) {}

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
    if (this.userService.token && this.userService.userid.value > -1) {
      return new HttpHeaders({Authorization: 'Bearer ' + this.userService.token});
    }
    return new HttpHeaders({});
  }
}
