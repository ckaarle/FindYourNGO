import {Injectable, OnDestroy} from '@angular/core';
import {AbstractControl, ValidationErrors, ValidatorFn} from '@angular/forms';
import {BehaviorSubject, Subscription} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class NgoNameValidator implements OnDestroy {
  allNgoNames: string[] = [];

  nameSubscription: undefined | Subscription;

  constructor(allNgoNames: BehaviorSubject<string[]>) {
    this.nameSubscription = allNgoNames.subscribe(value => this.allNgoNames = value.map(name => name.toLowerCase()));
  }

  validator(): ValidatorFn {

    return (control: AbstractControl): ValidationErrors | null => {
      console.log(control.value);
      if (this.allNgoNames.indexOf(control.value.toLowerCase()) >= 0) {
        return {
          ngoNameDuplicate: true
        };
      }
      return null;
    };
  }

  ngOnDestroy(): void {
    this.nameSubscription?.unsubscribe();
  }
}
