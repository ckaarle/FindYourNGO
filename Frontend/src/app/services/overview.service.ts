import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { NgoOverviewItemPagination } from '../models/ngo';

@Injectable({
  providedIn: 'root'
})
export class OverviewService {

  baseUrl = 'http://localhost:8000/ngoOverviewItems';
  pageSignifier = '?page=';

  constructor(private http: HttpClient) {}

  getNgoOverviewItems(): Observable<NgoOverviewItemPagination> {
    return this.http.get<NgoOverviewItemPagination>(this.baseUrl); // TODO: move this to request service
  }

  getNgoOverviewItemsForPage(pageNumber: number): Observable<NgoOverviewItemPagination> {
    if (pageNumber === 0) {
      return this.getNgoOverviewItems();
    }
    else {
      const url = this.baseUrl + this.pageSignifier + pageNumber.toString();
      return this.http.get<NgoOverviewItemPagination>(url);
    }
  }

}
