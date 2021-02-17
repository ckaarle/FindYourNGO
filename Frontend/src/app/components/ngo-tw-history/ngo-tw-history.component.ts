import {Component, Input, OnInit} from '@angular/core';
import {RatingService} from '../../services/rating.service';
import {NgoTWDataPoint} from '../../models/ratings';
import {EChartsOption} from 'echarts';
import {DatePipe} from '@angular/common';
import * as echarts from 'echarts';

@Component({
  selector: 'ngo-tw-history',
  templateUrl: './ngo-tw-history.component.html',
  styleUrls: ['./ngo-tw-history.component.scss'],
  providers: [DatePipe]
})
export class NgoTwHistoryComponent implements OnInit {
  @Input() ngoId: number = 1;
  options: any;

  constructor(public datePipe: DatePipe, private ratingService: RatingService) {}

  ngOnInit(): void {
    if (this.ngoId) {
        this.ratingService.getTwHistory(this.ngoId).subscribe((dataPoints: NgoTWDataPoint[]) => {
          this.createHistoryData(dataPoints);
        });
    }
  }

  createHistoryData(dataPoints: NgoTWDataPoint[]): void {
    const data: any[] = [];
    for (const dataPoint of dataPoints) {
      data.push([new Date(dataPoint.date), dataPoint.dailyTwScore]);
    }
    this.createChartOptions(data);
  }

  createChartOptions(data: any[]): void {
    this.options = {
      grid: {
        top: 10,
        right: 10,
        bottom: 0,
        left: 0,
        containLabel: true
      },
      xAxis: {
        type: 'time',
        axisLine: {
          show: false
        },
        axisTick: {
          show: false
        },
        minInterval: 3600 * 1000 * 24,
        axisLabel: {
          formatter: (params: any) => {
            return this.datePipe.transform(new Date(params), 'MMM d');
          },
          showMinLabel: true,
          showMaxLabel: false,
          fontSize: 10
        }
      },
      yAxis: {
        type: 'value',
        min: 0,
        max: 5,
        interval: 1,
        axisLabel: {
          showMinLabel: true,
          showMaxLabel: true,
          fontSize: 10
        },
        axisTick: {
          show: false
        }
      },
      tooltip: {
        borderColor: '#424242',
        textStyle: {
          color: '#424242'
        },
        trigger: 'axis',
        axisPointer: {
            animation: false
        }
      },
      series: [
        {
          name: 'TW value:',
          data: data,
          type: 'line',
          smooth: true,
          symbol: 'circle',
          itemStyle: {
            color: '#c62828'
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
              offset: 0,
              color: '#c62828'
            }, {
              offset: 0.75,
              color: '#ffc107'
            }, {
              offset: 1,
              color: '#ffffff'
            }])
          },
        }
      ]
    };
  }


}
