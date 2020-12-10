import {Component, OnInit} from '@angular/core';
import {NgoOverviewItem, NgoOverviewItemPagination} from '../../models/ngo';
import {OverviewService} from '../../services/overview.service';

@Component({
  selector: 'app-overview-screen',
  templateUrl: './overview-screen.component.html',
  styleUrls: ['./overview-screen.component.scss'],
})
export class OverviewScreenComponent implements OnInit {
  overviewItems: NgoOverviewItem[] = [];
  nextPage: string | null = null;
  previousPage: string | null = null;

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

  private processPaginatedResults(data): void {
    this.nextPage = data.next;
    this.previousPage = data.previous;
    this.overviewItems = data.results;

    // this.overviewItems.forEach(overviewItem => {
    //   overviewItem.amount = 10; // TODO: replace with amount of votes
    // });
  }

  getNextPage(): void {
    if (this.nextPage != null) {
      this.overviewService.getPaginatedNgoOverviewItems(this.nextPage).subscribe((data: NgoOverviewItemPagination) => {
        this.processPaginatedResults(data);
      });
    }
  }

  getPreviousPage(): void {
    if (this.previousPage != null) {
      this.overviewService.getPaginatedNgoOverviewItems(this.previousPage).subscribe((data: NgoOverviewItemPagination) => {
        this.processPaginatedResults(data);
      });
    }
  }

}
