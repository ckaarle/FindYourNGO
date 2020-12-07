import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map, share } from 'rxjs/operators';
import { NgoOverviewItem } from '../models/ngo';

@Injectable({
  providedIn: 'root'
})
export class OverviewService {

  constructor(private http: HttpClient) {}

  getNgoOverviewItems(): Observable<NgoOverviewItem[]> {
    let endpoint = 'http://localhost:8000/ngoOverviewItems';
    return this.http.get<NgoOverviewItem[]>(endpoint); //TODO: move this to request service
  }
}
