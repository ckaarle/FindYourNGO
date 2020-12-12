import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { NgoFilterOptions, NgoOverviewItem } from '../models/ngo';
import { Observable } from 'rxjs';
import { NgoOverviewItemComponent } from '../components/ngo-overview-item/ngo-overview-item.component';

@Injectable({
  providedIn: 'root'
})
export class FilterService {

  constructor(private http: HttpClient) { }

  getNgoFilterOptions(): Observable<NgoFilterOptions> {
    let endpoint = 'http://localhost:8000/ngos/filter';
    return this.http.get<NgoFilterOptions>(endpoint); //TODO: move this to request service
  }

  applyFilter(filterSelection: NgoFilterOptions): Observable<NgoOverviewItem[]> {
    let endpoint = 'http://localhost:8000/ngos/filter';
    return this.http.post<NgoOverviewItem[]>(endpoint, filterSelection);
  }
}
