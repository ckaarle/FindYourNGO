import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'ngo-rating-table',
  templateUrl: './ngo-rating-table.component.html',
  styleUrls: ['./ngo-rating-table.component.scss']
})
export class NgoRatingTableComponent implements OnInit {

  @Input() totalCommentNumber: number = 0;
  @Input() commentNumberIndexedByRating: number[] = [];

  constructor() {
  }

  ngOnInit(): void {
  }

  getPercentageOfTotalComments(comments: number): number {
    if (this.totalCommentNumber === 0) {
      return 0;
    }
    else {
      return (comments / this.totalCommentNumber) * 100;

    }
  }

}
