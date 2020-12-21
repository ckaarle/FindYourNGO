import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'typeEvaluator'
})
export class TypeEvaluatorPipe implements PipeTransform {

  transform(value: unknown, type: string): unknown {
    switch (type) {
      case 'isStringArray':
        return this.isStringArray(value);
      case 'isBoolean':
        return this.isBoolean(value);
      default:
        return this.isStringArray(value);
    }
  }

  isStringArray(value: any): boolean {
    return Array.isArray(value);
  }

  isBoolean(value: any): boolean {
    return typeof value === 'boolean';
  }

}
