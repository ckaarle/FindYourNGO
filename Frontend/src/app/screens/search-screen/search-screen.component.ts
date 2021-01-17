import {Component} from '@angular/core';
import {FormControl, FormGroup} from '@angular/forms';
import {ApiService} from '../../services/api.service';
import {NgoFilterOptions} from '../../models/ngo';
import {Router} from '@angular/router';
import {FilterService} from '../../services/filter.service';
import {Utils} from '../../services/utils';


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
    trustworthiness: number[] = [0, 1, 2, 3, 4, 5];

    searchForm: FormGroup;
    nameForm: FormGroup;

    constructor(private apiService: ApiService, private router: Router, private filter: FilterService) {
        this.searchForm = new FormGroup({
            branches: new FormControl(null),
            regions: new FormControl(null),
            countries: new FormControl(null),
            topics: new FormControl(null),
            trustworthiness: new FormControl(null),
        });

        this.nameForm = new FormGroup({name: new FormControl(null)});

        this.getSearchOptions();
    }

    getSearchOptions(): void {
        this.apiService.get('ngos/filteroptions/').subscribe((data: NgoFilterOptions) => {
            const filterOptions = this.filter.mapDataToObject(data);
            this.branches = filterOptions.branches.values;
            this.regions = filterOptions.regions.values;
            this.countries = filterOptions.countries.values;
            this.topics = filterOptions.topics.values;
        });
    }

    onFormSearch(): void {
        const filterSelection = Utils.clearNullValues(this.searchForm.value);
        this.filter.editSelectedFilters(filterSelection);
        this.router.navigate(['overview']);
    }

    onNameSearch(): void {
        const filterSelection = Utils.clearNullValues(this.nameForm.value);
        this.filter.editSelectedFilters(filterSelection);
        this.router.navigate(['overview']);
    }
}
