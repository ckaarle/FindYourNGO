import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import {Countries, Topics} from '../../models/ngo';

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
  // dummies are used to display query results after a search is called for prototyping
  dummy1: any;
  dummy2: any;

  default = 'UK';

  searchForm: FormGroup;
  nameForm: FormGroup;

  constructor(private apiService: ApiService) {
    this.searchForm = new FormGroup({
      operation: new FormControl(''),
      region: new FormControl(''),
      office: new FormControl(''),
      topic: new FormControl(''),
      trust: new FormControl(''),
    });
    this.apiService.getFromApi('countries').subscribe(data => {
      this.countries = (data as Countries).countries;
    });
    this.apiService.getFromApi('topics').subscribe(data => {
      this.topics = (data as Topics).topics;
    });
    this.nameForm = new FormGroup({name: new FormControl('')});
  }

  onFormSearch(): void {
    const queryList = this.searchForm.value;
    this.apiService.getFromApi('ngos', queryList).subscribe(data => this.dummy1 = data);
    console.log(this.dummy1);
  }

  onNameSearch(): void {
    const queryList = this.nameForm.value;
    this.apiService.getFromApi('ngos', queryList).subscribe(data => this.dummy2 = data);
    console.log(this.dummy2);
  }

}
