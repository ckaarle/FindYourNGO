import { Component, OnInit } from '@angular/core';
import {AutoscrollService} from '../../services/autoscroll.service';

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.scss']
})
export class AboutComponent implements OnInit {

  constructor(private autoscrollService: AutoscrollService) { }

  ngOnInit(): void {
    this.autoscrollService.listen();
  }

}
