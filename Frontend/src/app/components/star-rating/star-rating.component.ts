import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'star-rating',
  templateUrl: './star-rating.component.html',
  styleUrls: ['./star-rating.component.scss']
})
export class StarRatingComponent implements OnInit {
  @Input() value: number = 0;
  @Input() editable: boolean = false;
  starArray: any[] = [];
  private readonly MAX_AMOUNT_OF_STARS: number = 5;

  constructor() { }

  ngOnInit(): void {
    this.starArray = new Array(this.MAX_AMOUNT_OF_STARS);
  }

  onClickItem(value: number) {
    this.value = value;
  }

  resetStarRating() {
    this.value = 0;
    this.editable = false;
    this.starArray = [];
  }

}
