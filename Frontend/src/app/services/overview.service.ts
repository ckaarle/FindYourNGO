import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {NgoOverviewItemPagination} from '../models/ngo';

@Injectable({
  providedIn: 'root'
})
export class OverviewService {

  constructor(private http: HttpClient) {}

  getNgoOverviewItems(): Observable<NgoOverviewItemPagination> {
    let endpoint = 'http://localhost:8000/ngoOverviewItems';
    return this.http.get<NgoOverviewItemPagination>(endpoint); // TODO: move this to request service
  }

  getPaginatedNgoOverviewItems(endpoint: string): Observable<NgoOverviewItemPagination> {
    return this.http.get<NgoOverviewItemPagination>(endpoint);
  }
}
