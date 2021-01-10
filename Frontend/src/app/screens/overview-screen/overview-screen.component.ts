import {Component, OnDestroy, OnInit} from '@angular/core';
import {FilterService} from 'src/app/services/filter.service';
import { NgoFilterOptions, NgoFilterSelection, NgoOverviewItem, NgoOverviewItemPagination} from '../../models/ngo';
import {PaginationService} from '../../services/pagination.service';
import {PaginationComponent} from '../../components/pagination/pagination.component';
import { ApiService } from '../../services/api.service';
import { ActivatedRoute } from '@angular/router';
import { CustomOverlayRef, OverlayService } from 'src/app/services/overlay.service';


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

  constructor(private filter: FilterService, protected paginationService: PaginationService, public apiService: ApiService,
    public route: ActivatedRoute, private ngoOverviewDialog: OverlayService) {
    super();
  }

  ngOnInit(): void {
    this.getFilterOptions();
    this.subscribeOverviewItemChanges();
    this.subscribeSelectedFilterChanges();
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

  openNgoDetailItem(id: number): void {
    this.apiService.get('ngoDetailItem', { id: id }).subscribe(data => {
      let ngoDetailItem: any = data;
      let dialogRef: CustomOverlayRef = this.ngoOverviewDialog.open({
        ngoDetailItem: ngoDetailItem
      });
    });
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
      this.apiService.get('ngoOverviewItems', {page: pageNumber}).subscribe(data => {
        this.processPaginatedResults(data);
      });
    }
  }

  getFilterOptions(): void {
    this.apiService.get('ngos/filteroptions/').subscribe((data: NgoFilterOptions) => {
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
}
