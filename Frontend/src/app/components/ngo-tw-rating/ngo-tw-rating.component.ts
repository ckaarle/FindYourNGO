import {Component, Input, OnInit} from '@angular/core';
import {RatingService} from '../../services/rating.service';
import {Router} from '@angular/router';

@Component({
  selector: 'ngo-tw-rating',
  templateUrl: './ngo-tw-rating.component.html',
  styleUrls: ['./ngo-tw-rating.component.scss']
})
export class NgoTwRatingComponent implements OnInit {
  totalTrustworthiness: number = 0;
  totalReviewNumber: number = 0;
  reviewNumberIndexedByRating: number[] = [];

  @Input() ngoId: number = 1;
  @Input() amount: number = 0;

  constructor(private ratingService: RatingService, private router: Router) {
  }

  ngOnInit(): void {
    this.ratingService.getTwRating(this.ngoId).subscribe(rating => {
      this.totalTrustworthiness = rating.totalTrustworthiness;
      this.totalReviewNumber = rating.totalReviewNumber;

      const sortedKeys = Object.keys(rating.reviewNumberByRating).sort();

      if (sortedKeys.length > 0) {
        for (const key in sortedKeys) {
          // @ts-ignore
          this.reviewNumberIndexedByRating.unshift(rating.reviewNumberByRating[(+key + 1).toString()]);
        }
      } else {
        this.reviewNumberIndexedByRating = [0, 0, 0, 0, 0];
      }

    });
  }

  showInformation(): void {
    this.router.navigate(['/about'], {fragment: 'tw-explanation'});
  }
}
