import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-pagination',
  templateUrl: './pagination.component.html',
  styleUrls: ['./pagination.component.scss']
})
export class PaginationComponent implements OnInit {

  currentPageNumber = 1;
  totalPages = 1;
  surroundingPages: number[] = [];

  constructor() { }

  ngOnInit(): void {
  }

}
