import {Component} from '@angular/core';
import {FormControl, FormGroup} from '@angular/forms';
import {ApiService} from '../../services/api.service';
import {Names, NgoFilterOptions} from '../../models/ngo';
import {Router} from '@angular/router';
import {FilterService} from '../../services/filter.service';
import {Utils} from '../../services/utils';
import {Observable} from 'rxjs';
import {map, startWith} from 'rxjs/operators';


@Component({
  selector: 'app-search-screen',
  templateUrl: './search-screen.component.html',
  styleUrls: ['./search-screen.component.scss']
})
export class SearchScreenComponent {
  branches: string[] = [];
  countries: string[] = [];
  topics: string[] = [];
  regions: string[] = [];
  trustworthiness: number = 0;

  searchForm: FormGroup;
  nameForm: FormGroup;

  nameControl: FormControl = new FormControl(null);

  ngoNames: string[] = [];
  $ngoNames: Observable<string[]>;

  constructor(private apiService: ApiService, private router: Router, private filter: FilterService) {
    this.searchForm = new FormGroup({
      branches: new FormControl(null),
      regions: new FormControl(null),
      countries: new FormControl(null),
      topics: new FormControl(null),
      trustworthiness: new FormControl(null),
    });

    this.nameForm = new FormGroup({name: this.nameControl});

    this.apiService.get('names').subscribe((data: Names) => {
      this.ngoNames = data.names;
    });

    this.$ngoNames = this.nameControl.valueChanges.pipe(
        startWith(''), map(value => Utils.filter(value, this.ngoNames))
    );

    this.getSearchOptions();
  }

  getSearchOptions(): void {
    this.apiService.get('ngos/filteroptions/').subscribe((data: NgoFilterOptions) => {
      const filterOptions = Utils.mapDataToNgoFilterOptions(data);
      this.branches = filterOptions.branches.values;
      this.regions = filterOptions.regions.values;
      this.countries = filterOptions.countries.values;
      this.topics = filterOptions.topics.values;
    });
  }

  onFormSearch(): void {
    const filterSelection = Utils.clearNullValues(this.searchForm.value);
    this.filter.editSelectedFilters(filterSelection, {keyToSort: 'Name', orderToSort: 'asc'});
    this.router.navigate(['overview']);
  }

  onNameSearch(): void {
    const filterSelection = Utils.clearNullValues(this.nameForm.value);
    this.filter.editSelectedFilters(filterSelection, {keyToSort: 'Name', orderToSort: 'asc'});
    this.router.navigate(['overview']);
  }
}
