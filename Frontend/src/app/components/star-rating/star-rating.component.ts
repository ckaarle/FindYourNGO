import {ChangeDetectorRef, Component, Input, OnInit} from '@angular/core';
import {ValueTransformerPipe} from 'src/app/pipes/value-transformer.pipe';

@Component({
  selector: 'star-rating',
  templateUrl: './star-rating.component.html',
  styleUrls: ['./star-rating.component.scss'],
  providers: [ValueTransformerPipe]
})
export class StarRatingComponent implements OnInit {
  public readonly MAX_AMOUNT_OF_STARS: number = 5;
  starArray: any[] = [];
  hasHalfStar: boolean = false;

  @Input() value: number = 0;
  @Input() editable: boolean = false;

  constructor(private valueFormatter: ValueTransformerPipe, private cd: ChangeDetectorRef) {
  }

  ngOnInit(): void {
    this.starArray = new Array(this.MAX_AMOUNT_OF_STARS);
    this.hasHalfStar = this.valueFormatter.hasHalfStar(this.value);
  }

  onClickItem(value: number) {
    this.value = value;
    this.hasHalfStar = this.valueFormatter.hasHalfStar(this.value);
  }

  setValue(value: number): void {
    this.value = value;
    console.log('NEW RATING VALUE IS', value)
    this.hasHalfStar = this.valueFormatter.hasHalfStar(this.value);
    this.cd.detectChanges();
  }

  resetStarRating() {
    this.value = 0;
    this.hasHalfStar = false;
    this.editable = false;
    this.starArray = [];
  }
}
