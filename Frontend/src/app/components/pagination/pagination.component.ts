import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-pagination',
  templateUrl: './pagination.component.html',
  styleUrls: ['./pagination.component.scss']
})
export class PaginationComponent implements OnInit {

  currentPageNumber: number | undefined;
  totalPages: number | undefined;
  surroundingPages: number[] | undefined;

  constructor() { }

  ngOnInit(): void {
    this.currentPageNumber = 1;
    this.totalPages = 1;
    this.surroundingPages = [];
  }

}
