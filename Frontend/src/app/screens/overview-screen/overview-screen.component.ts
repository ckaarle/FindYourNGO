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
import {ActivatedRoute, Router} from '@angular/router';
import {Utils} from '../../services/utils';
import {FavouriteService} from '../../services/favourite.service';
import {UserService} from '../../services/user.service';

export interface FilteredNgosCount {
  currentAmount: number;
  totalAmount: number;
}

@Component({
  selector: 'app-overview-screen',
  templateUrl: './overview-screen.component.html',
  styleUrls: ['./overview-screen.component.scss'],
})
export class OverviewScreenComponent extends PaginationComponent implements OnInit, OnDestroy {
  overviewItems: NgoOverviewItem[] = [];
  totalAmountOverviewItems: FilteredNgosCount = {currentAmount: 0, totalAmount: 0};

  filterOptions: NgoFilterOptions = {} as NgoFilterOptions;
  sortingOptions: string[] = [];
  loadingNgoOverviewItems: boolean = false;

  filterActive: boolean = false;
  selectedFilters: NgoFilterSelection = {};
  selectedSorting: NgoSortingSelection = {keyToSort: 'Name', orderToSort: 'asc'};

  initialized: boolean = false;

  userFavourites: number[] = [];

  constructor(
      private filter: FilterService,
      protected paginationService: PaginationService,
      public apiService: ApiService,
      public route: ActivatedRoute,
      public router: Router,
      private favouriteService: FavouriteService,
      private userService: UserService,
  ) {
    super();
    this.sortingOptions = ['Name', 'Countries', 'Cities', 'Trustworthiness', '# Reviews'];
  }

  ngOnInit(): void {
    this._restorePreviousPaginationStatus();

    this.getFilterOptions();
    this.subscribeOverviewItemChanges();
    this.subscribeSelectedFilterChanges();

    this.userService.userid.subscribe(newValue => {
      if (!newValue || newValue < 0) {
        this.userFavourites = [];
      } else {
        this.loadFavouriteNgos();
      }
    });
  }

  private _restorePreviousPaginationStatus(): void {
    const customStartPage = this.route.snapshot.paramMap.get('startPage');

    const filter = this.route.snapshot.paramMap.get('filter');
    if (!this.isNull(filter)) {
      // @ts-ignore
      this.filterActive = filter.toLowerCase() === 'true';
      this.filter.filterActive = this.filterActive;
    }
    const filterSelection = this.route.snapshot.paramMap.get('filterSelection');
    if (!this.isNull(filterSelection)) {
      // @ts-ignore
      this.selectedFilters = JSON.parse(filterSelection);
    }

    const sortingSelection = this.route.snapshot.paramMap.get('sortingSelection');
    if (!this.isNull(sortingSelection)) {
      // @ts-ignore
      this.selectedSorting = JSON.parse(sortingSelection);
    }

    const totalAmount = this.route.snapshot.paramMap.get('totalAmount');
    if (!this.isNull(totalAmount)) {
      // @ts-ignore
      this.totalAmountOverviewItems = JSON.parse(totalAmount);
    }

    if (!this.isNull(sortingSelection) || !this.isNull(filterSelection)) {
      this.filter.editSelectedFilters(this.selectedFilters, this.selectedSorting);
    }

    if (!this.isNull(customStartPage)) {
      this.initialized = true;
      this.surroundingPages = [];
      // @ts-ignore
      this.getNgoOverviewItemsForPageNumber(+customStartPage);
    }
  }

  private isNull(value: string | null): boolean {  // please don't ask
    return value == null || value === 'null';
  }

  getNgoOverviewItems(): void {
    this.apiService.get('ngoOverviewItems/totalAmount').subscribe(data => {
        this.totalAmountOverviewItems.totalAmount = data.count;
    });

    if (this.filterActive) {
      this.filter.applyFilter(this.selectedFilters, this.selectedSorting).subscribe(data =>
            this.processPaginatedResults(data));
    } else {
      const ngoOverviewSubscription = this.apiService.get('ngoOverviewItems').subscribe(data => {
        this.processPaginatedResults(data);
        ngoOverviewSubscription.unsubscribe();
      });
    }
  }

  private processPaginatedResults(data: NgoOverviewItemPagination): void {
    this.paginationService.update(data, this);

    this.loadFavouriteNgos();

    this.overviewItems = data.results;
    this.totalAmountOverviewItems.currentAmount = data.count;
  }

  private loadFavouriteNgos(): void {
    this.favouriteService.getUserFavourites().subscribe(
        result => {
          this.userFavourites = [];
          result.map(ngoOverviewItem => this.userFavourites.push(ngoOverviewItem.id));
        });
  }

  getNgoOverviewItemsForPageNumber(pageNumber: number): void {
    if (this.filterActive) {
      this.filter.applyFilter(this.selectedFilters, this.selectedSorting, pageNumber).subscribe(data => {
        this.processPaginatedResults(data);
      });
    } else {
      const ngoOverviewSubscription = this.apiService.get('ngoOverviewItems', {page: pageNumber}).subscribe(data => {
        this.processPaginatedResults(data);
        ngoOverviewSubscription.unsubscribe();
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

      if (!this.initialized) {
        this.getNgoOverviewItems();
        this.initialized = true;
      }

    }
    this.filter.selectedFiltersChanged.subscribe((selectedFilter: NgoFilterSelection) => {
      this.filterActive = selectedFilter !== {};
      this.filter.filterActive = this.filterActive;
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

  showDetail(overviewItem: NgoOverviewItem): void {
    this.router.navigate(['/detailView', overviewItem.id, {
      currentPage: this.currentPageNumber,
      filter: this.filterActive,
      filterSelection: JSON.stringify(this.selectedFilters),
      sortingSelection: JSON.stringify(this.selectedSorting),
      totalAmount: JSON.stringify(this.totalAmountOverviewItems),
      pageBeforePaginated: true,
    }]);
  }
}
