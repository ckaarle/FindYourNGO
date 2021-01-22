import {Component, OnDestroy, OnInit} from '@angular/core';
import {FilterService} from 'src/app/services/filter.service';
import {
    NgoFilterOptions,
    NgoFilterSelection,
    NgoOverviewItem,
    NgoOverviewItemPagination,
    NgoSortingSelection
} from '../../models/ngo';
import {PaginationService} from '../../services/pagination.service';
import {PaginationComponent} from '../../components/pagination/pagination.component';
import {ApiService} from '../../services/api.service';
import {ActivatedRoute} from '@angular/router';
import {Utils} from '../../services/utils';


@Component({
  selector: 'app-overview-screen',
  templateUrl: './overview-screen.component.html',
  styleUrls: ['./overview-screen.component.scss'],
})
export class OverviewScreenComponent extends PaginationComponent implements OnInit, OnDestroy {
  overviewItems: NgoOverviewItem[] = [];

  filterOptions: NgoFilterOptions = {} as NgoFilterOptions;
  sortingOptions: string[] = [];
  loadingNgoOverviewItems: boolean = false;

  filterActive: boolean = false;
  selectedFilters: NgoFilterSelection = {};
  selectedSorting: NgoSortingSelection = {keyToSort: 'Name', orderToSort: 'asc'};

  constructor(private filter: FilterService, protected paginationService: PaginationService,
              public apiService: ApiService, public route: ActivatedRoute) {
    super();
    this.sortingOptions = ['Name', 'Countries', 'Cities', 'Trustworthiness'];
  }

  ngOnInit(): void {
    this.getFilterOptions();
    this.subscribeOverviewItemChanges();
    this.subscribeSelectedFilterChanges();
  }

  getNgoOverviewItems(): void {
    if (this.filterActive) {
      this.filter.applyFilter(this.selectedFilters, this.selectedSorting).subscribe(data =>
            this.processPaginatedResults(data));
    } else {
        this.apiService.get('ngoOverviewItems').subscribe(data =>
            this.processPaginatedResults(data));
    }
  }

  private processPaginatedResults(data: NgoOverviewItemPagination): void {
    this.paginationService.update(data, this);
    this.overviewItems = data.results;
  }

  getNgoOverviewItemsForPageNumber(pageNumber: number): void {
    if (this.filterActive) {
      this.filter.applyFilter(this.selectedFilters, this.selectedSorting, pageNumber).subscribe(data => {
        this.processPaginatedResults(data);
      });
    } else {
      this.apiService.get('ngoOverviewItems', {page: pageNumber}).subscribe(data => {
        this.processPaginatedResults(data);
      });
    }
  }

  getFilterOptions(): void {
    this.apiService.get('ngos/filteroptions/').subscribe((data: NgoFilterOptions) => {
      this.filterOptions = Utils.mapDataToNgoFilterOptions(data);
      this.selectedSorting = {keyToSort: 'Name', orderToSort: 'asc'};
    });
  }

  subscribeOverviewItemChanges(): void {
    this.filter
    .loadingNgoOverviewItems
    .subscribe((data: boolean) => {
      this.loadingNgoOverviewItems = true;
    });
    this.filter
    .filteredNgoOverviewItemsChanged
    .subscribe((data: NgoOverviewItemPagination) => {
      this.showFilteredNgoItems(data);
      this.loadingNgoOverviewItems = false;
    });
  }

  subscribeSelectedFilterChanges(): void {
    if (!this.filterActive) {
        this.selectedFilters = this.filter.getSelectedFilters();
        this.filterActive = Object.keys(this.selectedFilters).length > 0;
        this.getNgoOverviewItems();
    }
    this.filter.selectedFiltersChanged.subscribe((selectedFilter: NgoFilterSelection) => {
      this.filterActive = selectedFilter !== {};
      this.selectedFilters = selectedFilter;
    });
  }

  showFilteredNgoItems(filteredOverviewItems: NgoOverviewItemPagination): void {
    this.processPaginatedResults(filteredOverviewItems);
  }

  ngOnDestroy(): void {
    const selectedSorting: NgoSortingSelection = {keyToSort: 'Name', orderToSort: 'asc'};
    this.filter.editSelectedFilters({}, selectedSorting);
    this.filter.applyFilter({}, this.selectedSorting).subscribe(data => {
          this.filter.displayFilteredNgoItems(data);
    });
  }
}
