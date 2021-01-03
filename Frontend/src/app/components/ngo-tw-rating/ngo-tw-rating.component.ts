import {Component, Input, OnInit} from '@angular/core';
import {RatingService} from '../../services/rating.service';

@Component({
  selector: 'ngo-tw-rating',
  templateUrl: './ngo-tw-rating.component.html',
  styleUrls: ['./ngo-tw-rating.component.scss']
})
export class NgoTwRatingComponent implements OnInit {

  totalTrustworthiness: number;
  baseTrustworthiness: number;
  userTrustworthiness: number;
  totalReviewNumber: number;
  reviewNumberIndexedByRating: number[] = [];

  @Input() ngoId: number = 1;

  NGO_ID = 2; // TODO remove later

  constructor(private ratingService: RatingService) {
  }

  ngOnInit(): void {
    // const twRating = this.ratingService.getTwRating(this.ngoId).subscribe(rating => { TODO put back in
    this.ratingService.getTwRating(this.ngoId).subscribe(rating => {
      this.totalTrustworthiness = rating.totalTrustworthiness;
      this.baseTrustworthiness = rating.baseTrustworthiness;
      this.userTrustworthiness = rating.userTrustworthiness;
      this.totalReviewNumber = rating.totalReviewNumber;

      const sortedKeys = Object.keys(rating.reviewNumberByRating).sort();

      if (sortedKeys.length > 0) {
        for (const key in sortedKeys) {
          this.reviewNumberIndexedByRating.unshift(rating.reviewNumberByRating[(+key + 1).toString()]);
        }
      } else {
        this.reviewNumberIndexedByRating = [0, 0, 0, 0, 0];
      }

    });
  }

}
