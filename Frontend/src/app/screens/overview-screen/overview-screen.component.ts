import {Component, OnDestroy, OnInit} from '@angular/core';
import {FilterService} from 'src/app/services/filter.service';
import {NgoFilterOptions, NgoFilterSelection, NgoOverviewItem, NgoOverviewItemPagination} from '../../models/ngo';
import {PaginationService} from '../../services/pagination.service';
import {PaginationComponent} from '../../components/pagination/pagination.component';
import {ApiService} from '../../services/api.service';
import {ActivatedRoute, Router} from '@angular/router';
import {Utils} from '../../services/utils';


@Component({
  selector: 'app-overview-screen',
  templateUrl: './overview-screen.component.html',
  styleUrls: ['./overview-screen.component.scss'],
})
export class OverviewScreenComponent extends PaginationComponent implements OnInit, OnDestroy {
  overviewItems: NgoOverviewItem[] = [];

  filterOptions: NgoFilterOptions = {} as NgoFilterOptions;
  loadingNgoOverviewItems: boolean = false;

  filterActive: boolean = false;
  selectedFilters: NgoFilterSelection = {};

  constructor(
      private filter: FilterService,
      protected paginationService: PaginationService,
      public apiService: ApiService,
      public route: ActivatedRoute,
      public router: Router,
      ) {
    super();
  }

  ngOnInit(): void {
    this.getFilterOptions();
    this.subscribeOverviewItemChanges();
    this.subscribeSelectedFilterChanges();

    const customStartPage = this.route.snapshot.paramMap.get('startPage');
    if (customStartPage != null && customStartPage !== 'null') { // please don't ask
      this.getNgoOverviewItemsForPageNumber(+customStartPage);
    }
  }

  getNgoOverviewItems(): void {
    if (this.filterActive) {
      this.filter.applyFilter(this.selectedFilters).subscribe(data =>
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
      this.filter.applyFilter(this.selectedFilters, pageNumber).subscribe(data => {
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
    this.filter.editSelectedFilters({});
    this.filter.applyFilter({}).subscribe(data => {
      this.filter.displayFilteredNgoItems(data);
    });
  }

  showDetail(overviewItem: NgoOverviewItem): void {
    this.router.navigate(['/detailView', overviewItem.id, {currentPage: this.currentPageNumber}]);
  }
}
