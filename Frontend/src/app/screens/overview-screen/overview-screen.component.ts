import { Component, OnInit } from '@angular/core';
import { NgoOverviewItem } from '../../models/ngo';
import { OverviewService } from '../../services/overview.service';

@Component({
  selector: 'app-overview-screen',
  templateUrl: './overview-screen.component.html',
  styleUrls: ['./overview-screen.component.scss'],
})
export class OverviewScreenComponent implements OnInit {
  overviewItems: NgoOverviewItem[] = [];

  constructor(public overviewService: OverviewService) { }

  ngOnInit(): void {
    this.getNgoOverviewItems();
  }

  getNgoOverviewItems() {
    this.overviewService.getNgoOverviewItems().subscribe(data => {
      this.overviewItems = data;
      this.overviewItems.forEach(overviewItem => {
        overviewItem.amount = 10; //TODO: replace with amount of votes
      })
    })
  }

}
