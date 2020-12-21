import {Injectable} from '@angular/core';
import {NgoOverviewItemPagination} from '../models/ngo';
import {PaginationComponent} from '../components/pagination/pagination.component';


const MAX_PAGES_TO_DISPLAY = 5;


@Injectable({
  providedIn: 'root'
})
export class PaginationService {

  constructor() {
  }

  update(data: NgoOverviewItemPagination, component: PaginationComponent): void {
    const previousCurrentPage = component.currentPageNumber;

    if (data.previous == null && data.next == null) {
      component.surroundingPages = [];
    }

    component.currentPageNumber = data.current_page;
    component.totalPages = data.total_pages;

    this.calculateSurroundingPages(previousCurrentPage, component);
  }

  private calculateSurroundingPages(previousCurrentPage: number, component: PaginationComponent): void {
    if (component.surroundingPages.length === 0) {
      let currentPage = component.currentPageNumber;
      while (component.surroundingPages.length < MAX_PAGES_TO_DISPLAY && currentPage <= component.totalPages) {
        component.surroundingPages.push(currentPage);
        currentPage += 1;
      }
    } else {
      if (previousCurrentPage < component.currentPageNumber) {
        const nextPageNumber = component.surroundingPages[component.surroundingPages.length - 1] + 1;

        if (nextPageNumber <= component.totalPages &&
            (component.surroundingPages.length < 2
                || component.surroundingPages[component.surroundingPages.length - 1] === component.currentPageNumber)) {
          component.surroundingPages.push(nextPageNumber);
        }

        if (component.surroundingPages.length > MAX_PAGES_TO_DISPLAY) {
          component.surroundingPages.shift();
        }

      } else if (previousCurrentPage > component.currentPageNumber) {
        const nextPageNumber = component.surroundingPages[0] - 1;

        if (nextPageNumber >= 1 && component.surroundingPages[0] === component.currentPageNumber) {
          component.surroundingPages.unshift(nextPageNumber);
        }

        if (component.surroundingPages.length > MAX_PAGES_TO_DISPLAY) {
          component.surroundingPages.pop();
        }

      } else {
        // nothing to do here
      }
    }

  }
}
