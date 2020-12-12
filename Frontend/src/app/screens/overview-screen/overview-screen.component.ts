import {Component, OnInit} from '@angular/core';
import {NgoOverviewItem, NgoOverviewItemPagination} from '../../models/ngo';
import {OverviewService} from '../../services/overview.service';

const MAX_PAGES_TO_DISPLAY = 5;

@Component({
  selector: 'app-overview-screen',
  templateUrl: './overview-screen.component.html',
  styleUrls: ['./overview-screen.component.scss'],
})
export class OverviewScreenComponent implements OnInit {
  overviewItems: NgoOverviewItem[] = [];
  currentPageNumber = 1;
  totalPages = 1;
  surroundingPages: number[] = [];

  constructor(public overviewService: OverviewService) {
  }

  ngOnInit(): void {
    this.getNgoOverviewItems();
  }

  getNgoOverviewItems(): void {
    this.overviewService.getNgoOverviewItems().subscribe(data => {
      this.processPaginatedResults(data);
    });
  }

  private processPaginatedResults(data: NgoOverviewItemPagination): void {
    const previousCurrentPage = this.currentPageNumber;
    this.currentPageNumber = data.current_page;
    this.totalPages = data.total_pages;

    this.calculateSurroundingPages(previousCurrentPage);

    this.overviewItems = data.results;

    this.overviewItems.forEach(overviewItem => {
      overviewItem.amount = 10; // TODO: replace with amount of votes
    });
  }

  private calculateSurroundingPages(previousCurrentPage: number): void {
    const pagesToAddToCurrentToReachMaxPagesToDisplay = MAX_PAGES_TO_DISPLAY - 1;

    if (this.surroundingPages.length === 0) {
      let currentPage = this.currentPageNumber;
      while (this.surroundingPages.length < MAX_PAGES_TO_DISPLAY && currentPage <= this.totalPages) {
        this.surroundingPages.push(currentPage);
        currentPage += 1;
      }
    }
    else {
      if (previousCurrentPage < this.currentPageNumber) {
        const nextPageNumber = this.surroundingPages[this.surroundingPages.length - 1] + 1;

        if (nextPageNumber <= this.totalPages &&
            (this.surroundingPages.length < 2 || this.surroundingPages[this.surroundingPages.length - 1] === this.currentPageNumber)) {
          this.surroundingPages.push(nextPageNumber);
        }

        if (this.surroundingPages.length > MAX_PAGES_TO_DISPLAY) {
          this.surroundingPages.shift();
        }

      } else if (previousCurrentPage > this.currentPageNumber) {
          const nextPageNumber = this.surroundingPages[0] - 1;

          if (nextPageNumber >= 1 && this.surroundingPages[0] === this.currentPageNumber) {
            this.surroundingPages.unshift(nextPageNumber);
          }

          if (this.surroundingPages.length > MAX_PAGES_TO_DISPLAY) {
            this.surroundingPages.pop();
          }

      } else {
        // nothing to do here
      }
    }

  }

    getNgoOverviewItemsForPageNumber(pageNumber: number): void {
    this.overviewService.getNgoOverviewItemsForPage(pageNumber).subscribe(data => {
      this.processPaginatedResults(data);
    });
  }

}
