import {Component, Input, OnChanges, OnInit, SimpleChanges} from '@angular/core';
import {TwReview} from '../../models/ratings';
import {RatingService} from '../../services/rating.service';

@Component({
  selector: 'ngo-reviews',
  templateUrl: './ngo-reviews.component.html',
  styleUrls: ['./ngo-reviews.component.scss']
})
export class NgoReviewsComponent implements OnInit {

  @Input() ngoId: number = 0;
  @Input() ngoName: string;

  @Input() ownUserReview: TwReview = null;
  @Input() otherUserReviews: TwReview[];

  constructor() {
  }

  ngOnInit(): void {
  }

}
