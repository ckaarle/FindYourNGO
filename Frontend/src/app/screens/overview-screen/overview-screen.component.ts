import {Component, OnInit} from '@angular/core';
import {OverviewService} from '../../services/overview.service';
import {FilterService} from 'src/app/services/filter.service';
import {NgoFilterOptions, NgoFilterSelection, NgoOverviewItem, NgoOverviewItemPagination} from '../../models/ngo';
import {PaginationService} from '../../services/pagination.service';
import {PaginationComponent} from '../../components/pagination/pagination.component';
import {ApiService} from '../../services/api.service';
import {ActivatedRoute, Router} from '@angular/router';
import {OverlayService} from 'src/app/services/overlay.service';


@Component({
  selector: 'app-overview-screen',
  templateUrl: './overview-screen.component.html',
  styleUrls: ['./overview-screen.component.scss'],
})
export class OverviewScreenComponent extends PaginationComponent implements OnInit {
  overviewItems: NgoOverviewItem[] = [];
  queryList: any = {};

  filterOptions: NgoFilterOptions = {} as NgoFilterOptions;
  loadingNgoOverviewItems: boolean = false;

  filterActive: boolean = false;
  selectedFilters: NgoFilterSelection = {};

  constructor(private overviewService: OverviewService, private filter: FilterService, protected paginationService: PaginationService,
              public apiService: ApiService, public route: ActivatedRoute, private ngoOverviewDialog: OverlayService,
              private router: Router) {
    super();
  }

  ngOnInit(): void {
    this.route.queryParams.subscribe(
        params => this.queryList = params);
    this.getNgoOverviewItems();
    this.getFilterOptions();
    this.subscribeOverviewItemChanges();
    this.subscribeSelectedFilterChanges();
  }


  getNgoOverviewItems(): void {
    this.apiService.get('ngoOverviewItems', this.queryList).subscribe(
        data => this.processPaginatedResults(data));
  }

  private processPaginatedResults(data: NgoOverviewItemPagination): void {
    this.paginationService.update(data, this);
    this.overviewItems = data.results;

    this.overviewItems.forEach(overviewItem => {
      overviewItem.amount = 10; // TODO: replace with amount of votes
    });
  }

  getNgoOverviewItemsForPageNumber(pageNumber: number): void {
    if (this.filterActive) {
      this.filter.applyFilter(this.selectedFilters, pageNumber).subscribe(data => {
        this.processPaginatedResults(data);
      });
    } else {
      this.overviewService.getNgoOverviewItemsForPage(pageNumber).subscribe(data => {
        this.processPaginatedResults(data);
      });
    }
  }

  // getNgoOverviewItemsForPageNumber(pageNumber: number): void {
  //   this.apiService.get('ngoOverviewItems', {...this.queryList, page: pageNumber}).subscribe(
  //       data => this.processPaginatedResults(data));
  // }

  getFilterOptions(): void {
    this.filter.getNgoFilterOptions().subscribe(data => {
      this.filterOptions = this.filter.mapDataToObject(data);
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
    this.filter.selectedFiltersChanged.subscribe((selectedFilter: NgoFilterSelection) => {
      this.filterActive = selectedFilter !== {};
      this.selectedFilters = selectedFilter;
    });
  }

  showFilteredNgoItems(filteredOverviewItems: NgoOverviewItemPagination): void {
    this.processPaginatedResults(filteredOverviewItems);
    console.log('Filtered Items:', this.overviewItems);
  }
}
