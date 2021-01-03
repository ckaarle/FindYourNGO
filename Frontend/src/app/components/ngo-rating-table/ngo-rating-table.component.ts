import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'ngo-rating-table',
  templateUrl: './ngo-rating-table.component.html',
  styleUrls: ['./ngo-rating-table.component.scss']
})
export class NgoRatingTableComponent implements OnInit {

  @Input() totalReviewNumber: number = 0;
  @Input() reviewNumberIndexedByRating: number[] = [];

  constructor() {
  }

  ngOnInit(): void {
  }

  getPercentageOfTotalReviews(reviews: number): number {
    if (this.totalReviewNumber === 0) {
      return 0;
    }
    else {
      return (reviews / this.totalReviewNumber) * 100;

    }
  }

}
