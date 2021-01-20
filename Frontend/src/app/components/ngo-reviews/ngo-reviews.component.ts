import {Component, Input, OnInit} from '@angular/core';
import {EMPTY_TW_REVIEW, TwReview} from '../../models/ratings';

@Component({
  selector: 'ngo-reviews',
  templateUrl: './ngo-reviews.component.html',
  styleUrls: ['./ngo-reviews.component.scss']
})
export class NgoReviewsComponent implements OnInit {

  @Input() ngoId: number = 0;
  @Input() ngoName: string = '';

  @Input() ownUserReview: TwReview = EMPTY_TW_REVIEW;
  @Input() otherUserReviews: TwReview[] = [];

  constructor() {
  }

  ngOnInit(): void {
  }

}
