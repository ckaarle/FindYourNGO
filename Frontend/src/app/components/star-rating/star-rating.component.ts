import { Component, Input, OnInit } from '@angular/core';
import { ValueTransformerPipe } from 'src/app/pipes/value-transformer.pipe';

@Component({
  selector: 'star-rating',
  templateUrl: './star-rating.component.html',
  styleUrls: ['./star-rating.component.scss'],
  providers: [ValueTransformerPipe]
})
export class StarRatingComponent implements OnInit {
  private readonly MAX_AMOUNT_OF_STARS: number = 5;
  starArray: any[] = [];
  hasHalfStar: boolean = false;

  @Input() value: number = 0;
  @Input() editable: boolean = false;

  constructor() { }

  ngOnInit(): void {
    this.starArray = new Array(this.MAX_AMOUNT_OF_STARS);
    if (this.value % 1 <= .7 && this.value % 1 >= .3) {
      this.hasHalfStar = true;
    }
  }

  onClickItem(value: number) {
    this.value = value;
  }

  resetStarRating() {
    this.value = 0;
    this.hasHalfStar = false;
    this.editable = false;
    this.starArray = [];
  }
}
