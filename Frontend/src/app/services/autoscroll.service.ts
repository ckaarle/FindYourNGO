import {Injectable} from '@angular/core';
import {NavigationEnd, Router} from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AutoscrollService {

  constructor(private router: Router) {
  }

  listen(): void {
    this.router.events.subscribe(val => {
      if (val instanceof NavigationEnd) {
        const fragmentIdx = val.urlAfterRedirects.lastIndexOf('#');
        if (fragmentIdx >= 0 && fragmentIdx < val.urlAfterRedirects.length - 1) {
          const fragment = val.urlAfterRedirects.substring(fragmentIdx + 1);
          // @ts-ignore
          document.getElementById(fragment).scrollIntoView();
        }
      }
    });
  }
}
