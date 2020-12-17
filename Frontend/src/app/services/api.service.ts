import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  constructor(private httpClient: HttpClient) { }
  public delete(endpoint: string, params?: any): Observable<any> {
    return this.httpClient.delete('http://localhost:8000/' + endpoint, {params});
  }
  public get(endpoint: string, params?: any): Observable<any> {
    return this.httpClient.get('http://localhost:8000/' + endpoint, {params});
  }
  public patch(endpoint: string, body: any, params?: any): Observable<any> {
    return this.httpClient.patch('http://localhost:8000/' + endpoint, body, {params});
  }
  public post(endpoint: string, body: any, params?: any): Observable<any> {
    return this.httpClient.post('http://localhost:8000/' + endpoint, body, {params});
  }
  public put(endpoint: string, body: any, params?: any): Observable<any> {
    return this.httpClient.put('http://localhost:8000/' + endpoint, body, {params});
  }
}
