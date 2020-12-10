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
    if (value % 1 < .3) {
      return Math.floor(value);
    } else {
      return Math.ceil(value);
    }
  }

  hasHalfStar(value: number) {
    var decimals = parseFloat((value % 1).toFixed(1));
    if (decimals <= .7 && decimals >= .3) {
      return true;
    }
    return false;
  }
}
