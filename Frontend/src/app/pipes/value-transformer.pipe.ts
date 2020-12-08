import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'valueTransformer'
})
export class ValueTransformerPipe implements PipeTransform {

  transform(value: number, type: string): number {
    switch (type) {
      case 'starRound':
        return this.starRound(value);
      default:
        return this.starRound(value);
    }
  }

  starRound(value: number) {
    if (value % 1 < 3) {
      return Math.floor(value);
    } else if (value % 1 > 7) {
      return Math.ceil(value);
    } else {
      return value;
    }
  }
}