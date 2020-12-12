import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { Countries, Topics } from '../../models/ngo';
import { Router } from '@angular/router';

@Component({
  selector: 'app-search-screen',
  templateUrl: './search-screen.component.html',
  styleUrls: ['./search-screen.component.scss']
})
export class SearchScreenComponent {

  countries: string[] = [];
  topics: string[] = [];
  regions: string[] = ['AFRICA', 'ASIA', 'EUROPE'];
  trustworthiness: string[] = ['1', '2', '3', '4', '5'];

  searchForm: FormGroup;
  nameForm: FormGroup;

  constructor(private apiService: ApiService, private router: Router) {
    this.searchForm = new FormGroup({
      operation: new FormControl(''),
      region: new FormControl(''),
      office: new FormControl(''),
      topic: new FormControl(''),
      trust: new FormControl(''),
    });
    this.apiService.getFromApi('countries').subscribe(
        (data: Countries) => this.countries = data.countries);
    this.apiService.getFromApi('topics').subscribe(
        (data: Topics) => this.topics = data.topics);
    this.nameForm = new FormGroup({name: new FormControl('')});
  }

  onFormSearch(): void {
    const queryList = this.searchForm.value;
    this.router.navigate(['overview'], {queryParams: queryList});
  }

  onNameSearch(): void {
    const queryList = this.nameForm.value;
    this.router.navigate(['overview'], {queryParams: queryList});
  }
}
